# OntologyScraper

A Python pipeline that scrapes Wikipedia articles on a given topic and extracts taxonomic (is-a) relationships from the text, producing structured statements that can be used as a foundation for building an ontology.

**Example:** Point the scraper at the category `Animals`, and it will pull the relevant Wikipedia articles and extract statements such as:

```
Cat IS-A Mammal
```

## How It Works

The pipeline is split into two independent stages:

1. **Scraping** — Given a topic (mapped to a Wikipedia category), fetch all member pages via the Wikipedia API and save their plain-text content locally in /pages.
2. **NLP Extraction** — Run each page through a spaCy dependency parser, match copula constructions ("X is a Y") and write the resulting `subject IS-A object` pairs to an output file in /patterns.

## Usage

**1. Scrape a topic:**

```bash
python DownloadPages.py Physics
```

This fetches all articles belonging to the corresponding Wikipedia category and saves them as text files under `pages/`.

**2. Run extraction:**

```bash
python NLP.py
```

This parses every file in `pages/` and appends extracted `IS-A` statements to `patterns/pattern.txt`.

## Requirements

- Python 3.12+
- [spaCy](https://spacy.io/) with the `en_core_web_sm` English model
- [wikipedia-api](https://pypi.org/project/Wikipedia-API/)

## Installation

```bash
git clone https://github.com/<your-username>/OntologyScraper.git
cd OntologyScraper

python -m venv OntologyScraperEnv
source OntologyScraperEnv/bin/activate

pip install wikipedia-api
pip install spacy
python -m spacy download en_core_web_sm
```

## Project Structure

```
OntologyScraper/
├── DonwloadPages.py      # Wikipedia category scraper
├── NLP.py                # spaCy-based IS-A extraction
├── pages/                # Scraped article text (generated)
└── patterns/             # Extracted statements (generated)

```
## License

[MIT](LICENSE)
