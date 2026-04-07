import os

directory = r'c:\Users\etern\OneDrive\完成データー\Antigravity\Linklabo'
html_files = [f for f in os.listdir(directory) if f.endswith('.html')]

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content.replace('ReactDOM\\.createRoot', 'ReactDOM.createRoot')
    new_content = new_content.replace('data-lucide={name.toLowerCase()}', 'data-lucide={name.toLowerCase()}')

    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed Escapes: {filename}")
