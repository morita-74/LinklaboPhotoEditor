import os
import re

directory = r'c:\Users\etern\OneDrive\完成データー\Antigravity\Linklabo'
html_files = [f for f in os.listdir(directory) if f.endswith('.html') and f != 'index.html']

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Robust API Proxy replacement
    # 1. Models with predict?key=
    new_content = re.sub(r'https://generativelanguage.googleapis.com/v1beta/models/[^?]+\?key=[\$]?\{?[a-zA-Z0-9_]+\}?', '/api/ai', content)
    # 2. Models with generateContent?key=
    new_content = re.sub(r'https://generativelanguage.googleapis.com/v1beta/models/[^:]+:[^?]+\?key=[\$]?\{?[a-zA-Z0-9_]+\}?', '/api/ai', new_content)
    # 3. Simple API strings in backticks or quotes
    new_content = re.sub(r'https://generativelanguage.googleapis.com/v1beta/models/[^"`\'`\s]+', '/api/ai', new_content)

    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Sanitized: {filename}")
