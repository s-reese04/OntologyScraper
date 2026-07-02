import wikipediaapi
import sys

# Retrieve Wikipedia pages
# via Wikipedia-api

wiki = wikipediaapi.Wikipedia('OntologyScraper/1.0 (simonrk@gmx.de)', 'en')
cat = wiki.page(f"Category:{sys.argv[1]}")

def get_category_members(categorymembers, level=0, max_level=1):
    pages = []
    for title, page in categorymembers.items():
        if page.ns == wikipediaapi.Namespace.MAIN:
            pages.append(title)
        elif page.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            pages += get_category_members(page.categorymembers, level + 1, max_level)
    return pages


all_pages = get_category_members(cat.categorymembers)


def savePageContent(pages):
    for p_name in pages:
        page = wiki.page(p_name)
        with open(f"pages/{p_name}.txt", "a") as f:
            f.write(page.text)


savePageContent(all_pages)
