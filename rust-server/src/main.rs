use std::net::TcpListener;
use mongodb:: {
    bson::{Document, doc},
    Client,
    Collection,
};
mod server;
mod handlers;
mod models;
mod utils;
mod db;

#[tokio::main]
async fn main() {

    let database = db::init_db().await;

    let listener = TcpListener::bind("0.0.0.0:8000").expect("Failed to bind address");

    println!("SIEM Ingestion Server running on 127.0.0.1:8000");

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                let db = database.clone();
                
                tokio::spawn(async move{
                    server::handle_connection(stream, db).await;
                });
            }
            Err(e) => eprintln!("Connection failed: {}", e),
        }
    }
}
