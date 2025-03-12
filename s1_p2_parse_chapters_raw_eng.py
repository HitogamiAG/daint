import re

def extract_chapter_info(s):
    match = re.match(r'Chapter (\d+):\s*(.*)', s)
    if match:
        return int(match.group(1)), match.group(2)
    return None

with open('raw_chapters_eng\9kafe.com-shadow-slave-vol6-c1061-c1230.txt', 'r', encoding="utf8") as f:
    lines = f.readlines()
    lines = [x.strip() for x in lines]
    lines = [x for x in lines if len(x) > 0]
    
    chapter_headers = []
    chapters = []
    for line in lines:
        chapter_header = extract_chapter_info(line)
        
        if chapter_header:
            if len(chapters) and len(chapters[-1]) == 0:
                print(f'Removing empty chapter: {chapter_headers[-1]}')
                chapters.pop()
                chapter_headers.pop()
            chapter_headers.append(chapter_header)
            print(f'Found chapter: {chapter_header}')
            chapters.append([])
        else:
            chapters[-1].append(line)

for chapter_header, chapter_content in zip(chapter_headers, chapters):
    chapter_number, chapter_title = chapter_header
    with open(f'chapters_eng/Chapter_{chapter_number:03d} - {chapter_title}.txt'.replace('*', '').replace(',', '').replace('?', '').replace('!', '').replace(':', ''),
              'w', encoding="utf8") as f:
        f.write('\n'.join(chapter_content))