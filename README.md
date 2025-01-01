# RobotTxt.py

**RobotTxt.py** is a Python-based tool for fetching and parsing `robots.txt` files from websites. It extracts `Disallow` and `Allow` paths, checks their accessibility, and returns subdomain-like URLs with their HTTP status codes.

## Features
- Fetch and parse `robots.txt` files.
- Extract `Disallow` and `Allow` paths and construct URLs.
- Display HTTP status codes (e.g., 200, 301) for extracted URLs.
- Support for single or multiple domains.
- Option to follow redirects and filter results by status codes.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/awais0x01/robottxt.py.git
   cd robottxt.py
