use thiserror::Error;

#[derive(Error, Debug)]
pub enum Error {
    #[error("Missing required configuration: base_url")]
    MissingBaseURL,

    #[error("Missing authentication: either api_key or username/password required")]
    MissingAuth,

    #[error("HTTP request failed: {0}")]
    RequestFailed(#[from] reqwest::Error),

    #[error("API error: {id}: {description}")]
    ApiError { id: i32, description: String },

    #[error("Failed to parse response: {0}")]
    ParseError(#[from] serde_json::Error),

    #[error("Config error: {0}")]
    ConfigError(String),

    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}

impl Error {
    pub fn from_api_error(id: i32, description: String) -> Self {
        Error::ApiError { id, description }
    }
}

pub type Result<T> = std::result::Result<T, Error>;
