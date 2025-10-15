# ARGUS NLP Setup Guide

## Installing Dependencies

After setting up your virtual environment, follow these steps:

### 1. Install Python packages
```bash
pip install -r requirements.txt
```

### 2. Download spaCy English Language Model
```bash
python -m spacy download en_core_web_sm
```

## What is the spaCy en_core_web_sm model?

The `en_core_web_sm` is a **small English language model** provided by spaCy that includes:

### Core Capabilities:
- **Tokenization**: Breaks text into individual words and punctuation
- **Part-of-speech tagging**: Identifies nouns, verbs, adjectives, etc.
- **Named Entity Recognition (NER)**: Identifies and classifies entities like:
  - PERSON: People's names
  - ORG: Organizations, companies, agencies
  - GPE: Countries, cities, states (Geopolitical entities)
  - MONEY: Monetary values
  - DATE: Dates and time periods
  - And many more...

### Why we use it in ARGUS:
1. **Intelligence Gathering**: Automatically extract key entities from news articles
2. **Information Classification**: Sort information by type (people, organizations, locations)
3. **Relationship Mapping**: Understand connections between entities in different articles
4. **Trend Analysis**: Track mentions of specific entities over time

### Model Size and Performance:
- **Size**: ~15MB (small footprint)
- **Speed**: Fast processing suitable for real-time analysis
- **Accuracy**: Good balance between speed and accuracy for general use

### Alternative Models:
- `en_core_web_md`: Medium model (~50MB) - better accuracy
- `en_core_web_lg`: Large model (~750MB) - highest accuracy
- `en_core_web_trf`: Transformer model (~560MB) - state-of-the-art accuracy

For ARGUS, we start with the small model for quick setup and good performance.

## Verification

Test your installation:
```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple Inc. is looking at buying a startup in San Francisco.")
for ent in doc.ents:
    print(ent.text, ent.label_)
```

Expected output:
```
Apple Inc. ORG
San Francisco GPE
```