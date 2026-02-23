use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    pub base_url: String,
    pub username: Option<String>,
    pub password: Option<String>,
    pub api_key: Option<String>,
    pub timeout: u64,
    pub output: String,
    pub columns: Option<String>,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            base_url: String::new(),
            username: None,
            password: None,
            api_key: None,
            timeout: 30,
            output: "json".to_string(),
            columns: None,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VersionResponse {
    pub version: String,
    #[serde(rename = "min_version")]
    pub min_version: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ErrorResponse {
    pub errors: Vec<ErrorItem>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ErrorItem {
    pub id: i32,
    pub description: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Request {
    #[serde(rename = "xRequest")]
    pub x_request: Option<String>,
    #[serde(rename = "accesskey")]
    pub access_key: Option<String>,
    #[serde(rename = "sTitle")]
    pub title: Option<String>,
    #[serde(rename = "tNote")]
    pub note: Option<String>,
    #[serde(rename = "sFirstName")]
    pub first_name: Option<String>,
    #[serde(rename = "sLastName")]
    pub last_name: Option<String>,
    #[serde(rename = "sEmail")]
    pub email: Option<String>,
    #[serde(rename = "sPhone")]
    pub phone: Option<String>,
    #[serde(rename = "sUserId")]
    pub user_id: Option<String>,
    #[serde(rename = "sCategory")]
    pub category: Option<String>,
    #[serde(rename = "xCategory")]
    pub x_category: Option<String>,
    #[serde(rename = "sStatus")]
    pub status: Option<String>,
    #[serde(rename = "xStatus")]
    pub x_status: Option<String>,
    #[serde(rename = "fUrgent")]
    pub urgent: Option<String>,
    #[serde(rename = "fOpen")]
    pub open: Option<String>,
    #[serde(rename = "xPersonAssignedTo")]
    pub person_assigned_to: Option<String>,
    #[serde(rename = "xPersonOpenedBy")]
    pub person_opened_by: Option<String>,
    #[serde(rename = "fullname")]
    pub full_name: Option<String>,
    #[serde(rename = "dtGMTOpened")]
    pub created: Option<String>,
    #[serde(rename = "dtGMTChange")]
    pub updated: Option<String>,
    pub age: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Category {
    #[serde(rename = "xCategory")]
    pub x_category: i32,
    #[serde(rename = "sCategory")]
    pub category: String,
    #[serde(rename = "sCustomFieldList")]
    pub custom_field_list: Option<Vec<i32>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CustomField {
    #[serde(rename = "xCustomField")]
    pub x_custom_field: i32,
    #[serde(rename = "fieldName")]
    pub field_name: String,
    #[serde(rename = "fieldType")]
    pub field_type: String,
    #[serde(rename = "isRequired")]
    pub is_required: bool,
    #[serde(rename = "sTxtSize")]
    pub text_size: Option<String>,
    #[serde(rename = "lrgTextRows")]
    pub large_text_rows: Option<String>,
    #[serde(rename = "listItems")]
    pub list_items: Option<Vec<String>>,
    #[serde(rename = "iDecimalPlaces")]
    pub decimal_places: Option<i32>,
    #[serde(rename = "sRegex")]
    pub regex: Option<String>,
    #[serde(rename = "isAlwaysVisible")]
    pub always_visible: Option<bool>,
    #[serde(rename = "iOrder")]
    pub order: Option<i32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KBBook {
    #[serde(rename = "xBook")]
    pub x_book: String,
    #[serde(rename = "sBookName")]
    pub title: String,
    pub pages: Option<Vec<KBPage>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KBPage {
    #[serde(rename = "xKBPage")]
    pub x_kb_page: i32,
    #[serde(rename = "xKBBook")]
    pub x_kb_book: i32,
    #[serde(rename = "sTitle")]
    pub title: String,
    #[serde(rename = "tContent")]
    pub content: Option<String>,
    #[serde(rename = "iPageOrder")]
    pub page_order: Option<i32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Forum {
    #[serde(rename = "xForum")]
    pub x_forum: i32,
    #[serde(rename = "sTitle")]
    pub title: String,
    #[serde(rename = "iTopics")]
    pub topics: i32,
    #[serde(rename = "iPosts")]
    pub posts: i32,
    #[serde(rename = "dtGMTLastPost")]
    pub last_post: Option<i32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Topic {
    #[serde(rename = "xTopic")]
    pub x_topic: i32,
    #[serde(rename = "xForum")]
    pub x_forum: i32,
    #[serde(rename = "sTitle")]
    pub title: String,
    #[serde(rename = "sAuthor")]
    pub author: String,
    #[serde(rename = "iPosts")]
    pub posts: i32,
    #[serde(rename = "iViews")]
    pub views: i32,
    #[serde(rename = "dtGMTLastPost")]
    pub last_post: Option<i32>,
    #[serde(rename = "fSticky")]
    pub sticky: Option<bool>,
    #[serde(rename = "fLocked")]
    pub locked: Option<bool>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Post {
    #[serde(rename = "xPost")]
    pub x_post: i32,
    #[serde(rename = "xTopic")]
    pub x_topic: i32,
    #[serde(rename = "tPost")]
    pub content: String,
    #[serde(rename = "sAuthor")]
    pub author: String,
    #[serde(rename = "dtGMTCreated")]
    pub created: Option<i32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Mailbox {
    #[serde(rename = "xMailbox")]
    pub x_mailbox: i32,
    #[serde(rename = "sName")]
    pub name: String,
    #[serde(rename = "sEmail")]
    pub email: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StatusType {
    #[serde(rename = "xStatus")]
    pub x_status: i32,
    #[serde(rename = "sStatus")]
    pub status: String,
    #[serde(rename = "fOpen")]
    pub is_open: bool,
    #[serde(rename = "iOrder")]
    pub order: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Staff {
    #[serde(rename = "xPerson")]
    pub x_person: i32,
    #[serde(rename = "sName")]
    pub name: String,
    #[serde(rename = "sEmail")]
    pub email: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Filter {
    #[serde(rename = "xFilter")]
    pub x_filter: i32,
    #[serde(rename = "sName")]
    pub name: String,
    #[serde(rename = "sColumns")]
    pub columns: Option<String>,
    #[serde(rename = "sQuery")]
    pub query: Option<String>,
    #[serde(rename = "fPublic")]
    pub public: bool,
    #[serde(rename = "xUser")]
    pub user_id: Option<i32>,
}

#[derive(Debug, Deserialize)]
pub struct Response {
    #[serde(default)]
    pub version: Option<VersionResponse>,
    #[serde(default)]
    pub requests: Option<Vec<Request>>,
    #[serde(default)]
    pub request: Option<Request>,
    #[serde(default)]
    pub categories: Option<Vec<Category>>,
    #[serde(default)]
    pub customfields: Option<Vec<CustomField>>,
    #[serde(default)]
    pub book: Option<KBBook>,
    #[serde(default)]
    pub page: Option<KBPage>,
    #[serde(default)]
    pub forums: Option<Vec<Forum>>,
    #[serde(default)]
    pub forum: Option<Forum>,
    #[serde(default)]
    pub topics: Option<Vec<Topic>>,
    #[serde(default)]
    pub topic: Option<Topic>,
    #[serde(default)]
    pub posts: Option<Vec<Post>>,
    #[serde(default)]
    pub mailboxes: Option<Vec<Mailbox>>,
    #[serde(default)]
    pub status_types: Option<Vec<StatusType>>,
    #[serde(default)]
    pub active_staff: Option<Vec<Staff>>,
    #[serde(default)]
    pub filters: Option<Vec<Filter>>,
    #[serde(default)]
    pub column_names: Option<Vec<String>>,
    #[serde(default)]
    pub preferences: Option<serde_json::Value>,
    #[serde(default)]
    pub field_labels: Option<serde_json::Value>,
    #[serde(default)]
    pub errors: Option<Vec<ErrorItem>>,
}
