# Web Scraping with Selenium

This project is a web scraping application built with Python and Selenium.

## Prerequisites

- Python 3.x
- Chrome browser installed
- macOS Command Line Tools (Xcode)

## Setup

1. Install Command Line Tools (Xcode) by running:
   ```
   xcode-select --install
   ```

2. Create and activate virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the scraper:
```
python scraper.py
```

## Project Structure

- `scraper.py`: Main script containing the web scraping logic
- `requirements.txt`: Project dependencies
- `.vscode/`: VS Code configuration files

## Customization

To modify the scraping behavior, edit the `scraper.py` file and update the scraping logic in the `main()` function.
