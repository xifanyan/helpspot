use crate::config::ConfigFile;
use crate::errors::{Error, Result};
use crate::types::*;
use reqwest::blocking::Client;
use serde::Deserialize;
use std::collections::HashMap;
use std::time::Duration;

const BASE_PATH: &str = "/api/index.php";

pub struct HelpSpotClient {
    client: Client,
    config: Config,
}

pub struct Config {
    pub base_url: String,
    pub api_key: Option<String>,
    pub username: Option<String>,
    pub password: Option<String>,
    pub output: String,
    pub columns: Option<String>,
    pub timeout: Duration,
    pub debug: bool,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            base_url: String::new(),
            api_key: None,
            username: None,
            password: None,
            output: "json".to_string(),
            columns: None,
            timeout: Duration::from_secs(30),
            debug: false,
        }
    }
}

impl HelpSpotClient {
    pub fn new(config: Config) -> Result<Self> {
        if config.base_url.is_empty() {
            return Err(Error::MissingBaseURL);
        }

        let client = Client::builder().timeout(config.timeout).build()?;

        Ok(Self { client, config })
    }

    pub fn from_config_file(config_file: &ConfigFile) -> Result<Self> {
        let config = Config {
            base_url: config_file.base_url.clone(),
            api_key: config_file.api_key.clone(),
            username: config_file.username.clone(),
            password: config_file.password.clone(),
            output: config_file
                .output
                .clone()
                .unwrap_or_else(|| "json".to_string()),
            columns: None,
            timeout: Duration::from_secs(config_file.timeout.unwrap_or(30)),
            debug: false,
        };

        Self::new(config)
    }

    fn build_url(&self, method: &str) -> String {
        format!(
            "{}{}?method={}&output=json",
            self.config.base_url, BASE_PATH, method
        )
    }

    fn is_post_method(&self, method: &str) -> bool {
        let public_post = matches!(
            method,
            "request.create" | "request.update" | "forums.createTopic" | "forums.createPost"
        );

        if public_post {
            return true;
        }

        if method.starts_with("private.") {
            return !matches!(method, "private.request.get" | "private.request.search");
        }

        false
    }

    pub fn do_request<T: serde::de::DeserializeOwned>(
        &self,
        method: &str,
        params: HashMap<String, String>,
    ) -> Result<T> {
        let url = self.build_url(method);

        if self.config.debug {
            eprintln!("API Request: {} {}", method, url);
            if !params.is_empty() {
                eprintln!("Params: {:?}", params);
            }
        }

        let req_params = params;

        let mut request = if self.is_post_method(method) {
            let mut all_params = req_params.clone();
            all_params.insert("method".to_string(), method.to_string());
            self.client
                .post(&url)
                .header("Content-Type", "application/x-www-form-urlencoded")
                .form(&all_params)
        } else if !req_params.is_empty() {
            self.client.get(&url).query(&req_params)
        } else {
            self.client.get(&url)
        };

        if let Some(ref api_key) = self.config.api_key {
            if !api_key.is_empty() {
                request = request.header("Authorization", format!("Bearer {}", api_key));
            } else if let (Some(ref username), Some(ref password)) =
                (&self.config.username, &self.config.password)
            {
                if !username.is_empty() && !password.is_empty() {
                    let credentials = base64::Engine::encode(
                        &base64::engine::general_purpose::STANDARD,
                        format!("{}:{}", username, password),
                    );
                    request = request.header("Authorization", format!("Basic {}", credentials));
                }
            }
        } else if let (Some(ref username), Some(ref password)) =
            (&self.config.username, &self.config.password)
        {
            if !username.is_empty() && !password.is_empty() {
                let credentials = base64::Engine::encode(
                    &base64::engine::general_purpose::STANDARD,
                    format!("{}:{}", username, password),
                );
                request = request.header("Authorization", format!("Basic {}", credentials));
            }
        }

        let response = request.send()?;

        if response.status().as_u16() >= 400 {
            let status = response.status();
            let body = response.text().unwrap_or_default();
            return Err(self.parse_error(&body, status.as_u16()));
        }

        let body = response.text()?;

        if self.config.debug {
            eprintln!("Response: {}", body);
        }

        let result: T = serde_json::from_str(&body)?;
        Ok(result)
    }

    fn parse_error(&self, body: &str, status: u16) -> Error {
        if let Ok(response) = serde_json::from_str::<Response>(body) {
            if let Some(errors) = response.errors {
                if let Some(error) = errors.first() {
                    return Error::from_api_error(error.id, error.description.clone());
                }
            }
        }
        Error::ApiError {
            id: status as i32,
            description: body.to_string(),
        }
    }

    pub fn get_version(&self) -> Result<VersionResponse> {
        self.do_request("version", HashMap::new())
    }

    pub fn private_get_version(&self) -> Result<VersionResponse> {
        self.do_request("private.version", HashMap::new())
    }

    pub fn create_request(&self, params: HashMap<String, String>) -> Result<Request> {
        #[derive(Deserialize)]
        struct RequestWrapper {
            request: Option<Request>,
        }

        let wrapper: RequestWrapper = self.do_request("request.create", params)?;
        wrapper.request.ok_or_else(|| Error::ApiError {
            id: 1,
            description: "Missing request in response".to_string(),
        })
    }

    pub fn get_request(&self, access_key: &str) -> Result<Request> {
        let mut params = HashMap::new();
        params.insert("accesskey".to_string(), access_key.to_string());

        #[derive(Deserialize)]
        struct RequestWrapper {
            request: Option<Request>,
        }

        let wrapper: RequestWrapper = self.do_request("request.get", params)?;
        wrapper.request.ok_or_else(|| Error::ApiError {
            id: 1,
            description: "Missing request in response".to_string(),
        })
    }

    pub fn update_request(&self, params: HashMap<String, String>) -> Result<Request> {
        #[derive(Deserialize)]
        struct RequestWrapper {
            request: Option<Request>,
        }

        let wrapper: RequestWrapper = self.do_request("request.update", params)?;
        wrapper.request.ok_or_else(|| Error::ApiError {
            id: 1,
            description: "Missing request in response".to_string(),
        })
    }

    pub fn get_categories(&self) -> Result<Vec<Category>> {
        #[derive(Deserialize)]
        struct CategoriesWrapper {
            categories: Option<Vec<Category>>,
        }

        let wrapper: CategoriesWrapper =
            self.do_request("request.getCategories", HashMap::new())?;
        Ok(wrapper.categories.unwrap_or_default())
    }

    pub fn get_custom_fields(&self) -> Result<Vec<CustomField>> {
        #[derive(Deserialize)]
        struct CustomFieldsWrapper {
            customfields: Option<Vec<CustomField>>,
        }

        let wrapper: CustomFieldsWrapper =
            self.do_request("request.getCustomFields", HashMap::new())?;
        Ok(wrapper.customfields.unwrap_or_default())
    }

    pub fn kb_list(&self) -> Result<Vec<KBBook>> {
        #[derive(Deserialize)]
        struct BooksWrapper {
            book: Option<Vec<KBBook>>,
        }

        let wrapper: BooksWrapper = self.do_request("kb.list", HashMap::new())?;
        Ok(wrapper.book.unwrap_or_default())
    }

    pub fn kb_get(&self, x_book: &str) -> Result<KBBook> {
        let mut params = HashMap::new();
        params.insert("xBook".to_string(), x_book.to_string());

        #[derive(Deserialize)]
        struct BookWrapper {
            book: Option<KBBook>,
        }

        let wrapper: BookWrapper = self.do_request("kb.get", params)?;
        wrapper.book.ok_or_else(|| Error::ApiError {
            id: 1,
            description: "Missing book in response".to_string(),
        })
    }

    pub fn kb_get_page(&self, x_page: &str) -> Result<KBPage> {
        let mut params = HashMap::new();
        params.insert("xKBPage".to_string(), x_page.to_string());

        #[derive(Deserialize)]
        struct PageWrapper {
            page: Option<KBPage>,
        }

        let wrapper: PageWrapper = self.do_request("kb.getPage", params)?;
        wrapper.page.ok_or_else(|| Error::ApiError {
            id: 1,
            description: "Missing page in response".to_string(),
        })
    }

    pub fn kb_search(&self, query: &str) -> Result<Vec<KBPage>> {
        let mut params = HashMap::new();
        params.insert("search".to_string(), query.to_string());

        #[derive(Deserialize)]
        struct SearchWrapper {
            page: Option<Vec<KBPage>>,
        }

        let wrapper: SearchWrapper = self.do_request("kb.search", params)?;
        Ok(wrapper.page.unwrap_or_default())
    }

    pub fn kb_get_book_toc(&self, x_book: &str) -> Result<KBBook> {
        let mut params = HashMap::new();
        params.insert("xBook".to_string(), x_book.to_string());

        #[derive(Deserialize)]
        struct BookWrapper {
            book: Option<KBBook>,
        }

        let wrapper: BookWrapper = self.do_request("kb.getBookTOC", params)?;
        wrapper.book.ok_or_else(|| Error::ApiError {
            id: 1,
            description: "Missing book in response".to_string(),
        })
    }

    pub fn forum_list(&self) -> Result<Vec<Forum>> {
        #[derive(Deserialize)]
        struct ForumsWrapper {
            forums: Option<Vec<Forum>>,
        }

        let wrapper: ForumsWrapper = self.do_request("forums.list", HashMap::new())?;
        Ok(wrapper.forums.unwrap_or_default())
    }

    pub fn forum_get(&self, x_forum: &str) -> Result<Forum> {
        let mut params = HashMap::new();
        params.insert("xForum".to_string(), x_forum.to_string());

        #[derive(Deserialize)]
        struct ForumWrapper {
            forum: Option<Forum>,
        }

        let wrapper: ForumWrapper = self.do_request("forums.get", params)?;
        wrapper.forum.ok_or_else(|| Error::ApiError {
            id: 1,
            description: "Missing forum in response".to_string(),
        })
    }

    pub fn forum_get_topics(&self, x_forum: &str) -> Result<Vec<Topic>> {
        let mut params = HashMap::new();
        params.insert("xForum".to_string(), x_forum.to_string());

        #[derive(Deserialize)]
        struct TopicsWrapper {
            topics: Option<Vec<Topic>>,
        }

        let wrapper: TopicsWrapper = self.do_request("forums.getTopics", params)?;
        Ok(wrapper.topics.unwrap_or_default())
    }

    pub fn forum_get_posts(&self, x_topic: &str) -> Result<Vec<Post>> {
        let mut params = HashMap::new();
        params.insert("xTopic".to_string(), x_topic.to_string());

        #[derive(Deserialize)]
        struct PostsWrapper {
            posts: Option<Vec<Post>>,
        }

        let wrapper: PostsWrapper = self.do_request("forums.getPosts", params)?;
        Ok(wrapper.posts.unwrap_or_default())
    }

    pub fn get_field_labels(&self) -> Result<serde_json::Value> {
        #[derive(Deserialize)]
        struct FieldLabelsWrapper {
            field_labels: Option<serde_json::Value>,
        }

        let wrapper: FieldLabelsWrapper = self.do_request("util.getFieldLabels", HashMap::new())?;
        Ok(wrapper.field_labels.unwrap_or(serde_json::Value::Null))
    }

    pub fn private_get_request(&self, x_request: &str) -> Result<Request> {
        let mut params = HashMap::new();
        params.insert("xRequest".to_string(), x_request.to_string());

        #[derive(Deserialize)]
        struct RequestWrapper {
            request: Option<Request>,
        }

        let wrapper: RequestWrapper = self.do_request("private.request.get", params)?;
        wrapper.request.ok_or_else(|| Error::ApiError {
            id: 1,
            description: "Missing request in response".to_string(),
        })
    }

    pub fn private_search_requests(&self, params: HashMap<String, String>) -> Result<Vec<Request>> {
        #[derive(Deserialize)]
        struct RequestsWrapper {
            #[serde(rename = "request")]
            requests: Option<Vec<Request>>,
        }

        let wrapper: RequestsWrapper = self.do_request("private.request.search", params)?;
        Ok(wrapper.requests.unwrap_or_default())
    }

    pub fn private_get_categories(&self) -> Result<Vec<Category>> {
        #[derive(Deserialize)]
        struct CategoriesWrapper {
            categories: Option<Vec<Category>>,
        }

        let wrapper: CategoriesWrapper =
            self.do_request("private.request.getCategories", HashMap::new())?;
        Ok(wrapper.categories.unwrap_or_default())
    }

    pub fn private_get_custom_fields(&self) -> Result<Vec<CustomField>> {
        #[derive(Deserialize)]
        struct CustomFieldsWrapper {
            customfields: Option<Vec<CustomField>>,
        }

        let wrapper: CustomFieldsWrapper =
            self.do_request("private.request.getCustomFields", HashMap::new())?;
        Ok(wrapper.customfields.unwrap_or_default())
    }

    pub fn private_get_mailboxes(&self) -> Result<Vec<Mailbox>> {
        #[derive(Deserialize)]
        struct MailboxesWrapper {
            mailboxes: Option<Vec<Mailbox>>,
        }

        let wrapper: MailboxesWrapper =
            self.do_request("private.request.getMailboxes", HashMap::new())?;
        Ok(wrapper.mailboxes.unwrap_or_default())
    }

    pub fn private_get_status_types(&self) -> Result<Vec<StatusType>> {
        #[derive(Deserialize)]
        struct StatusTypesWrapper {
            status_types: Option<Vec<StatusType>>,
        }

        let wrapper: StatusTypesWrapper =
            self.do_request("private.request.getStatusTypes", HashMap::new())?;
        Ok(wrapper.status_types.unwrap_or_default())
    }

    pub fn private_get_filters(&self) -> Result<Vec<Filter>> {
        #[derive(Deserialize)]
        struct FiltersWrapper {
            filters: Option<Vec<Filter>>,
        }

        let wrapper: FiltersWrapper = self.do_request("private.filter.get", HashMap::new())?;
        Ok(wrapper.filters.unwrap_or_default())
    }

    pub fn private_get_filter_stream(&self, x_filter: &str) -> Result<Vec<Request>> {
        let mut params = HashMap::new();
        params.insert("xFilter".to_string(), x_filter.to_string());

        #[derive(Deserialize)]
        struct RequestsWrapper {
            requests: Option<Vec<Request>>,
        }

        let wrapper: RequestsWrapper = self.do_request("private.filter.getStream", params)?;
        Ok(wrapper.requests.unwrap_or_default())
    }

    pub fn private_get_active_staff(&self) -> Result<Vec<Staff>> {
        #[derive(Deserialize)]
        struct StaffWrapper {
            active_staff: Option<Vec<Staff>>,
        }

        let wrapper: StaffWrapper =
            self.do_request("private.util.getActiveStaff", HashMap::new())?;
        Ok(wrapper.active_staff.unwrap_or_default())
    }

    pub fn private_get_preferences(&self) -> Result<serde_json::Value> {
        #[derive(Deserialize)]
        struct PreferencesWrapper {
            preferences: Option<serde_json::Value>,
        }

        let wrapper: PreferencesWrapper =
            self.do_request("private.user.preferences", HashMap::new())?;
        Ok(wrapper.preferences.unwrap_or(serde_json::Value::Null))
    }
}
