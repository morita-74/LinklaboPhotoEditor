import os
import re

directory = r'c:\Users\etern\OneDrive\完成データー\Antigravity\Linklabo'
html_files = [f for f in os.listdir(directory) if f.endswith('.html') and f != 'index.html']

def fix_duplicate_destructuring(content):
    # Find the destructuring line
    match = re.search(r'const \{ (.*?) \} = Lucide;', content)
    if not match:
        return content
    
    keys = [k.strip() for k in match.group(1).split(',')]
    unique_keys = []
    seen = set()
    for k in keys:
        if k not in seen:
            unique_keys.append(k)
            seen.add(k)
    
    new_line = f"        const {{ {', '.join(unique_keys)} }} = Lucide;"
    return content.replace(match.group(0), new_line)

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = fix_duplicate_destructuring(content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Cleaned Destructuring: {filename}")
