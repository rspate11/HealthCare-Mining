# Reuters-128 dataset
# contains 128 news articles
# 800 named entities with position in document and a URI of a DBpedia resource identifying the entity

# example of a document
# <document id="8">
#   <documenturi>http://www.research.att.com/~lewis/Reuters-21578/15009</documenturi>
#   <documentsource>Reuters-21578</documentsource>
#   <textwithnamedentities>
#     <namedentityintext uri="http://aksw.org/notInWiki/Home_Intensive_Care_Inc">Home Intensive Care Inc</namedentityintext>
#     <simpletextpart> said it has opened a Dialysis at Home office in </simpletextpart>
#     <namedentityintext uri="http://dbpedia.org/resource/Philadelphia">Philadelphia</namedentityintext>
#     <simpletextpart>, its 12th nationwide.</simpletextpart>
#   </textwithnamedentities>
# </document>
# sentence in document: Home Intensive Care Inc said it has opened a Dialysis at Home office in Philadelphia, its 12th nationwide
# named entity in document: Home Intensive Care Inc, Philadelphia

# extract data from xml
from bs4         import BeautifulSoup as bs
from bs4.element import Tag

import codecs

# Read data file and parse the XML
with codecs.open("reuters-128.xml", "r", "utf-8") as infile:
    soup = bs(infile, "lxml")


# creates a label for every word: N for named-entity, I for invalid (word, N), (word, I)
docs = []
for elem in soup.find_all("document"):
    texts = []

    # Loop through each child of the element under "textwithnamedentities"
    for c in elem.find("textwithnamedentities").children:
        if type(c) == Tag:
            if c.name == "namedentityintext":
                label = "N"  # part of a named entity
            else:
                label = "I"  # irrelevant word
            for w in c.text.split(" "):
                if len(w) > 0:
                    texts.append((w, label))
    docs.append(texts)


# generate POS tags: [('word', POS, N/i), ]
import nltk
nltk.download('averaged_perceptron_tagger')
data = []
for i, doc in enumerate(docs):
    # Obtain the list of tokens in the document
    tokens = [term for term, label in doc]
    # Perform POS tagging
    tagged = nltk.pos_tag(tokens)
    # Take the word, POS tag, and its label
    data.append([(w, pos, label) for (w, label), (word, pos) in zip(doc, tagged)])
