# Clinical Trials AI Agent

# 📖 Project Overview
An AI-powered research assistant that discovers, analyzes, and summarizes clinical trials from public biomedical data sources.

This project demonstrates how Large Language Models can augment scientific data pipelines to transform natural language research questions into structured clinical insights.

---

# 💡 Motivation

Clinical trial databases contain massive amounts of biomedical data, but exploring them efficiently often requires complex queries and manual analysis.

This project builds an **AI-assisted pipeline** that:

• interprets natural language queries  
• retrieves relevant clinical trials  
• categorizes therapeutic interventions  
• generates concise AI summaries  

The result is a structured dataset that helps researchers quickly understand ongoing clinical research.

---

# 📌 Example Query

User Input: breast cancer durvalumab by AstraZeneca


AI Extracted Search Parameters:
{
"condition": "breast cancer",
"intervention": "durvalumab",
"sponsor": "AstraZeneca"
}


Retrieved trials are enriched with:

• intervention classification  
• AI-generated trial summaries  

---

# ✨ Key Features

Natural Language Clinical Trial Search

AI interprets free-text research queries.

ClinicalTrials.gov Integration

Automated retrieval of publicly available clinical trials.

AI Intervention Categorization

LLM categorizes therapies such as:

• Immunotherapy  
• Targeted therapy  
• Combination therapy  

AI Trial Summaries

Each study is summarized into concise insights.

Structured Dataset Output.

Results are returned as an enriched research dataset.

---

## ✨ Project Architecture

The system follows a modular AI pipeline:
```
User Query  
↓  
LLM Query Parsing  
↓  
ClinicalTrials.gov API Search  
↓  
Trial Data Retrieval  
↓  
AI Processing  
• Intervention Categorization  
• Trial Summary Generation  
↓  
Enriched Clinical Trial Dataset
```

The system architecture and AI pipeline design are documented here:

- [Architecture Documentation](docs/architecture.md)
- [Architecture Diagram](docs/architecture_diagram.md)

---

# 📁 Project Structure
```
clinical_trials_ai_agent
│
├── src
│   ├── pipeline.py
│   ├── seed_processing.py
│   ├── trial_search.py
│   ├── ai_processing.py
│
├── notebooks
│   └── clinical_trial_ai_agent.ipynb
│
├── data
│   └── sample_trials.csv
│
├── docs
│   └── architecture.md
│
├── requirements.txt
├── .env
└── README.md
```

---

## 🚀 Quick Start

Follow these steps to run the AI agent locally.

### 1. Clone the repository

git clone https://github.com/Diksha-Bidikar/clinical_trials_ai_agent.git

cd clinical_trials_ai_agent


### 2. Install dependencies

pip install -r requirements.txt


### 3. Set up environment variables

Create a `.env` file in the project root and add your API key:

ANTHROPIC_API_KEY = your_api_key_here


### 4. Run the AI agent

python3 test_agent.py


The system will:

1. Interpret the research query using an LLM
2. Search ClinicalTrials.gov
3. Retrieve relevant trials
4. Categorize interventions
5. Generate AI summaries
6. Output enriched clinical trial results

---

## 📊 Example Output

The AI agent generates an enriched clinical trial dataset with the following fields:

| Field | Description |
|------|-------------|
| nct_id | Clinical trial identifier |
| title | Study title |
| conditions | Target disease or indication |
| interventions | Treatment being studied |
| sponsor | Trial sponsor organization |
| status | Recruitment status |
| brief_summary | Short description of the trial |
| start_date | Trial start date |
| completion_date | Expected completion date |
| intervention_category | AI-derived intervention classification |
| extracted_drugs | Drugs identified from intervention text |
| ai_summary | LLM-generated concise trial summary |
---

# 📌 Technologies Used

Python

Libraries

• Pandas  
• Requests  
• Anthropic Claude API  

Data Source: ClinicalTrials.gov API

---

# 🎯 Use Cases

Biomedical Research

Quick discovery of relevant clinical trials.

Pharmaceutical Competitive Intelligence

Track competitor trial activity.

Academic Literature Exploration

Identify active research in therapeutic areas.

---

# 🔮 Future Improvements

Potential enhancements include:

• Vector similarity search for clinical trials  
• Retrieval-Augmented Generation (RAG)  
• Interactive research dashboard  
• Clinical trial knowledge graphs  

---

# 🔗 Connect With Me

Author: Diksha Bidikar (Master's in Data Science, Rice University) 

LinkedIn: linkedin.com/in/diksha-bidikar

Portfolio: https://diksha-bidikar.github.io/

Email: bidikar.diksha@gmail.com

---

# License

MIT License