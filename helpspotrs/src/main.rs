use clap::{Parser, Subcommand};
use helpspotrs::client::{Config, HelpSpotClient};
use helpspotrs::config::{load_config_file, save_config_file, ConfigFile};
use helpspotrs::errors::Result;
use helpspotrs::output::{
    print_as_table, print_categories_table, print_forums_table, print_requests_table,
    print_topics_table,
};
use serde_json::Value;
use std::collections::HashMap;
use std::io::{self, Write};

#[derive(Parser)]
#[command(name = "helpspot")]
#[command(about = "HelpSpot CLI - HelpDesk API Client", long_about = None)]
struct Cli {
    #[arg(long)]
    base_url: Option<String>,

    #[arg(long)]
    username: Option<String>,

    #[arg(long)]
    password: Option<String>,

    #[arg(long)]
    api_key: Option<String>,

    #[arg(long, default_value = "json")]
    output: String,

    #[arg(long)]
    columns: Option<String>,

    #[arg(long)]
    debug: bool,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Config {
        #[command(subcommand)]
        action: ConfigAction,
    },
    Version,
    Request {
        #[command(subcommand)]
        action: RequestAction,
    },
    Category {
        #[command(subcommand)]
        action: CategoryAction,
    },
    CustomField {
        #[command(subcommand)]
        action: CustomFieldAction,
    },
    Kb {
        #[command(subcommand)]
        action: KbAction,
    },
    Forum {
        #[command(subcommand)]
        action: ForumAction,
    },
    FieldLabels,
}

#[derive(Subcommand)]
enum ConfigAction {
    Init,
    Show,
}

#[derive(Subcommand)]
enum RequestAction {
    Create {
        #[arg(long)]
        note: Option<String>,

        #[arg(long)]
        email: Option<String>,

        #[arg(long)]
        first_name: Option<String>,

        #[arg(long)]
        last_name: Option<String>,

        #[arg(long)]
        category: Option<String>,

        #[arg(long)]
        title: Option<String>,
    },
    Get {
        access_key: String,
    },
    GetId {
        id: String,
    },
    Update {
        #[arg(long)]
        id: Option<String>,

        #[arg(long)]
        access_key: Option<String>,

        #[arg(long)]
        note: Option<String>,
    },
    List {
        #[arg(long)]
        search: Option<String>,

        #[arg(long)]
        filter: Option<String>,

        #[arg(long)]
        limit: Option<usize>,
    },
}

#[derive(Subcommand)]
enum CategoryAction {
    List,
}

#[derive(Subcommand)]
enum CustomFieldAction {
    List,
}

#[derive(Subcommand)]
enum KbAction {
    List,
    Get { id: String },
    Toc { id: String },
    Page { id: String },
    Search { query: String },
}

#[derive(Subcommand)]
enum ForumAction {
    List,
    Get { id: String },
    Topics { forum_id: String },
    Posts { topic_id: String },
}

fn build_client_from_args(args: &Cli) -> Result<Option<HelpSpotClient>> {
    let mut config = Config::default();

    if let Ok(Some(config_file)) = load_config_file() {
        config.base_url = config_file.base_url.clone();
        config.username = config_file.username.clone();
        config.password = config_file.password.clone();
        config.api_key = config_file.api_key.clone();
        config.output = config_file.output.unwrap_or_else(|| "json".to_string());
    }

    if let Some(base_url) = &args.base_url {
        config.base_url = base_url.clone();
    }
    if let Some(username) = &args.username {
        config.username = Some(username.clone());
    }
    if let Some(password) = &args.password {
        config.password = Some(password.clone());
    }
    if let Some(api_key) = &args.api_key {
        config.api_key = Some(api_key.clone());
    }
    config.output = args.output.clone();
    config.columns = args.columns.clone();
    config.debug = args.debug;

    if config.base_url.is_empty() {
        return Ok(None);
    }

    Ok(Some(HelpSpotClient::new(config)?))
}

fn output_data(output_format: &str, data: &Value) {
    match output_format {
        "table" => {
            let table = print_as_table(data);
            println!("{}", table);
        }
        _ => {
            println!("{}", serde_json::to_string_pretty(data).unwrap_or_default());
        }
    }
}

fn run() -> Result<()> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Config { action } => match action {
            ConfigAction::Init => {
                println!("Initializing config...");
                let mut config = ConfigFile::default();

                print!("Base URL: ");
                io::stdout().flush()?;
                let mut input = String::new();
                io::stdin().read_line(&mut input)?;
                config.base_url = input.trim().to_string();

                print!("Username (optional): ");
                io::stdout().flush()?;
                input.clear();
                io::stdin().read_line(&mut input)?;
                let username = input.trim().to_string();
                if !username.is_empty() {
                    config.username = Some(username);
                }

                print!("Password (optional): ");
                io::stdout().flush()?;
                input.clear();
                io::stdin().read_line(&mut input)?;
                let password = input.trim().to_string();
                if !password.is_empty() {
                    config.password = Some(password);
                }

                print!("API Key (optional): ");
                io::stdout().flush()?;
                input.clear();
                io::stdin().read_line(&mut input)?;
                let api_key = input.trim().to_string();
                if !api_key.is_empty() {
                    config.api_key = Some(api_key);
                }

                save_config_file(&config)?;
                println!("Config saved successfully.");
            }
            ConfigAction::Show => {
                if let Some(config) = load_config_file()? {
                    println!("{}", serde_json::to_string_pretty(&config)?);
                } else {
                    println!("No config file found.");
                }
            }
        },

        Commands::Version => {
            let client = build_client_from_args(&cli)?;
            if let Some(client) = client {
                let version = client.get_version()?;
                println!("{}", serde_json::to_string(&version)?);
            } else {
                println!("Error: base_url not configured");
            }
        }

        Commands::FieldLabels => {
            let client = build_client_from_args(&cli)?;
            if let Some(client) = client {
                let labels = client.get_field_labels()?;
                println!("{}", serde_json::to_string(&labels)?);
            } else {
                println!("Error: base_url not configured");
            }
        }

        Commands::Request { action } => {
            let client = build_client_from_args(&cli)?;
            if let Some(client) = client {
                match action {
                    RequestAction::Create {
                        note,
                        email,
                        first_name,
                        last_name,
                        category,
                        title,
                    } => {
                        let mut params = HashMap::new();
                        if let Some(v) = note {
                            params.insert("tNote".to_string(), v.clone());
                        }
                        if let Some(v) = email {
                            params.insert("sEmail".to_string(), v.clone());
                        }
                        if let Some(v) = first_name {
                            params.insert("sFirstName".to_string(), v.clone());
                        }
                        if let Some(v) = last_name {
                            params.insert("sLastName".to_string(), v.clone());
                        }
                        if let Some(v) = category {
                            params.insert("xCategory".to_string(), v.clone());
                        }
                        if let Some(v) = title {
                            params.insert("sTitle".to_string(), v.clone());
                        }

                        let request = client.create_request(params)?;
                        println!("{}", serde_json::to_string(&request)?);
                    }
                    RequestAction::Get { access_key } => {
                        let request = client.get_request(access_key)?;
                        println!("{}", serde_json::to_string(&request)?);
                    }
                    RequestAction::GetId { id } => {
                        let request = client.private_get_request(id)?;
                        println!("{}", serde_json::to_string(&request)?);
                    }
                    RequestAction::Update {
                        id,
                        access_key,
                        note,
                    } => {
                        let mut params = HashMap::new();
                        if let Some(v) = id {
                            params.insert("xRequest".to_string(), v.clone());
                        }
                        if let Some(v) = access_key {
                            params.insert("accesskey".to_string(), v.clone());
                        }
                        if let Some(v) = note {
                            params.insert("tNote".to_string(), v.clone());
                        }

                        let request = client.update_request(params)?;
                        println!("{}", serde_json::to_string(&request)?);
                    }
                    RequestAction::List {
                        search,
                        filter,
                        limit,
                    } => {
                        let mut params = HashMap::new();
                        if let Some(v) = search {
                            params.insert("search".to_string(), v.clone());
                        }
                        if let Some(v) = filter {
                            params.insert("xFilter".to_string(), v.clone());
                        }
                        if let Some(v) = limit {
                            params.insert("limit".to_string(), v.to_string());
                        }

                        let requests = client.private_search_requests(params)?;
                        let output_format = cli.output.as_str();
                        if output_format == "table" {
                            let json_reqs: Vec<Value> = requests
                                .iter()
                                .map(|r| serde_json::to_value(r).unwrap_or(Value::Null))
                                .collect();
                            println!("{}", print_requests_table(&json_reqs));
                        } else {
                            println!("{}", serde_json::to_string(&requests)?);
                        }
                    }
                }
            } else {
                println!("Error: base_url not configured");
            }
        }

        Commands::Category { action } => {
            let client = build_client_from_args(&cli)?;
            if let Some(client) = client {
                match action {
                    CategoryAction::List => {
                        let categories = client.get_categories()?;
                        let output_format = cli.output.as_str();
                        if output_format == "table" {
                            let json_cats: Vec<Value> = categories
                                .iter()
                                .map(|c| serde_json::to_value(c).unwrap_or(Value::Null))
                                .collect();
                            println!("{}", print_categories_table(&json_cats));
                        } else {
                            println!("{}", serde_json::to_string(&categories)?);
                        }
                    }
                }
            } else {
                println!("Error: base_url not configured");
            }
        }

        Commands::CustomField { action } => {
            let client = build_client_from_args(&cli)?;
            if let Some(client) = client {
                match action {
                    CustomFieldAction::List => {
                        let fields = client.private_get_custom_fields()?;
                        println!("{}", serde_json::to_string(&fields)?);
                    }
                }
            } else {
                println!("Error: base_url not configured");
            }
        }

        Commands::Kb { action } => {
            let client = build_client_from_args(&cli)?;
            if let Some(client) = client {
                match action {
                    KbAction::List => {
                        let books = client.kb_list()?;
                        println!("{}", serde_json::to_string(&books)?);
                    }
                    KbAction::Get { id } => {
                        let book = client.kb_get(id)?;
                        println!("{}", serde_json::to_string(&book)?);
                    }
                    KbAction::Toc { id } => {
                        let book = client.kb_get_book_toc(id)?;
                        println!("{}", serde_json::to_string(&book)?);
                    }
                    KbAction::Page { id } => {
                        let page = client.kb_get_page(id)?;
                        println!("{}", serde_json::to_string(&page)?);
                    }
                    KbAction::Search { query } => {
                        let results = client.kb_search(query)?;
                        println!("{}", serde_json::to_string(&results)?);
                    }
                }
            } else {
                println!("Error: base_url not configured");
            }
        }

        Commands::Forum { action } => {
            let client = build_client_from_args(&cli)?;
            if let Some(client) = client {
                match action {
                    ForumAction::List => {
                        let forums = client.forum_list()?;
                        let output_format = cli.output.as_str();
                        if output_format == "table" {
                            let json_forums: Vec<Value> = forums
                                .iter()
                                .map(|f| serde_json::to_value(f).unwrap_or(Value::Null))
                                .collect();
                            println!("{}", print_forums_table(&json_forums));
                        } else {
                            println!("{}", serde_json::to_string(&forums)?);
                        }
                    }
                    ForumAction::Get { id } => {
                        let forum = client.forum_get(id)?;
                        println!("{}", serde_json::to_string(&forum)?);
                    }
                    ForumAction::Topics { forum_id } => {
                        let topics = client.forum_get_topics(forum_id)?;
                        let output_format = cli.output.as_str();
                        if output_format == "table" {
                            let json_topics: Vec<Value> = topics
                                .iter()
                                .map(|t| serde_json::to_value(t).unwrap_or(Value::Null))
                                .collect();
                            println!("{}", print_topics_table(&json_topics));
                        } else {
                            println!("{}", serde_json::to_string(&topics)?);
                        }
                    }
                    ForumAction::Posts { topic_id } => {
                        let posts = client.forum_get_posts(topic_id)?;
                        println!("{}", serde_json::to_string(&posts)?);
                    }
                }
            } else {
                println!("Error: base_url not configured");
            }
        }
    }

    Ok(())
}

fn main() {
    if let Err(e) = run() {
        eprintln!("Error: {}", e);
        std::process::exit(1);
    }
}
