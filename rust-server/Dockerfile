# --- Build Stage ---
FROM clux/muslrust:stable as builder

WORKDIR /app

COPY Cargo.toml .
COPY src ./src

# Build static binary for MUSL target
RUN cargo build --release --target x86_64-unknown-linux-musl

# --- Runtime Stage ---
FROM debian:bookworm-slim

WORKDIR /app

# Copy the static binary
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/rust-server .

# Ensure it's executable
RUN chmod +x rust-server

EXPOSE 8000

CMD ["./rust-server"]

