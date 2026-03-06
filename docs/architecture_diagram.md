# System Architecture

```mermaid
flowchart TD

A[User Research Query] --> B[LLM Query Parser]
B --> C[Structured Parameters]

C --> D[ClinicalTrials.gov API]

D --> E[Trial Data Retrieval]

E --> F[Data Processing Pipeline]

F --> G[AI Intervention Categorization]

F --> H[AI Trial Summarization]

G --> I[Enriched Trial Dataset]
H --> I

I --> J[CSV / DataFrame Output]
