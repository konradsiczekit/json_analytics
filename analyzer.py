import os
import json
from typing import Dict

def analyze_json_file(filepath: str) -> Dict:
    try:
        directory = os.path.basename(os.path.dirname(filepath))
        main_directory = os.path.basename(os.path.dirname(os.path.dirname(filepath)))

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        metadata = data.get("metadata", {})

        # Links
        links = []
        for l in data.get("links", []):
            if isinstance(l, dict) and "value" in l:
                links.append(l["value"])
            elif isinstance(l, str):
                links.append(l)
        links_str = ", ".join(links)

        # E-mails
        emails = []
        for e in data.get("emails", []):
            if isinstance(e, dict) and "value" in e:
                emails.append(e["value"])
            elif isinstance(e, str):
                emails.append(e)
        emails_str = ", ".join(emails)

        # Tables - zebranie wszystkich z klucza "tables" na poziomie dokumentu
        all_tables = []
        for idx, table in enumerate(data.get("tables", [])):
            page_number = table.get("page_number", "")
            table_index = table.get("table_index", "")
            # Automatyczny tytuł, jeśli nie ma "title"
            title = table.get("title") or f"Table {page_number}-{table_index}"
            headers = table.get("headers", [])
            headers = [str(h) if h is not None else "" for h in headers]
            preview_rows = table.get("preview_rows", [])
            csv_lines = []
            if any(headers):
                csv_lines.append(", ".join(headers))
            for row in preview_rows:
                row = [str(cell) if cell is not None else "" for cell in row]
                csv_lines.append(", ".join(row))
            # Składamy tekst: tytuł + tabela jako csv
            table_text = f"{title}\n" + "\n".join(csv_lines)
            all_tables.append(table_text)
        tables_separator = "\n\n---TABLE_SEPARATOR---\n\n"
        tables_str = tables_separator.join(all_tables)

        return {
            "Nazwa pliku": filepath,
            "Directory": directory,
            "Main Directory": main_directory,
            "Liczba stron": metadata.get("page_count", 0),
            "Liczba tabel": metadata.get("table_count", 0),
            "Liczba słów": metadata.get("word_count", 0),
            "Liczba linków": len(links),
            "Links": links_str,
            "Liczba maili": len(emails),
            "E-mails": emails_str,
            "Tables": tables_str,  # NOWA KOLUMNA!
            "Producent PDF": metadata.get("producer", ""),
            "Wersja PDF": metadata.get("pdf_version", ""),
            "Język": metadata.get("language", ""),
            "Czy zaszyfrowany": metadata.get("is_encrypted", False),
        }

    except Exception as e:
        return {"Nazwa pliku": filepath, "BŁĄD": str(e)}
