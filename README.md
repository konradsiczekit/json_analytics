
---

# 📂 JSON Analytics – Katalogowanie i Streszczenie Analiz PDF

## **Opis projektu**

Aplikacja umożliwia **automatyczne skanowanie folderów** w poszukiwaniu plików `.json` będących wynikiem analizy dokumentów PDF. Dla każdego pliku generuje podsumowanie (streszczenie) i zapisuje zbiorczo całość do pliku `.csv` – gotowego do analizy w Excelu, Power BI lub innym narzędziu BI.

Kluczowe cechy:

* **Rekurencyjne** przeszukiwanie folderów
* **Analiza struktury JSON** – wyciąganie kluczowych informacji z każdego pliku
* **Wyciąganie, streszczenie oraz normalizacja** tabel, linków, e-maili i metadanych PDF
* **Przyjazny dla Excela** format CSV (`;` jako separator, UTF-8)

---

## **Struktura katalogów i plików**

```
json_analytics/
│
├── main.py             # Główna aplikacja: skanowanie folderów, wywołanie analizy, zapis CSV
├── analyzer.py         # Analiza pojedynczego pliku JSON (wyciąganie danych, formatowanie)
├── logger_config.py    # Konfiguracja logowania
├── README.md           # Niniejszy plik
```

---

## **Jak uruchomić?**

1. **Ustaw ścieżkę wejściową** (folder z JSON-ami) oraz wyjściową (plik CSV) w `main.py`:

   ```python
   if __name__ == "__main__":
       input_dir = r"C:\ścieżka\do\folderu"
       output_file = r"C:\ścieżka\do\podsumowanie.csv"
       main(input_dir, output_file)
   ```
2. **Uruchom aplikację z terminala:**

   ```bash
   python main.py
   ```
3. **Sprawdź plik wynikowy** (`podsumowanie.csv`) w Excelu lub Power BI.

---

## **Opis najważniejszych plików**

### `main.py`

* Rekurencyjne wyszukiwanie wszystkich plików `.json` w zadanym folderze
* Analiza każdego pliku przez `analyzer.py`
* Zapis wyników do CSV (Excel-friendly, separator `;`, cytowanie wszystkich pól)

### `analyzer.py`

* Wyciąga dane z pojedynczego pliku JSON
* Zwraca słownik z następującymi polami:

  * **Nazwa pliku** – pełna ścieżka do analizowanego pliku `.json`
  * **Directory** – bezpośredni folder pliku
  * **Main Directory** – folder o jeden poziom wyżej
  * **Liczba stron** – liczba stron PDF
  * **Liczba tabel** – liczba wykrytych tabel w pliku
  * **Liczba słów** – liczba słów w dokumencie
  * **Liczba linków** – ile linków wykryto w dokumencie
  * **Links** – wszystkie linki, oddzielone przecinkami
  * **Liczba maili** – ile adresów e-mail wykryto
  * **E-mails** – wszystkie maile, oddzielone przecinkami
  * **Tables** – wszystkie tabele z dokumentu, każda w formacie CSV, oddzielone wyraźnym separatorem
  * **Producent PDF** – producent oprogramowania PDF
  * **Wersja PDF** – wersja PDF
  * **Język** – wykryty język dokumentu
  * **Czy zaszyfrowany** – czy PDF jest zaszyfrowany
* Obsługuje błędy – w razie błędu kolumna `BŁĄD` zawiera opis wyjątku

### `logger_config.py`

* Konfiguracja logowania do konsoli
* Format: `[czas] - [poziom] - [wiadomość]`
* Możliwość łatwej rozbudowy (np. logowanie do pliku)

---

## **Format pliku wynikowego `.csv`**

Każdy wiersz to podsumowanie jednego pliku JSON.

| Nazwa pliku          | Directory | Main Directory | Liczba stron | Liczba tabel | Liczba słów | Liczba linków | Links | Liczba maili | E-mails | Tables | Producent PDF | Wersja PDF | Język | Czy zaszyfrowany |
| -------------------- | --------- | -------------- | ------------ | ------------ | ----------- | ------------- | ----- | ------------ | ------- | ------ | ------------- | ---------- | ----- | ---------------- |
| C:\ścieżka\plik.json | ...       | ...            | ...          | ...          | ...         | ...           | ...   | ...          | ...     | ...    | ...           | ...        | ...   | ...              |

**Kolumna "Tables":**

* Każda tabela pojawia się w formacie:

  ```
  Tytuł tabeli (lub Table <page_number>-<table_index>)
  Nagłówek1, Nagłówek2, ...
  wiersz1-kol1, wiersz1-kol2, ...
  wiersz2-kol1, wiersz2-kol2, ...
  ```
* Tabele oddzielone separatorem:

  ```
  ---TABLE_SEPARATOR---
  ```

  (z pustą linią nad i pod separatorem).

---

## **Wskazówki i najczęstsze problemy**

* **CSV w jednej kolumnie w Excelu?**
  Ustaw separator na `;` podczas importu.
* **Brakujące dane?**
  Puste komórki oznaczają brak danych w pliku JSON.
* **Błąd w kolumnie `BŁĄD`?**
  Zawiera szczegóły błędu przy analizie pliku.

---

## **Możliwości rozbudowy**

* Dodanie eksportu do SQL lub PowerBI (np. przez ODBC)
* Rozszerzenie o analizę plików DOCX, XLSX, itp.
* Rozpoznawanie typów dokumentów, auto-tagowanie słów kluczowych
* Filtrowanie/wykluczanie duplikatów na podstawie ścieżki lub metadanych
* Rozbudowane logowanie (np. do pliku)
* Automatyczne wykrywanie i obsługa kodowań plików

---

## **Przykładowy workflow**

1. Skopiuj pliki `.json` do wybranego katalogu (zagnieżdżenia nie mają znaczenia)
2. Ustaw ścieżki w `main.py`
3. Odpal `python main.py`
4. Otwórz plik `podsumowanie.csv` w Excelu/Power BI
5. Przeglądaj tabele, metadane i kluczowe informacje dla każdego dokumentu

