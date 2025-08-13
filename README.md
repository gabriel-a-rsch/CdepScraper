# CdepScraper

CdepScraper is a Python library focused on extracting and processing legislative bill information from HTML pages retrieved from cdep.ro’s “Urmarire legislativa” (Legislative follow-up) section. The primary goal is to accurately interpret and structure bill data for downstream analysis, rather than crawling or scraping at scale.

## Features

- **HTML Data Processing:** Extracts bill number, title, and basic metadata from individual legislative bill pages.
- **Modular API:** Use via the [`PLXRepository`](cdep_scraping/PLXRepository.py) class for structured workflows.
- **Planned Outputs:** JSON, CSV, and SQLite database entries.
- **Extensible:** Designed to support bill timeline analysis and attachment support in future releases.
- **MIT Licensed:** Open and free to use with attribution.

## Installation

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

Then import the library in your Python project.

## Usage

The main API is built around the `PLXRepository` class. Example usage:

```python
from cdep_scraping.PLXRepository import PLXRepository

repo = PLXRepository("mySQLiteFile.db")  # Optional: specify DB file for persistence

# Add bill data from HTML string
repo.addPLXFromHTMLString(myHTMLFileHere)

# Save repository data to JSON file
repo.saveToJSON(myPath)

# Remove a bill by its number
repo.removeByPLXNumber(myPLXNumber)

# Save current state to SQLite DB
repo.saveToDB()
```

> **Note:** The API is under active development. Some functionality (like full bill timeline analysis and attachment handling) is not yet implemented.

## Configuration

No configuration files are required for current versions. This may change as features are added.

## Output Formats

- **JSON**
- **CSV**
- **SQLite** (local .db files)

## Roadmap

- Full bill timeline parsing
- Bill attachment support
- GUI tools for easier data handling

## License

This project is licensed under the MIT License. Please see [LICENSE](LICENSE) for details and attribution requirements.

## Authors & Contributors

- [gabriel-a-rsch](https://github.com/gabriel-a-rsch) (project founder)

## Contact & Support

- For issues or requests, use the [GitHub Issues](https://github.com/gabriel-a-rsch/CdepScraper/issues) page.
- For urgent matters, see the email address on my [GitHub profile](https://github.com/gabriel-a-rsch).

---

_This README is a living document and will be updated as features are added. Contributions and feedback are welcome!_
