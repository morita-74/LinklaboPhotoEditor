import os
import re

directory = r'c:\Users\etern\OneDrive\完成データー\Antigravity\Linklabo'
html_files = [f for f in os.listdir(directory) if f.endswith('.html') and f != 'index.html']

def fix_missing_destructuring(content):
    # Find the Lucide object definition
    lucide_match = re.search(r'const Lucide = \{(.*?)\};', content, re.DOTALL)
    if not lucide_match:
        return content
    
    # Extract all keys from the Lucide object
    keys = re.findall(r'([a-zA-Z0-9_]+):', lucide_match.group(1))
    if not keys:
        return content
    
    destructuring_line = f"        const {{ {', '.join(keys)} }} = Lucide;"
    
    # Check if destructuring already exists
    if f"const {{ {keys[0]}" in content or "const { Sparkles" in content:
        # Already has some destructuring, might be partial or different. 
        # For safety, let's replace any existing one or insert after the object.
        content = re.sub(r'const \{ [a-zA-Z0-9_, ]+ \} = Lucide;', '', content)

    # Insert after the Lucide object
    new_content = content.replace(lucide_match.group(0), lucide_match.group(0) + "\n\n" + destructuring_line)
    return new_content

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = fix_missing_destructuring(content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed Destructuring: {filename}")
