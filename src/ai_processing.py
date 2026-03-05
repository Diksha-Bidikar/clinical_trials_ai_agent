import anthropic
import os
from typing import Dict
import pandas as pd

CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def categorize_intervention(intervention_text: str) -> Dict[str, str]:
    """
    Use AI to categorize intervention type and extract specific names/agents.
    """
    if not CLAUDE_API_KEY or not intervention_text:
        return {"type": "Unknown", "drugs": []}

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

        prompt = f"""
        Analyze this intervention description and categorize it.

        Return JSON with:
        - "type": One of "Drug", "Biological", "Device", "Procedure", "Diagnostic Test", "Other"
        - "drugs": Array of specific names mentioned (drugs, biological agents, devices, tests, procedures)

        Examples:
        - "Drug: Aspirin (DRUG)" → {{"type": "Drug", "drugs": ["Aspirin"]}}
        - "Biological: Pembrolizumab (BIOLOGICAL)" → {{"type": "Biological", "drugs": ["Pembrolizumab"]}}
        - "Diagnostic Test: BRCA1 Gene Test" → {{"type": "Diagnostic Test", "drugs": ["BRCA1 Gene Test"]}}
        - "Device: Pacemaker Implant" → {{"type": "Device", "drugs": ["Pacemaker"]}}

        Intervention: "{intervention_text}"

        Extract ALL specific names, not just traditional drugs.
        """

        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=200,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.content[0].text.strip()
        parsed = None

        # Extract from markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result, re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group(1).strip())
            except json.JSONDecodeError:
                pass

        # Find JSON-like content
        if not parsed:
            json_start = result.find('{')
            json_end = result.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                potential_json = result[json_start:json_end]
                try:
                    parsed = json.loads(potential_json)
                except json.JSONDecodeError:
                    pass

        # Try entire response
        if not parsed:
            try:
                parsed = json.loads(result)
            except json.JSONDecodeError:
                pass

        # Manual extraction
        if not parsed:
            intervention_type = "Unknown"
            extracted_names = []

            # Determine type from text patterns
            text_lower = intervention_text.lower()
            if any(word in text_lower for word in ['drug', 'medication', 'tablet', 'oral']):
                intervention_type = "Drug"
            elif any(word in text_lower for word in ['biological', 'antibody', 'vaccine', 'cell therapy', 'monoclonal']):
                intervention_type = "Biological"
            elif any(word in text_lower for word in ['device', 'implant', 'stent', 'catheter']):
                intervention_type = "Device"
            elif any(word in text_lower for word in ['procedure', 'surgery', 'therapy', 'radiation']):
                intervention_type = "Procedure"
            elif any(word in text_lower for word in ['test', 'assay', 'diagnostic', 'screening', 'biomarker']):
                intervention_type = "Diagnostic Test"

            # Extract names using multiple patterns
            # Pattern 1: Parentheses content (DRUG), (BIOLOGICAL), etc.
            paren_matches = re.findall(r'\(([^)]+)\)', intervention_text)
            for match in paren_matches:
                if match.upper() in ['DRUG', 'BIOLOGICAL', 'DEVICE', 'PROCEDURE', 'DIAGNOSTIC TEST']:
                    continue  # Skip the type indicators
                extracted_names.append(match.strip())

            # Pattern 2: Colon-separated values
            if ':' in intervention_text:
                parts = intervention_text.split(':')
                if len(parts) > 1:
                    name_part = parts[1].strip()
                    # Remove type indicators
                    name_part = re.sub(r'\s*\([^)]+\)\s*$', '', name_part)
                    if name_part and len(name_part.split()) <= 5:  # Reasonable length limit
                        extracted_names.append(name_part)

            # Pattern 3: Capitalized words (potential drug/device names)
            capitalized_words = re.findall(r'\b[A-Z][a-zA-Z0-9\-]+(?:\s+[A-Z][a-zA-Z0-9\-]+)*\b', intervention_text)
            for word in capitalized_words:
                if len(word.split()) <= 3 and word not in ['The', 'And', 'Or', 'For', 'With', 'Drug', 'Biological', 'Device']:
                    extracted_names.append(word)

            # Remove duplicates and limit
            extracted_names = list(set(extracted_names))[:5]  # Max 5 names

            parsed = {"type": intervention_type, "drugs": extracted_names}

        # Validate the result
        if not isinstance(parsed, dict) or 'type' not in parsed or 'drugs' not in parsed:
            parsed = {"type": "Unknown", "drugs": []}

        if not isinstance(parsed['drugs'], list):
            parsed['drugs'] = []

        return parsed

    except Exception as e:
        print(f"Intervention categorization failed: {e}")
        return {"type": "Unknown", "drugs": []}


def generate_trial_summary(trial_data: Dict[str, Any]) -> str:
    """
    Use AI to generate a structured summary of the trial.
    """
    if not CLAUDE_API_KEY:
        return trial_data.get('brief_summary', '')

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

        prompt = f"""
        Generate a concise, structured summary of this clinical trial in 2-3 sentences.
        Focus on: what condition it treats, what intervention is tested, current status, and key outcomes if available.

        Trial Data:
        - Title: {trial_data.get('title', '')}
        - Condition: {trial_data.get('conditions', '')}
        - Intervention: {trial_data.get('interventions', '')}
        - Sponsor: {trial_data.get('sponsor', '')}
        - Status: {trial_data.get('status', '')}
        - Start Date: {trial_data.get('start_date', '')}
        - Completion Date: {trial_data.get('completion_date', '')}
        - Summary: {trial_data.get('brief_summary', '')}
        """

        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=150,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text.strip()

    except Exception as e:
        print(f"Summary generation failed: {e}")
        return trial_data.get('brief_summary', '')

def trial_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply AI processing to enrich the dataset with intervention categorization and AI summaries.
    """
    if df.empty:
        return df

    final_df = df.copy()

    # Add new columns
    final_df['intervention_category'] = None
    final_df['extracted_drugs'] = None
    final_df['ai_summary'] = None

    for idx, row in final_df.iterrows():
        print(f"Processing trial {idx+1}/{len(final_df)}: {row['nct_id']}")

        # Categorize intervention
        intervention_info = categorize_intervention(row.get('interventions', ''))
        final_df.at[idx, 'intervention_category'] = intervention_info.get('type', 'Unknown')
        final_df.at[idx, 'extracted_drugs'] = intervention_info.get('drugs', [])

        # Generate AI summary
        ai_summary = generate_trial_summary(row.to_dict())
        final_df.at[idx, 'ai_summary'] = ai_summary

    return final_df