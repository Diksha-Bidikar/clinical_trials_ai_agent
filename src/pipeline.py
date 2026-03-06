from .seed_processing import process_seed_input_with_llm
from .trial_search import collect_trial_data
from .ai_processing import trial_dataset

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

def run_agent(seed_input, max_results=20):

    parsed_seed = process_seed_input_with_llm(seed_input)

    trials_df = collect_trial_data(parsed_seed, max_results)

    enriched_df = trial_dataset(trials_df)

    return enriched_df