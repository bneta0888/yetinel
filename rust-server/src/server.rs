use std::io::{Read};
use std::net::TcpStream;

use crate::handlers::handle_logs;
use crate::utils::http_response;

pub fn handle_connection(mut stream: TcpStream) {
    let mut buffer = [0; 4096];
    let _ = stream.read(&mut buffer);

    let request = String::from_utf8_lossy(&buffer);

    if request.starts_with("POST /logs") {
        let body = request
            .split("\r\n\r\n")
            .nth(1)
            .unwrap_or("")
            .trim_matches(char::from(0));

        handle_logs(body, &mut stream);
    } else {
        http_response(&mut stream, "404 Not Found", "Not Found");
    }
}
