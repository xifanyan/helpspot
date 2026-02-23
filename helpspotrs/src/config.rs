use crate::errors::{Error, Result};
use crate::types::Config;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

const CONFIG_FILE_NAME: &str = "config.json";
const APP_NAME: &str = "helpspot";

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConfigFile {
    #[serde(rename = "base_url")]
    pub base_url: String,
    pub username: Option<String>,
    pub password: Option<String>,
    #[serde(rename = "api_key")]
    pub api_key: Option<String>,
    pub timeout: Option<u64>,
    pub output: Option<String>,
}

impl Default for ConfigFile {
    fn default() -> Self {
        Self {
            base_url: String::new(),
            username: None,
            password: None,
            api_key: None,
            timeout: Some(30),
            output: Some("json".to_string()),
        }
    }
}

impl From<&Config> for ConfigFile {
    fn from(cfg: &Config) -> Self {
        Self {
            base_url: cfg.base_url.clone(),
            username: cfg.username.clone(),
            password: cfg.password.clone(),
            api_key: cfg.api_key.clone(),
            timeout: Some(cfg.timeout),
            output: Some(cfg.output.clone()),
        }
    }
}

impl From<ConfigFile> for Config {
    fn from(cf: ConfigFile) -> Self {
        Self {
            base_url: cf.base_url,
            username: cf.username,
            password: cf.password,
            api_key: cf.api_key,
            timeout: cf.timeout.unwrap_or(30),
            output: cf.output.unwrap_or_else(|| "json".to_string()),
            columns: None,
        }
    }
}

pub fn get_config_dir() -> Result<PathBuf> {
    if let Ok(config_dir) = std::env::var("HELSPOT_CONFIG_DIR") {
        return Ok(PathBuf::from(config_dir));
    }

    let home = dirs::home_dir()
        .ok_or_else(|| Error::ConfigError("Cannot find home directory".to_string()))?;

    Ok(home.join(".config").join(APP_NAME))
}

pub fn get_config_path() -> Result<PathBuf> {
    let config_dir = get_config_dir()?;
    Ok(config_dir.join(CONFIG_FILE_NAME))
}

pub fn load_config_file() -> Result<Option<ConfigFile>> {
    let config_path = get_config_path()?;

    if !config_path.exists() {
        return Ok(None);
    }

    let content = std::fs::read_to_string(&config_path)?;
    let config: ConfigFile = serde_json::from_str(&content)?;
    Ok(Some(config))
}

pub fn save_config_file(config: &ConfigFile) -> Result<()> {
    let config_dir = get_config_dir()?;
    std::fs::create_dir_all(&config_dir)?;

    let config_path = config_dir.join(CONFIG_FILE_NAME);
    let content = serde_json::to_string_pretty(config)?;
    std::fs::write(&config_path, content)?;

    Ok(())
}
