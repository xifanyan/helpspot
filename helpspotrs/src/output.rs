use serde::Serialize;
use tabled::{builder::Builder, settings::Style};

pub fn print_as_table<T: Serialize>(data: &T) -> String {
    if let Ok(value) = serde_json::to_value(data) {
        match value {
            serde_json::Value::Array(arr) => {
                if arr.is_empty() {
                    return "No data".to_string();
                }
                if let Some(serde_json::Value::Object(obj)) = arr.first() {
                    let headers: Vec<String> = obj.keys().cloned().collect();
                    let mut rows: Vec<Vec<String>> = Vec::new();

                    for item in arr {
                        if let serde_json::Value::Object(map) = item {
                            let row: Vec<String> = headers
                                .iter()
                                .map(|h| {
                                    map.get(h)
                                        .map(|v| match v {
                                            serde_json::Value::String(s) => s.clone(),
                                            serde_json::Value::Null => String::new(),
                                            other => other.to_string(),
                                        })
                                        .unwrap_or_default()
                                })
                                .collect();
                            rows.push(row);
                        }
                    }

                    let all_rows: Vec<Vec<&str>> = rows
                        .iter()
                        .map(|r| r.iter().map(|s| &s[..]).collect())
                        .collect();

                    let header_refs: Vec<&str> = headers.iter().map(|s| &s[..]).collect();
                    let builder: Builder = std::iter::once(header_refs).chain(all_rows).collect();

                    return builder.build().with(Style::rounded()).to_string();
                }
            }
            serde_json::Value::Object(obj) => {
                let rows: Vec<Vec<String>> = obj
                    .iter()
                    .map(|(key, val)| {
                        let value_str = match val {
                            serde_json::Value::String(s) => s.clone(),
                            serde_json::Value::Null => String::new(),
                            other => other.to_string(),
                        };
                        vec![key.clone(), value_str]
                    })
                    .collect();

                let all_rows: Vec<Vec<&str>> = rows
                    .iter()
                    .map(|r| r.iter().map(|s| &s[..]).collect())
                    .collect();

                let builder: Builder = std::iter::once(vec!["Field", "Value"])
                    .chain(all_rows)
                    .collect();

                return builder.build().with(Style::rounded()).to_string();
            }
            _ => {
                return serde_json::to_string_pretty(data).unwrap_or_default();
            }
        }
    }

    serde_json::to_string_pretty(data).unwrap_or_default()
}

pub fn print_requests_table(requests: &[serde_json::Value]) -> String {
    if requests.is_empty() {
        return "No requests found".to_string();
    }

    let headers = vec!["ID", "Title", "Status", "Created"];

    let mut rows: Vec<Vec<String>> = Vec::new();

    for req in requests {
        if let serde_json::Value::Object(obj) = req {
            let id = obj
                .get("xRequest")
                .map(|v| v.to_string().trim_matches('"').to_string())
                .unwrap_or_default();
            let title = obj
                .get("sTitle")
                .or_else(|| obj.get("Title"))
                .map(|v| match v {
                    serde_json::Value::String(s) => s.clone(),
                    _ => v.to_string(),
                })
                .unwrap_or_default();
            let status = obj
                .get("xStatus")
                .or_else(|| obj.get("sStatus"))
                .or_else(|| obj.get("Status"))
                .map(|v| match v {
                    serde_json::Value::String(s) => s.clone(),
                    _ => v.to_string(),
                })
                .unwrap_or_default();
            let created = obj
                .get("dtGMTOpened")
                .or_else(|| obj.get("Created"))
                .map(|v| match v {
                    serde_json::Value::String(s) => s.clone(),
                    _ => v.to_string(),
                })
                .unwrap_or_default();

            rows.push(vec![id, title, status, created]);
        }
    }

    let all_rows: Vec<Vec<&str>> = rows
        .iter()
        .map(|r| r.iter().map(|s| &s[..]).collect())
        .collect();

    let header_refs: Vec<&str> = headers.iter().map(|s| &s[..]).collect();
    let builder: Builder = std::iter::once(header_refs).chain(all_rows).collect();

    builder.build().with(Style::rounded()).to_string()
}

pub fn print_categories_table(categories: &[serde_json::Value]) -> String {
    if categories.is_empty() {
        return "No categories found".to_string();
    }

    let headers = vec!["xCategory", "Category"];
    let mut rows: Vec<Vec<String>> = Vec::new();

    for cat in categories {
        if let serde_json::Value::Object(obj) = cat {
            let x_category = obj
                .get("xCategory")
                .or_else(|| obj.get("xCategory"))
                .map(|v| v.to_string())
                .unwrap_or_default();
            let category = obj
                .get("sCategory")
                .or_else(|| obj.get("Category"))
                .map(|v| match v {
                    serde_json::Value::String(s) => s.clone(),
                    _ => v.to_string(),
                })
                .unwrap_or_default();
            rows.push(vec![x_category.trim_matches('"').to_string(), category]);
        }
    }

    let all_rows: Vec<Vec<&str>> = rows
        .iter()
        .map(|r| r.iter().map(|s| &s[..]).collect())
        .collect();

    let header_refs: Vec<&str> = headers.iter().map(|s| &s[..]).collect();
    let builder: Builder = std::iter::once(header_refs).chain(all_rows).collect();

    builder.build().with(Style::rounded()).to_string()
}

pub fn print_forums_table(forums: &[serde_json::Value]) -> String {
    if forums.is_empty() {
        return "No forums found".to_string();
    }

    let headers = vec!["xForum", "Title", "Topics", "Posts"];
    let mut rows: Vec<Vec<String>> = Vec::new();

    for forum in forums {
        if let serde_json::Value::Object(obj) = forum {
            let row: Vec<String> = headers
                .iter()
                .map(|h| {
                    let key = String::from(*h);
                    obj.get(&key)
                        .map(|v| match v {
                            serde_json::Value::String(s) => s.clone(),
                            serde_json::Value::Number(n) => n.to_string(),
                            serde_json::Value::Null => String::new(),
                            other => other.to_string(),
                        })
                        .unwrap_or_default()
                })
                .collect();
            rows.push(row);
        }
    }

    let all_rows: Vec<Vec<&str>> = rows
        .iter()
        .map(|r| r.iter().map(|s| &s[..]).collect())
        .collect();

    let header_refs: Vec<&str> = headers.iter().map(|s| &s[..]).collect();
    let builder: Builder = std::iter::once(header_refs).chain(all_rows).collect();

    builder.build().with(Style::rounded()).to_string()
}

pub fn print_topics_table(topics: &[serde_json::Value]) -> String {
    if topics.is_empty() {
        return "No topics found".to_string();
    }

    let headers = vec!["xTopic", "Title", "Author", "Posts", "Views"];
    let mut rows: Vec<Vec<String>> = Vec::new();

    for topic in topics {
        if let serde_json::Value::Object(obj) = topic {
            let row: Vec<String> = headers
                .iter()
                .map(|h| {
                    let key = String::from(*h);
                    obj.get(&key)
                        .map(|v| match v {
                            serde_json::Value::String(s) => s.clone(),
                            serde_json::Value::Number(n) => n.to_string(),
                            serde_json::Value::Null => String::new(),
                            other => other.to_string(),
                        })
                        .unwrap_or_default()
                })
                .collect();
            rows.push(row);
        }
    }

    let all_rows: Vec<Vec<&str>> = rows
        .iter()
        .map(|r| r.iter().map(|s| &s[..]).collect())
        .collect();

    let header_refs: Vec<&str> = headers.iter().map(|s| &s[..]).collect();
    let builder: Builder = std::iter::once(header_refs).chain(all_rows).collect();

    builder.build().with(Style::rounded()).to_string()
}
