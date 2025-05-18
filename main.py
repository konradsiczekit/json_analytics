import os
import csv
from analyzer import analyze_json_file
from logger_config import setup_logger

logger = setup_logger("json_summary_app")

def find_json_files(base_dir: str) -> list:
    logger.info(f"Szukanie plików .json w: {base_dir}")
    paths = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.lower().endswith('.json'):
                paths.append(os.path.join(root, f))
    logger.info(f"Znaleziono {len(paths)} plików .json")
    return paths

def save_summary_to_csv(results: list, output_path: str):
    import csv

    if not results:
        logger.warning("Brak wyników do zapisania.")
        return

    fieldnames = list(results[0].keys())
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            delimiter=';',                # separator zgodny z PL
            quotechar='"',
            quoting=csv.QUOTE_ALL         # cytowanie każdej wartości
        )
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    logger.info(f"Zapisano podsumowanie do pliku: {output_path}")


def main(input_dir: str, output_file: str):
    files = find_json_files(input_dir)
    results = []
    for path in files:
        logger.info(f"Analiza pliku: {path}")
        result = analyze_json_file(path)
        results.append(result)
    save_summary_to_csv(results, output_file)

if __name__ == "__main__":
    input_dir = r"C:\Users\sicze\PycharmProjects\Selenium\MaterialyGPT\BROKERZY"
    output_file = r"C:\Users\sicze\PycharmProjects\json_analytics\podsumowanie.csv"
    main(input_dir, output_file)

