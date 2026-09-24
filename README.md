# Ontology Scraper

A machine learning pipeline that turns raw text into **Axioms in the ALS DL Language**, aiming to produce output that is structurally and logically correct as an ontology. The system scrapes Wikipedia for training data, fine-tunes a `t5-small` sequence-to-sequence model with **LoRA**, and then refines it further using **reinforcement learning (PPO)** so that generated axioms better satisfy ontology-correctness constraints.

## Table of Contents

- [Overview](#overview)
- [Pipeline](#pipeline)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Download Wikipedia Pages](#1-download-wikipedia-pages)
  - [2. Preprocess into Sentences](#2-preprocess-into-sentences)
  - [3. Fine-Tune T5 with LoRA](#3-fine-tune-t5-with-lora)
  - [4. Merge the LoRA Adapter](#4-merge-the-lora-adapter)
  - [5. Reinforcement Learning with PPO](#5-reinforcement-learning-with-ppo)
- [Roadmap](#roadmap)
- [License](#license)

## Overview

Ontology Scraper explores whether a small, efficiently fine-tuned language model can learn to translate natural language sentences into formal **ALS DL** axioms — the kind of statements used to build description-logic ontologies. Rather than hand-writing extraction rules, the project:

1. Gathers a training corpus directly from Wikipedia categories.
2. Reduces each page to clean, atomic sentences.
3. Teaches a compact `t5-small` model the text-to-axiom mapping via supervised fine-tuning (LoRA).
4. Uses PPO-based reinforcement learning to push the model toward axioms that are not just fluent, but *logically valid* as ontology statements.

The result is an end-to-end pipeline from "a Wikipedia category" to "a fine-tuned model that emits ALS DL axioms."

## Pipeline

```
Wikipedia Category
       │
       ▼
DownloadPages.py        →  raw Wikipedia pages
       │
       ▼
NLP.py                  →  clean, single-sentence corpus (.txt)
       │
       ▼
T5FineTune.ipynb         →  t5-small + LoRA adapter (supervised fine-tuning)
       │
       ▼
merge_adapter.py         →  merged model (base + adapter weights combined)
       │
       ▼
rl_train_t5_ppo.py       →  PPO-refined model generating ALS DL axioms
```

## Project Structure

```
Ontology-Scraper/
├── DownloadPages.py       # Downloads all pages from a given Wikipedia category
├── NLP.py                 # Converts downloaded pages into single-sentence lines in a .txt corpus
├── T5FineTune.ipynb        # Fine-tunes t5-small with LoRA on the sentence → axiom task
├── merge_adapter.py        # Merges the LoRA adapter into the base model for the RL stage
├── rl_train_t5_ppo.py      # Further trains the merged model with PPO
└── README.md
```

## Tech Stack

| Purpose | Library |
|---|---|
| Model training | [PyTorch](https://pytorch.org/) |
| Model architecture / tokenization | [🤗 Transformers](https://github.com/huggingface/transformers) |
| Parameter-efficient fine-tuning | [🤗 PEFT](https://github.com/huggingface/peft) |
| Reinforcement learning | [🤗 TRL](https://github.com/huggingface/trl) |
| Data handling | [🤗 Datasets](https://github.com/huggingface/datasets), [pandas](https://pandas.pydata.org/) |
| Wikipedia scraping | [wikipedia-api](https://github.com/martin-majlis/Wikipedia-API) |
| NLP preprocessing | [spaCy](https://spacy.io/) |

## Installation

```bash
git clone https://github.com/s-reese04/OntologyScraper.git
cd OntologyScraper

python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

pip install torch transformers peft trl datasets pandas wikipedia-api spacy
python -m spacy download en_core_web_sm
```

> **Note:** Python 3.12 is recommended. Some compiled dependencies used here are not yet compatible with newer Python releases (e.g. 3.14).

## Usage

### 1. Download Wikipedia Pages

Downloads every page belonging to a given Wikipedia category.

```bash
python DownloadPages.py "Machine_learning"
```

### 2. Preprocess into Sentences

Takes the downloaded pages and reduces them to a single-sentence-per-line `.txt` corpus, ready for training.

```bash
python NLP.py
```

### 3. Fine-Tune T5 with LoRA

Open the notebook and run all cells to fine-tune `t5-small` on the text → ALS DL axiom task using a LoRA adapter.

```bash
jupyter notebook T5FineTune.ipynb
```

This produces a base model + LoRA adapter checkpoint.

### 4. Merge the LoRA Adapter

Combines the LoRA adapter weights into the base model, producing a single merged model that the RL stage can train directly.

```bash
python merge_adapter.py 
```

### 5. Reinforcement Learning with PPO

Uses the scraped sentences to further train the merged model with PPO, using a reward signal tied to ALS DL axiom correctness, to push generations toward valid ontology statements.

```bash
python rl_train_t5_ppo.py
```

## Roadmap
- Create a custom reward functions for PPO
- Host Model on a webserver

## License

[MIT](LICENSE)
