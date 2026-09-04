# OntologyScraper

A T5 based language model to extract Statements in ALC Description Language from Natural Language Sentences

**Example:** Input: Every cat is an animal => Output: Cat ⊑ Animal 

## Components

1. Notebook for fine tuning a t5-small model
2. Test Script
3. Wikipedia Scraper based on wikipediaapi

## Planed Features

1. Further Training via Reinforcement Learning
2. Full Ontology Generation
3. Hosted website

## Requirements

- Python 3.12+
- [spaCy](https://spacy.io/) with the `en_core_web_sm` English model
- [wikipedia-api](https://pypi.org/project/Wikipedia-API/)
- [transformers](https://github.com/huggingface/transformers)
- [peft](https://github.com/huggingface/peft)
- [datasets](https://github.com/huggingface/datasets)
- [accelerate](https://github.com/huggingface/accelerate)
- [pandas](https://github.com/pandas-dev/pandas)
- [PyTorch](https://github.com/pytorch/pytorch)

## License

[MIT](LICENSE)
