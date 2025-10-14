# Hello Httpy

A tiny HTTP server written in Python for learning purposes. It focuses on understanding sockets, request parsing, simple routing, and serving static files. Not production-ready.

## Features
- Minimal HTTP/1.1 implementation (GET/POST)
- Simple router and middleware-style flow
- Static file serving from a public directory
- Basic logging and error handling
- Health and echo demo endpoints
- No external dependencies (intended), unless noted in requirements.txt

## Quick start
- Can only communicate with raw data such as telnet

## Demo endpoints
- None

## Configuration
- None

## Project structure
- server.py           entry point

## Development (Future)
- Lint/test: ruff/flake8, pytest or unittest
- Run tests: pytest or python -m unittest

## Notes
- Educational project.
- Do not expose to the public Internet.

## Roadmap
- Learn How HTTP Http is different from other type of communication
- Basic Working HTTP Server 
- Proper error handling and graceful shutdown
- Handle MIME type and such

## Milestones
- Basic socket communication working with TCP (14/10/2025)