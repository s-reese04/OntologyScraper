import spacy
from spacy.matcher import DependencyMatcher
from os import listdir, makedirs
from os.path import isfile, join

nlp = spacy.load("en_core_web_sm")
matcher = DependencyMatcher(nlp.vocab)

pattern = [
    {
        "RIGHT_ID": "predicate",
        "RIGHT_ATTRS": {"LEMMA": "be"}
    },
    {
        "LEFT_ID": "predicate",
        "REL_OP": ">",
        "RIGHT_ID": "subject",
        "RIGHT_ATTRS": {"DEP": "nsubj"}
    },
    {
        "LEFT_ID": "predicate",
        "REL_OP": ">",
        "RIGHT_ID": "object",
        "RIGHT_ATTRS": {"DEP": "attr"}
    }
]
matcher.add("IS_A", [pattern])


def findPatternInPages(matcher, nlp, pages):
    with open("patterns/pattern.txt", "a") as patternFile:
        for page in pages:
            print(f"Finding Patterns in: {page}")
            with open(join("pages", page), "r") as f:
                content = f.read()

            doc = nlp(content)
            matches = matcher(doc)
            for match_id, token_ids in matches:
                subj = doc[token_ids[1]]
                obj = doc[token_ids[2]]
                patternFile.write(f"{subj.text} IS-A {obj.text}\n")


pages = [f for f in listdir("pages") if isfile(join("pages", f))]
findPatternInPages(matcher, nlp, pages)
