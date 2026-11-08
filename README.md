# Atlas AI 🌍

A conversational travel recommender that uses **fuzzy logic** to suggest the three destinations that best match your preferences.

Team project for the **Knowledge-Based Systems** course, Bachelor in Artificial Intelligence & Data Science, La Salle – Universitat Ramon Llull (2025–2026).

![Python](https://img.shields.io/badge/Python-3-blue) ![NLTK](https://img.shields.io/badge/NLTK-NLP-green) ![Streamlit](https://img.shields.io/badge/Streamlit-app-red)

## What it does

You chat with Atlas AI in plain English. It asks six questions (when you want to travel, your budget, preferred weather, trip length, how far you'd go and what kind of holiday you want) and recommends your top 3 destinations out of 28 countries, each with a confidence score.

## How it works

1. **Understanding your answers:** a context-free grammar (NLTK `CFG` + `ChartParser`) checks each reply and extracts the key values, such as months, budget level or weather.
2. **Fuzzification:** each answer becomes a number and is mapped onto fuzzy sets with trapezoidal membership functions (for example, *cheap / medium / expensive* budgets).
3. **Rule evaluation:** a knowledge base of 67 fuzzy rules links user preferences to destination characteristics.
4. **Defuzzification:** scores are aggregated per destination and the top 3 are ranked.
5. **Interface:** a Streamlit chat with a separate recommendations view.

The system follows a knowledge-based architecture, keeping data (JSON), inference logic and presentation in separate modules.

## My contribution

I built the fuzzy inference model and tested the system.

## Team

Alex Vilamitjana · Sara Gibert · Oriol Pros

## Run it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project structure

```
app.py                     Entry point and page navigation
fuzzy/
  fuzzy_sets.json          Membership functions for each variable
  rules.json               67 fuzzy rules (knowledge base)
  countries.json           Destination characteristics (28 countries)
  fuzzification.py         Turns numeric inputs into fuzzy memberships
  rule_evaluation.py       Applies the rules to each destination
  defuzzification.py       Aggregates scores and ranks the top 3
  inference_engine.py      Runs the full fuzzy pipeline
nav/
  chat.py                  Conversational interface
  recommendations.py       Results view
  utils.py                 Grammar, parsing and answer-to-number conversion
img/                       Logo assets
```
