# PopMart Web Scraper

A Selenium-based web scraper for automating interactions with the PopMart website. This tool helps automate the process of finding and clicking specific box items on the PopMart website.

## Features

- Automated box item detection and clicking
- Cookie consent handling
- SSL certificate error handling
- Multiple URL variation attempts
- Sound feedback for successful/unsuccessful actions
- Detailed logging
- Pagination support

## Prerequisites

- Python 3.x
- Chrome browser
- macOS Command Line Tools (Xcode)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/schia00/popmart-scraper.git
   cd popmart-scraper
   ```

2. Install Command Line Tools (if not already installed):
   ```bash
   xcode-select --install
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Activate the virtual environment if not already activated:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Run the scraper:
   ```bash
   python scraper.py
   ```

The script will:
- Prompt for a URL (or use the default)
- Handle cookie consent automatically
- Try to find and click box items on the page
- Navigate through multiple URL variations
- Provide audio feedback for successful/unsuccessful actions
- Log all actions and results

## Configuration

The following constants can be modified in `scraper.py`:

- `MAIN_URL`: Base URL for the PopMart website
- `VAR_URL`: Starting URL variation number (incremented by 10)
- `END_URL`: Ending URL component
- `max_attempts_per_page`: Maximum number of click attempts per page (default: 3)
- `max_url_attempts`: Maximum number of URL variations to try (default: 5)

## Error Handling

The script includes comprehensive error handling for:
- SSL certificate errors
- Network connectivity issues
- Element detection failures
- Click interaction failures
- Page navigation errors

## Logging

The script logs all actions and results to the console with timestamps, including:
- Page navigation events
- Box item detection
- Click attempts and results
- Error messages and stack traces

## Project Structure

- `scraper.py`: Main script containing the web scraping logic
- `requirements.txt`: Project dependencies
- `.gitignore`: Git ignore file
- `README.md`: Project documentation
