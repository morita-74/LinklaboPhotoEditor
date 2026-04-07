import os

directory = r'c:\Users\etern\OneDrive\完成データー\Antigravity\Linklabo'
html_files = [f for f in os.listdir(directory) if f.endswith('.html')]

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    if 'crypto.randomUUID()' in content:
        content = content.replace('crypto.randomUUID()', 'generateId()')
        if 'const generateId = () => Math.random().toString(36).substring(2, 9);' not in content:
            # Insert generateId definition
            content = content.replace('const { useState,', 'const generateId = () => Math.random().toString(36).substring(2, 9);\n        const { useState,')
        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed randomUUID: {filename}")
