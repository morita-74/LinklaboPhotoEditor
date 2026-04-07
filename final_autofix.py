import os
import re

directory = r'c:\Users\etern\OneDrive\完成データー\Antigravity\Linklabo'
html_files = [f for f in os.listdir(directory) if f.endswith('.html') and f != 'index.html']

def fix_duplicate_app(content):
    # Match everything between <script type="text/babel"> and </script>
    match = re.search(r'(<script type="text/babel">)(.*?)(</script>)', content, re.DOTALL)
    if not match:
        return content

    header = match.group(1)
    script_body = match.group(2)
    footer = match.group(3)

    # 1. Fix duplicate App definitions
    # Find all occurrences of "function App()"
    app_indices = [m.start() for m in re.finditer(r'function App\(\)', script_body)]
    if len(app_indices) > 1:
        # Keep the content before the FIRST App, but then use the code from the LAST App onwards
        # In this project's specific breakage, the redundant part is usually a block starting from the first "function App()"
        # up until just before the final "root.render" or another "function App()"
        first_app_idx = app_indices[0]
        last_app_idx = app_indices[-1]
        
        # Keep the header stuff (Icon, Lucide)
        header_stuff = script_body[:first_app_idx]
        # Keep the ACTUAL App code
        actual_app_code = script_body[last_app_idx:]
        
        script_body = header_stuff + actual_app_code
        print("  - Removed duplicate App definition")

    # 2. Fix fetch("${url}?key=${apiKey}") if url is /api/ai
    # Find all fetch calls that add ?key= to /api/ai
    script_body = re.sub(r'fetch\([$`"\']?/?api/ai[`"\']?\s*\+\s*[`"\']\?key=[\$]?\{?[a-zA-Z0-9_]+\}[`"\']', 'fetch("/api/ai"', script_body)
    script_body = re.sub(r'fetch\(`\$\{url\}\?key=\$\{apiKey\}`', 'fetch(url', script_body)
    script_body = re.sub(r'fetch\(`\$\{url\}\?key=\$\{API_KEY\}`', 'fetch(url', script_body)
    script_body = re.sub(r'\$\{url\}\?key=\$[\{][^}]+[\}]', r'${url}', script_body)

    # 3. Final cleanup of any raw Gemini URLs that might have leaked back
    script_body = re.sub(r'https://generativelanguage.googleapis.com/v1beta/models/[^"`\'`\s]+', '/api/ai', script_body)

    # 4. Consistency for crypto.randomUUID (Add polyfill or manual if missing?)
    # But for now let's just make sure it's valid
    
    return content[:match.start()] + header + script_body + footer + content[match.end():]

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = fix_duplicate_app(content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed: {filename}")
