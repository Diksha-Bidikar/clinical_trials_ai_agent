# AI Agent for Clinical Trial Intelligence

## Overview
This project builds a prototype AI-assisted system that automatically
discovers and structures information about clinical trials from public sources.

The system retrieves clinical trial data using public APIs and organizes
key attributes such as trial ID, intervention, sponsor, and status.

## Features
- Automated clinical trial discovery
- Structured extraction of trial metadata
- AI-assisted summarization
- Flexible seed query system

## Data Sources
- ClinicalTrials.gov API

## Example Query
"breast cancer durvalumab by AstraZeneca"

## Output
Structured dataset containing:
- Trial ID
- Disease
- Intervention
- Sponsor
- Status
- Summary

## Tech Stack
Python, Pandas, APIs, LLM tools