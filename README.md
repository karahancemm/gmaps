# Google Maps Scraper

Google Maps Scraper is a desktop GUI tool built with Python and Tkinter. It allows users to fetch and export public Google Maps reviews by simply entering a **Place ID** and choosing where to save the resulting **CSV file**.

---

## Features

- User-friendly GUI — no need to use the terminal
- Scrapes public Google Maps reviews using Selenium and undetected-chromedriver
- Outputs CSV files containing usernames and review content

---

## Example Output

Here’s a sample of what your CSV file will look like:

```csv
"user_name","user_review"
"Alice","Great atmosphere and friendly staff."
"Bob","Coffee was excellent, highly recommend!"
```

---

## Installation (For Python Users)

This project uses [Poetry](https://python-poetry.org/) for dependency management. You’ll need:

- Python 3.10 (recommended)
- Poetry installed: `pip install poetry` or follow the guide at [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/gmaps-scraper.git
cd gmaps-scraper
```

### 2. Install dependencies
```bash
poetry install
```

### 3. Launch the GUI
```bash
poetry run python src/gmaps/gmaps_gui_main.py
```

---

## Known Limitations

- Currently works on macOS and requires Chrome.
- Requires a valid Google Maps **Place ID** (future versions will support place name search).

---

## License

MIT License.

---

## Coming Soon

We are planning to add:
- Search by place name and city (instead of requiring Place ID)
- .app and .dmg packaging for easier macOS installation
- Windows support

---

**Author:** Cem Karahan  
**Project Status:** In active development
