from openai import OpenAI
import json
import glob, os

def get_translation_names(client, english_chapter_text, russian_chapter_text, i):
    custom_prompt = """
    Find all names (of characters, places, weapon, etc.) in text and their translations and provide JSON dictionary file as output.
    JSON format: {"english_name": "russian_translation", ...}
    NO OTHER OUTPUT, ONLY JSON
    """

    prompt = f"""
    ENGLISH SOURCE TEXT:
    {english_chapter_text}

    RUSSIAN TRANSLATION:
    {russian_chapter_text}

    YOUR TASK:
    {custom_prompt}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert in english to russian translation."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    if len(response.choices) > 0:
        message_content = response.choices[0].message.content
        try:
            json_data = json.loads(message_content)
            return json_data
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")

if __name__ == '__main__':
    rus_chapters = glob.glob('chapters_rus\*.txt')
    rus_chapters = {os.path.basename(chapter).split(' - ')[0]: chapter for chapter in rus_chapters}

    eng_chapters = glob.glob('chapters_eng\*.txt')
    eng_chapters = {os.path.basename(chapter).split(' - ')[0]: chapter for chapter in eng_chapters}

    prompt = "Provide the information as a JSON object with appropriate fields."

    openai_client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        organization=os.getenv("OPENAI_ORG_ID"),
        project=os.getenv("OPENAI_PROJECT_ID"),
    )
    
    for i in range(174, 946):
        print(f"Processing Chapter {i}")
        
        try:
            english_chapter_path = eng_chapters[f'Chapter_{i:03d}']
            russian_chapter_path = rus_chapters[f'Глава_{i:03d}']
        except KeyError:
            print(f"Chapter {i} not found.")
            continue
        
        with open(english_chapter_path, 'r', encoding='utf-8') as file:
            english_chapter_text = file.read()
        
        with open(russian_chapter_path, 'r', encoding='utf-8') as file:
            russian_chapter_text = file.read()
            
        json_data = get_translation_names(openai_client, english_chapter_text, russian_chapter_text, i)
        
        with open(f'word_translation_parser_responses/Chapter_{i:03d}.json', 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
        # Process the JSON data as needed