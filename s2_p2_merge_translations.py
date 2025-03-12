import json
import glob
from collections import Counter, defaultdict

def create_update_translation_dict():
    translation_dicts = glob.glob('word_translation_parser_responses/*.json')

    # Initialize a defaultdict to store lists of translations for each English word
    translations = defaultdict(list)
    english_word_counter = Counter()

    # Step 2: Iterate over each JSON file
    for file_path in translation_dicts:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Step 3: Filter key-value pairs where the English word contains capital letters
            filtered_data = {k: v for k, v in data.items() if any(c.isupper() for c in k)}
            # Step 4: Append translations to the corresponding English word in the defaultdict
            for eng_word, rus_translation in filtered_data.items():
                english_word_counter.update([eng_word])
                translations[eng_word].append(rus_translation)

    # Step 5: Create a Counter dictionary to count the number of unique translations for each English word
    translation_counts = {word: Counter(trans) for word, trans in translations.items()}

    translation_counts = dict(sorted(translation_counts.items(), key=lambda x: english_word_counter.get(x[0]), reverse=True))

    translation_dict_common = {}
    for english_word, translations in translation_counts.items():
        translation_dict_common[english_word] = {'n' : english_word_counter.get(english_word), 'translations' : dict(translations)}

    with open('translation_dict.json', 'w', encoding='utf-8') as file:
        json.dump(translation_dict_common, file, ensure_ascii=False, indent=4)
        
    print('Translation dictionary successfully created!')
    print('Number of English words:', len(translation_dict_common))

    translation_dict_short = {}

    for english_word, translations in translation_counts.items():
        translation_dict_short[english_word] = translations.most_common(1)[0][0]

    with open('translation_dict_short.json', 'w', encoding='utf-8') as file:
        json.dump(translation_dict_short, file, ensure_ascii=False, indent=4)
        
    return translation_dict_short

if __name__ == '__main__':
    create_update_translation_dict()