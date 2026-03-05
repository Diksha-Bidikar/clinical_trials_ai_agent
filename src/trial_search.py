import requests
import pandas as pd
import json
from typing import List, Dict, Any
import anthropic


def collect_trial_data(parsed_seed: Dict[str, str], max_results: int = 20) -> pd.DataFrame:
    """
    Collect and structure clinical trial data based on parsed seed input.
    Searches for trials and fetches details in one integrated process.
    """
    seed_description = f"condition: {parsed_seed.get('condition', '')}, intervention: {parsed_seed.get('intervention', '')}, sponsor: {parsed_seed.get('sponsor', '')}"
    print(f"Searching for clinical trials related to: {seed_description}...")

    # Search parameters
    params = {
        "format": "json",
        "countTotal": "true",
        "pageSize": max_results
    }

    # Use specific API parameters for each component
    if parsed_seed.get("condition"):
        params["query.cond"] = parsed_seed["condition"]
    if parsed_seed.get("intervention"):
        params["query.intr"] = parsed_seed["intervention"]
    if parsed_seed.get("sponsor"):
        params["query.spons"] = parsed_seed["sponsor"]

    # Use general term for targets/keywords
    additional_terms = []
    if parsed_seed.get("target"):
        additional_terms.append(parsed_seed["target"])
    if parsed_seed.get("keywords"):
        additional_terms.append(parsed_seed["keywords"])
    if additional_terms:
        params["query.term"] = " ".join(additional_terms)

    print(f"Search parameters: {params}")

    # Search for trials
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    print("response",response.json())
    data = response.json()
    studies = data.get("studies", [])
    print(f"Found {len(studies)} trials.")

    # Fetch details for each trial directly
    trial_data = []
    for i, study in enumerate(studies):
        nct_id = study.get("protocolSection", {}).get("identificationModule", {}).get("nctId")
        if nct_id:
            print(f"Fetching details for {nct_id} ({i+1}/{len(studies)})...")
            # Double-check sponsor filtering
            sponsor = study.get("protocolSection", {}).get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name", "")

            if parsed_seed.get("sponsor"):
              if parsed_seed["sponsor"].lower() not in sponsor.lower():
                continue  # Skip trials that don't match the sponsor
            try:
                # Get full details for this trial
                detail_params = {"format": "json"}
                detail_url = f"{BASE_URL}/{nct_id}"
                detail_response = requests.get(detail_url, params=detail_params)
                detail_response.raise_for_status()

                detail_data = detail_response.json()
                full_study = detail_data.get("protocolSection", {})

                # Extract key information
                details = {
                    "nct_id": nct_id,
                    "title": full_study.get("identificationModule", {}).get("briefTitle", ""),
                    "conditions": ", ".join(full_study.get("conditionsModule", {}).get("conditions", [])),
                    "interventions": ", ".join([
                        f"{intv.get('name', '')} ({intv.get('type', '')})"
                        for intv in full_study.get("armsInterventionsModule", {}).get("interventions", [])
                    ]),
                    "sponsor": sponsor,
                    # "sponsor": full_study.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name", ""),
                    "status": full_study.get("statusModule", {}).get("overallStatus", ""),
                    "brief_summary": full_study.get("descriptionModule", {}).get("briefSummary", ""),
                    "start_date": full_study.get("statusModule", {}).get("startDateStruct", {}).get("date", ""),
                    "completion_date": full_study.get("statusModule", {}).get("completionDateStruct", {}).get("date", "")
                }

                trial_data.append(details)
            except Exception as e:
                print(f"Error fetching {nct_id}: {e}")
    df = pd.DataFrame(trial_data)
    return df