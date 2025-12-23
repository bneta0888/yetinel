use std::io::{Read};
use std::net::TcpStream;


use crate::models::LogEvent;
// use crate::handlers::handle_logs;
use crate::utils::http_response;
use mongodb::Database;


pub async fn handle_connection(mut stream: TcpStream, db: Database) {
    let mut buffer = [0; 4096];
    let _ = stream.read(&mut buffer);

    let request = String::from_utf8_lossy(&buffer);

    if request.starts_with("POST /logs") {
        let body = request
            .split("\r\n\r\n")
            .nth(1)
            .unwrap_or("")
            .trim_matches(char::from(0));
       
        let log: LogEvent = match serde_json::from_str(body) {
            Ok(log) => log,
            Err(_) => {
                http_response(&mut stream, "400 Bad Request", "Invalid JSON");
                return;
            }
        };

        println!("Parsed log: {:?}", log);

        let collection = db.collection::<LogEvent>("logs");

        if let Err(e) = collection.insert_one(&log, None).await {
            eprintln!("Mongo insert failed: {}", e);
            http_response(&mut stream, "500 Internal Server Error", "DB error");
            return;
        }

        println!("Log stored in MongoDB");
        
        http_response(&mut stream, "200 OK", "Log received");

    } else {
        http_response(&mut stream, "404 Not Found", "Not Found");
    }

}
