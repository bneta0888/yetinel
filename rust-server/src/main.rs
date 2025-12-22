use std::net::TcpListener;

mod server;
mod handlers;
mod models;
mod utils;

fn main() {
    let listener = TcpListener::bind("0.0.0.0:8000").expect("Failed to bind address");

    println!("SIEM Ingestion Server running on 127.0.0.1:8000");

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                server::handle_connection(stream);
            }
            Err(e) => eprintln!("Connection failed: {}", e),
        }
    }
}
