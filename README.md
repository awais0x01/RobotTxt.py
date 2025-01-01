# robotTxt.py

**robotTxt.py** is a Python-based tool for fetching and parsing `robots.txt` files from websites. It extracts `Disallow` and `Allow` paths, checks their accessibility, and returns subdomain-like URLs with their HTTP status codes.

## Features
- Fetch and parse `robots.txt` files.
- Extract `Disallow` and `Allow` paths and construct URLs.
- Display HTTP status codes (e.g., 200, 301) for extracted URLs.
- Support for single or multiple domains.
- Option to follow redirects and filter results by status codes.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/robotTxt.py.git
   cd robotTxt.py
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Check a single domain

```bash
python3 robotTxt.py -u example.com
```

### Check multiple domains from a file

```bash
python3 robotTxt.py -dl domains.txt
```

### Advanced Options

- **Follow redirects:** `-r`
- **Filter by status codes:** `-mc 200 301`
- **Silent mode:** `--silent`
- **Hide status codes:** `-ns`

## Example

```bash
python3 robotTxt.py -u example.com -r -mc 200
```

## Contributors

- **Awais0x01**  
  - GitHub: [awais0x01](https://github.com/awais0x01)  
  - Twitter: [@awais0x01](https://twitter.com/awais0x01)  
  - Facebook: [awais0x01](https://facebook.com/awais0x01)  
  - LinkedIn: [awais0x01](https://linkedin.com/in/awais0x01)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
