use crate::models::LogEvent;
use crate::utils::http_response;
use serde_json;
use std::net::TcpStream;

pub fn handle_logs(body: &str, stream: &mut TcpStream) {
    match serde_json::from_str::<LogEvent>(body) {
        Ok(log) => {
            println!("Log received: {:?}", log);
            http_response(stream, "200 OK", "Log received");
        }
        Err(_) => {
            http_response(stream, "400 Bad Request", "Invalid JSON");
        }
    }
}
