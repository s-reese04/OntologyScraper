import os
import re
import glob
import spacy

def clean_wikipedia_text(text: str) -> str:
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"={2,}.*?={2,}", "", text)
    text = re.sub(r"'{2,}", "", text)
    text = re.sub(r"\|.*?=.*?(\n|$)"," ", text)
    text = re.sub(r"\{\{.*?\}\}", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"www\.\S+", "", text)
    text = re.sub(r"&\w+;", "", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"^\s*[*#]+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\n", " ", text)

    return text.strip()

def is_valid_sentence(sentence: str) -> bool:

    s = sentence.strip()

    if len(s.split()) < 4:
        return False

    if re.fullmatch(r"[\W\d]+", s):
        return False
    
    if not re.search(r"[.!?]$", s):
        return False

    return True
    

def process_pages(input_folder: str = "pages", output_file: str = "patterns/sentences.txt"):
    nlp = spacy.load("en_core_web_sm")

    txt_files = sorted(glob.glob(os.path.join(input_folder, "*.txt")))

    total_sentences = 0

    with open(output_file, "w", encoding="utf-8") as out_f:
        for filepath in txt_files:
            print(f"Parsing: {filepath}")
            with open(filepath, "r", encoding="utf-8") as in_f:
                text=in_f.read()
            
            text = clean_wikipedia_text(text)

            doc = nlp(text)
    
            for sent in doc.sents:
                sentence = sent.text.strip() 
                if is_valid_sentence(sentence):
                    out_f.write(sentence + "\n")
                    total_sentences += 1

if __name__ == "__main__":
    process_pages("pages", "patterns/sentences.txt")
