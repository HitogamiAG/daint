import json
import os, glob
import time
import xml.etree.ElementTree as ET

translated_chapters = glob.glob('chapters_translated\*.txt')
translated_chapters = {os.path.basename(chapter).split(' - ')[0]: chapter for chapter in translated_chapters}

def open_chapter(chapter):
    with open(chapter, 'r', encoding='utf-8') as file:
        return file.readlines()

def filter_rows(chapter):
    chapter = [row for row in chapter if row.strip()]
    chapter = [row.replace('**', '') for row in chapter]
    return chapter


def create_fb2(chapter_headers, chapters, title="Untitled Book", author="Unknown Author", filename="output.fb2"):
    # Create root element
    root = ET.Element("FictionBook", xmlns="http://www.gribuser.ru/xml/fictionbook/2.0")
    
    # Create description
    description = ET.SubElement(root, "description")
    title_info = ET.SubElement(description, "title-info")
    ET.SubElement(title_info, "book-title").text = title
    author_elem = ET.SubElement(title_info, "author")
    ET.SubElement(author_elem, "first-name").text = author.split()[0] if " " in author else author
    ET.SubElement(author_elem, "last-name").text = author.split()[-1] if " " in author else ""
    
    # Create body with chapters
    body = ET.SubElement(root, "body")
    for chapter_header, chapter_text in zip(chapter_headers, chapters):
        section = ET.SubElement(body, "section")
        title_elem = ET.SubElement(section, "title")
        ET.SubElement(title_elem, "p").text = chapter_header
        for paragraph_text in chapter_text:
            paragraph = ET.SubElement(section, "p")
            paragraph.text = paragraph_text
    
    # Convert to XML string and save
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)  # Pretty print XML (Python 3.9+)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    
    print(f"FB2 file saved as {filename}")

start_chapter = 1086
end_chapter = 1140

chapters_headers = []
chapters_text = []
for i in range(start_chapter, end_chapter+1):
    translated_chapter_path = translated_chapters[f'Chapter_{i:03d}']
    translated_chapter = open_chapter(translated_chapter_path)
    translated_chapter = filter_rows(translated_chapter)

    chapters_headers.append(f'Глава {i}')
    chapters_text.append(translated_chapter)
    
create_fb2(chapters_headers, chapters_text,
            title=f"Shadow Slave - Главы {start_chapter}-{end_chapter}",
            author="Shadow Slave",
            filename=f"shadow_slave_{start_chapter}_{end_chapter}.fb2")