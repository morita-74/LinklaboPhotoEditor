import os
import re

directory = r'c:\Users\etern\OneDrive\完成データー\Antigravity\Linklabo'
html_files = [f for f in os.listdir(directory) if f.endswith('.html') and f != 'index.html']

def final_aggressive_cleanup(content):
    # Match script body
    match = re.search(r'(<script type="text/babel">)(.*?)(</script>)', content, re.DOTALL)
    if not match:
        return content

    header = match.group(1)
    body = match.group(2)
    footer = match.group(3)

    # 1. Deduplicate 'function App()'
    parts = re.split(r'function App\(\)', body)
    if len(parts) > 2:
        # Keep everything before first App, then keep the LAST App's code
        header_stuff = parts[0]
        actual_code = "function App()" + parts[-1]
        body = header_stuff + actual_code
        print("  - Deduplicated App")

    # 2. Deduplicate 'ReactDOM.createRoot'
    # Find all root render blocks and keep only the last one
    render_marker_regex = r'const root = ReactDOM\.createRoot'
    render_marker_raw = 'const root = ReactDOM.createRoot'
    render_parts = re.split(render_marker_regex, body)
    if len(render_parts) > 2:
        # Keep everything before the first marker, and append the last render block code
        before_all = render_parts[0]
        last_block_code = render_marker_raw + render_parts[-1]
        body = before_all + last_block_code
        print("  - Deduplicated Root Render (Aggressive)")

    # 3. Fix ?key= issue again just in case
    body = re.sub(r'\$\{url\}\?key=\$[\{][^}]+[\}]', r'${url}', body)
    body = re.sub(r'fetch\([$`"\']?/?api/ai[`"\']?\s*\+\s*[`"\']\?key=[\$]?\{?[a-zA-Z0-9_]+\}[`"\']', 'fetch("/api/ai"', body)

    # 4. Icon name.toLowerCase() consistency
    body = body.replace('data-lucide={name}', 'data-lucide={name.toLowerCase()}')

    return content[:match.start()] + header + body + footer + content[match.end():]

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = final_aggressive_cleanup(content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Aggressively Cleaned: {filename}")
