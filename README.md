# Dummy AI Novel Translator

## Overview
This project is an AI-powered novel translator using OpenAI and DeepSeek APIs. It is designed to translate English novels into Russian (or any other language) while maintaining consistent terminology for character names, locations, skills, etc.

## Features
- **Automated Novel Translation:** Uses DeepSeek API to translate entire novels.
- **Consistent Terminology:** Ensures uniform translation of names and key terms using OpenAI API.
- **Human-Translated Reference Parsing:** Extracts terminology from human-translated chapters to improve accuracy.
- **Custom Dictionary Management:** Builds and updates a translation dictionary dynamically.
- **FB2 Format Export:** Converts translated chapters into an `.FB2` file for easy reading.

## Project Structure
```
.gitignore
env_example                 # Example of environment variables

demo/                       # Directory with processed results
├── chapters_eng/           # Chapters ready for translation
├── chapters_rus/           # Human-translated chapters
├── chapters_translated/    # AI-translated chapters
├── raw_chapters_eng/       # Raw source text
├── raw_chapters_rus/       # Raw human-translated text
├── raw_chapters_translated/# Raw AI-translated text
├── word_translation_parser_responses/ # Translation dictionary per chapter
├── shadow_slave_1000_1004.fb2 # Final translated novel in FB2 format
├── translation_dict.json   # Common terminology dictionary
└── translation_dict_short.json # Shortened version for prompt insertion

s1_p1_parse_chapters_raw_rus.py   # Parses human-translated text into separate files
s1_p2_parse_chapters_raw_eng.py   # Parses original text into separate files
s2_p1_parse_name_translations.py  # Extracts and standardizes name translations
s2_p2_merge_translations.py       # Processes name translation data
s3_p1_translate_chapters.py       # Translates chapters and updates terminology dictionary
s4_p1_fb2_wrap.py                 # Converts translated chapters into an .FB2 file
```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Copy `env_example` to `.env` and fill in required API keys.

## Usage
### Step 1: Prepare Chapters
- Place raw English and Russian chapters into `raw_chapters_eng/` and `raw_chapters_rus/` respectively.
- Run parsing scripts:
  ```bash
  python s1_p1_parse_chapters_raw_rus.py
  python s1_p2_parse_chapters_raw_eng.py
  ```

### Step 2: Process Name Translations
- Extract and standardize name translations:
  ```bash
  python s2_p1_parse_name_translations.py
  ```
- Merge and clean translation data:
  ```bash
  python s2_p2_merge_translations.py
  ```

### Step 3: Translate Chapters
- Translate the novel:
  ```bash
  python s3_p1_translate_chapters.py
  ```

### Step 4: Generate FB2 File
- Create `.FB2` file for reading:
  ```bash
  python s4_p1_fb2_wrap.py
  ```

## Contributing
~~Pull requests are welcome!~~ For personal use. No plans to maintain this repo.

## License
MIT License.

