from src.pipeline import run_agent


def main():

    query = "breast cancer durvalumab AstraZeneca"

    print("\nRunning Clinical Trials AI Agent...\n")

    results = run_agent(query)

    print("\nTop Results:\n")

    print(results.head())


if __name__ == "__main__":
    main()