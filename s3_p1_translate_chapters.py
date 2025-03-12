from openai import OpenAI
import json
import os, glob
import time
import os

from s2_p1_parse_name_translations import get_translation_names
from s2_p2_merge_translations import create_update_translation_dict

openai_client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
  organization=os.getenv("OPENAI_ORG_ID"),
  project=os.getenv("OPENAI_PROJECT_ID"),
)

deepseek_client = OpenAI(
  api_key=os.getenv("DEEPSEEK_API_KEY"),
  base_url="https://api.deepseek.com/v1"
)

try:
    with open('translation_dict_short.json', 'r', encoding='utf-8') as file:
        translation_dict = json.load(file)
        translation_dict_str = json.dumps(translation_dict, indent=4, ensure_ascii=False)
except:
    translation_dict = {}
    translation_dict_str = ""
    print("!!! Translation dictionary not found.")

eng_chapters = glob.glob('chapters_eng\*.txt')
eng_chapters = {os.path.basename(chapter).split(' - ')[0]: chapter for chapter in eng_chapters}

custom_prompt = """
Act as an professional english-to-russian translator with world global awards for fantasy translation. Translate the text above to russian.
Be carefull with names of characters, places, etc. You can tune the translation so it will fit for russian readers, but avoid hallucination and information that was not in the source text.
Use ready translation vocabulary dict to help you with translation.
All dialogues should start with a dash "-".
All thoughts should be quoted with double quotes «».
"""

with open('chapters_translated/Chapter_957 - Tooth and Nail.txt', 'r', encoding='utf-8') as file:
    previouse_translation = file.read()

for i in range(1087, 1231):
    print(f"Processing Chapter {i}")
    start_time = time.time()
    
    try:
        english_chapter_path = eng_chapters[f'Chapter_{i:03d}']
    except KeyError:
        print(f"Chapter {i} not found.")
        break
    
    with open(english_chapter_path, 'r', encoding='utf-8') as file:
        english_chapter_text = file.read()

    #--- INITIAL TRANSLATION ---
    print(f'Chapter {i} - Initial Translation')
    
    # previous_translation_prompt = f"""
    # TRANSLATION OF PREVIOUS CHAPTER:
    # {previouse_translation}
    
    # DO NOT ANSWER THIS PROMPT. JUST READ IT TO UNDERSTAND THE CONTEXT.
    # """
    
    translation_dict_prompt = f"""
    TRANSLATION VOCABULARY DICT:
    {translation_dict_str}
    
    DO NOT ANSWER THIS PROMPT. JUST READ IT TO UNDERSTAND THE CONTEXT.
    """
    
    prompt = f"""
    ENGLISH CHAPTER TEXT:
    {english_chapter_text}

    YOUR TASK:
    {custom_prompt}
    """
    
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are an expert in english to russian translation. You can professionally translate the text so native speakers cannot distinguish it from original."},
           #  {"role": "user", "content": previous_translation_prompt},
            {"role": "user", "content": translation_dict_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    initial_translation = response.choices[0].message.content
    with open(os.path.join('raw_chapters_translated', os.path.basename(english_chapter_path)), 'w', encoding='utf-8') as file:
        file.write(initial_translation)
    
    print(f'Time elapsed: {time.time() - start_time}')
    #--- TUNED TRANSLATION ---
    print(f'Chapter {i} - Tuned Translation')
    
    prompt = f"""
    МАШИННЫЙ ПЕРЕВОД НА РУССКИЙ ЯЗЫК:
    {initial_translation}
    
    ЗАДАЧА:
    Сделай так, чтобы русский читатель не понял, что текст был переведен машиной. Однако не добавляй никакой информации, которой не было в оригинале.
    Изменяй текст точечно, только если это требуется.
    НЕ МЕНЯЙ НИКАКИХ НАЗВАНИЙ - ПЕРСОНАЖЕЙ, МЕСТ, ПРЕДМЕТОВ, И Т.Д.
    Все диалоги должны начинаться с дефиса "-".
    Все мысли должны быть заключены в кавычки «».
    """
    
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Ты профессиональный копирайтер русского текста. Ты обрабатываешь текст, полученный в результате машинного перевода, и делаешь его таким, будто он был написан носителем русского языка."},
            {"role": "user", "content": prompt}
        ]
    )
    
    tuned_translation = response.choices[0].message.content
    with open(os.path.join('chapters_translated', os.path.basename(english_chapter_path)), 'w', encoding='utf-8') as file:
        file.write(tuned_translation)
    
    previouse_translation = tuned_translation
    
    print(f'Time elapsed: {time.time() - start_time}')
    #--- NEW NAMES TRANSLATION ---
    print(f'Chapter {i} - New Names Translation')
    
    json_data = get_translation_names(openai_client, english_chapter_text, tuned_translation, i)
    with open(f'word_translation_parser_responses/Chapter_{i:03d}.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
    
    #--- UPDATE TRANSLATION VOCABULARY DICT ---
    print(f'Chapter {i} - Update Translation Vocabulary Dict')
    
    translation_dict = create_update_translation_dict()
    translation_dict_str = json.dumps(translation_dict, indent=4, ensure_ascii=False)
    
    print(f'Time elapsed: {time.time() - start_time}')