import os
from typing import Dict
import anthropic
# import relate

CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not CLAUDE_API_KEY:
    print("Warning: CLAUDE_API_KEY not set!")
    
def process_seed_input_with_llm(seed_input: str) -> Dict[str, str]:
    """
    Use LLM to understand and parse the natural language seed input.
    Extracts key components like disease, intervention, sponsor, etc.
    """
    if not CLAUDE_API_KEY:
        return {"condition": seed_input, "intervention": "", "sponsor": "", "target": "", "keywords": ""}

    try:
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

        prompt = f"""
        Analyze the following natural language query for clinical trial search: "{seed_input}"

        Extract the following components if present:
        - Disease/Condition: The medical condition or disease mentioned
        - Intervention/Drug: Any specific treatment, drug, or intervention
        - Sponsor/Company: Any mentioned company or sponsor
        - Target: Any molecular target if specified
        - Other keywords: Any other relevant terms

        Return ONLY a valid JSON object with keys: condition, intervention, sponsor, target, keywords
        Do not include any other text, explanations, or formatting. Just the JSON.
        Example: {{"condition": "breast cancer", "intervention": "", "sponsor": "", "target": "", "keywords": ""}}
        """

        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=200,
            temperature=0.1,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response.content[0].text.strip()

        # Extract JSON if wrapped in code blocks
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', result, re.DOTALL)
        if json_match:
            result = json_match.group(1).strip()

        # Parse JSON
        try:
            parsed = json.loads(result)
            return parsed
        except json.JSONDecodeError as je:
            print(f"JSON parsing failed: {je}. Response was: '{result}'.")
            return {"condition": seed_input, "intervention": "", "sponsor": "", "target": "", "keywords": ""}

    except Exception as e:
        print(f"LLM processing failed: {e}.")
        return {"condition": seed_input, "intervention": "", "sponsor": "", "target": "", "keywords": ""}
