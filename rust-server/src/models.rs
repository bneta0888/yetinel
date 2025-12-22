use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct LogEvent {
    pub timestamp: String, 
    pub source: String,
    pub level: String,
    pub event: String,
    pub message: String,
    pub source_ip: String,
}
