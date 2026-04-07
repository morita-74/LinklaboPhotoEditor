import os
import re

# Reuse the conversion logic but specialized for the new files
def convert_react_to_standalone(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    body_lines = []
    for line in lines:
        if line.startswith('import ') or line.startswith('// import'):
            continue
        body_lines.append(line)
    
    body_code = "\n".join(body_lines)
    body_code = body_code.replace('export default function', 'function')
    body_code = body_code.replace('export default App', '')
    body_code = body_code.replace('const App = () =>', 'function App()')

    match = re.search(r'function (\w+)\(\)', body_code)
    component_name = match.group(1) if match else "App"

    # API Proxy conversion
    body_code = re.sub(r'const url = `https://generativelanguage.googleapis.com/v1beta/models/[^`]+`;', 'const url = "/api/ai";', body_code)
    body_code = re.sub(r'https://generativelanguage.googleapis.com/v1beta/models/[^?]+\?key=[\$]?\{?apiKey\}?', '/api/ai', body_code)
    body_code = re.sub(r'https://generativelanguage.googleapis.com/v1beta/models/[^?]+\?key=[\$]?\{?API_KEY\}?', '/api/ai', body_code)

    standalone_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{component_name} - Linklabo AI Tool</title>
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {{ font-family: 'Inter', sans-serif; }}
    </style>
</head>
<body class="bg-slate-900 text-slate-100">
    <div id="root"></div>

    <script type="text/babel">
        const {{ useState, useRef, useEffect, useMemo }} = React;

        const Icon = ({{ name, size = 24, className = "" }}) => {{
            const ref = useRef(null);
            useEffect(() => {{
                if (ref.current && window.lucide) {{
                    const icon = lucide.icons[name];
                    if (icon) {{
                        lucide.createIcons({{
                            icons: {{ [name]: icon }},
                            nameAttr: 'data-lucide',
                            attrs: {{ 'stroke-width': 2, width: size, height: size, class: className }}
                        }});
                    }}
                }}
            }}, [name, size, className]);
            return <i ref={{ref}} data-lucide={{name}} className={{className}} style={{ {{ width: size, height: size, display: 'inline-block' }} }}></i>;
        }};

        const Lucide = {{
            UploadCloud: (props) => <Icon name="UploadCloud" {{...props}} />,
            ImagePlus: (props) => <Icon name="ImagePlus" {{...props}} />,
            Save: (props) => <Icon name="Save" {{...props}} />,
            RefreshCw: (props) => <Icon name="RefreshCw" {{...props}} />,
            Loader2: (props) => <Icon name="Loader2" {{...props}} />,
            Sparkles: (props) => <Icon name="Sparkles" {{...props}} />,
            X: (props) => <Icon name="X" {{...props}} />,
            MessageSquare: (props) => <Icon name="MessageSquare" {{...props}} />,
            Pencil: (props) => <Icon name="Pencil" {{...props}} />,
            Upload: (props) => <Icon name="Upload" {{...props}} />,
            Download: (props) => <Icon name="Download" {{...props}} />,
            Trash2: (props) => <Icon name="Trash2" {{...props}} />,
            Edit: (props) => <Icon name="Edit" {{...props}} />,
            RefreshCw: (props) => <Icon name="RefreshCw" {{...props}} />,
            Search: (props) => <Icon name="Search" {{...props}} />,
        }};

        // Main code
        {body_code}

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<{component_name} />);
    </script>
</body>
</html>"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(standalone_html)

files_to_convert = ["box.html", "Ukiyoe.html"]
directory = r'c:\Users\etern\OneDrive\完成データー\Antigravity\Linklabo'
for filename in files_to_convert:
    path = os.path.join(directory, filename)
    if os.path.exists(path):
        convert_react_to_standalone(path)
        print(f"Converted: {filename}")
