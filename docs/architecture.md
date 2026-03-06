# Clinical Trials AI Agent – System Architecture

## Overview

This project implements an AI-assisted research agent that automatically discovers, analyzes, and summarizes clinical trials using public biomedical data sources.

The system combines:

• Large Language Models (Claude API)  
• ClinicalTrials.gov public API  
• Structured data processing  
• AI-powered clinical intelligence extraction  

The goal is to transform **unstructured research queries** into **structured clinical trial insights**.

---

# System Workflow

The AI agent follows a multi-stage pipeline.

User Query
     │
     ▼
LLM Query Understanding
     │
     ▼
Structured Search Parameters
     │
     ▼
ClinicalTrials.gov API Search
     │
     ▼
Trial Data Extraction
     │
     ▼
AI Processing
     ├─ Intervention Categorization
     └─ Trial Summary Generation
     │
     ▼
Structured Clinical Intelligence Dataset

---

# Architecture Diagram
User Query
(e.g. “breast cancer durvalumab by AstraZeneca”)

↓

1. Seed Processing (LLM)

Extract structured parameters

↓

2. Trial Discovery

Search ClinicalTrials.gov

↓

3. Data Structuring

Extract key trial metadata

↓

4. AI Processing

Categorize interventions
Generate trial summaries

↓

5. Enriched Clinical Dataset

CSV / DataFrame output


---

# Component Breakdown

## 1. Seed Input Processing

File: src/seed_processing.py


Purpose: Convert natural language queries into structured parameters.

Example:

Input: breast cancer durvalumab by AstraZeneca

Output: 
{
"condition": "breast cancer",
"intervention": "durvalumab",
"sponsor": "AstraZeneca"
}


This is performed using the **Claude LLM API**, which interprets the semantic structure of biomedical queries.

Benefits:

• Flexible natural language queries  
• No strict search syntax required  
• Improved search precision  

---

## 2. Clinical Trial Discovery

File: src/trial_search.py


Data Source: ClinicalTrials.gov API. (https://clinicaltrials.gov/api/v2/studies)


The module:

• Queries trials based on extracted parameters  
• Retrieves structured study metadata  
• Handles pagination and result limits  

Key attributes extracted include:

- NCT ID
- Study Title
- Condition
- Intervention
- Sponsor
- Phase
- Recruitment Status
- Brief Summary

Results are converted into a **Pandas DataFrame** for downstream processing.

---

## 3. AI Intervention Categorization

File: src/ai_processing.py


This module uses an LLM to classify intervention descriptions.

Example:

Input: Durvalumab + Chemotherapy


Output: 
{
"type": "Combination Therapy",
"drugs": ["Durvalumab"]
}


Interventions may be categorized as:

- Immunotherapy
- Targeted Therapy
- Combination Therapy
- Chemotherapy
- Vaccine
- Gene Therapy

This step enables **high-level therapeutic analysis** across trials.

---

## 4. AI Trial Summary Generation

Also implemented in: src/ai_processing.py

Each trial is summarized using an LLM.

Example output:
This Phase 2 study evaluates the PD-L1 inhibitor durvalumab in patients with advanced breast cancer. The trial investigates the safety and efficacy of immunotherapy in combination with standard chemotherapy.



Benefits:

• Rapid understanding of complex trials  
• Improved clinical research exploration  
• Automated knowledge extraction  

---

## 5. Dataset Enrichment

File: src/pipeline.py


Pipeline responsibilities:

1. Process seed input
2. Retrieve trials
3. Categorize interventions
4. Generate trial summaries
5. Produce enriched dataset

The final output contains:

| Field | Description |
|------|-------------|
| NCT ID | Clinical trial identifier |
| Title | Study title |
| Condition | Target disease |
| Intervention | Treatment |
| Status | Recruitment status |
| Intervention Category | AI-derived classification |
| Trial Summary | AI-generated summary |

---

# Example Output

Example enriched dataset:

| NCT ID | Condition | Intervention | Category | Summary |
|------|------|------|------|------|
| NCT0123456 | Breast Cancer | Durvalumab | Immunotherapy | Phase 2 trial evaluating PD-L1 blockade... |

---

# Technology Stack

Programming Language

Python

Libraries

• requests  
• pandas  
• anthropic (Claude API)  

Data Sources

• ClinicalTrials.gov API  

AI Model

Claude LLM

---

# Design Principles

The system was designed around several key principles:

### Modularity

Each stage of the pipeline is independent and extensible.

### AI-Augmented Research

LLMs enhance:

• query interpretation  
• trial classification  
• knowledge summarization  

### Reproducibility

Results are structured into datasets that can be reused for research.

---

# Future Improvements

Potential extensions include:

### Vector Search

Embedding-based semantic retrieval of trials.

### RAG Architecture

Retrieval-augmented generation for deeper trial analysis.

### Research Dashboard

Interactive exploration via Streamlit.

### Clinical Knowledge Graph

Link drugs, sponsors, targets, and diseases.

---

# Conclusion

This AI agent demonstrates how modern LLMs can accelerate biomedical research by transforming large public datasets into structured clinical intelligence.


