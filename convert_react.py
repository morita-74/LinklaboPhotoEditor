import os
import re

def convert_react_to_standalone(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extract the main component logic
    # Find the part between the last import and the end of the file
    # (Assuming everything after imports is the component code)
    lines = content.splitlines()
    body_lines = []
    in_component = False
    for line in lines:
        if line.startswith('import ') or line.startswith('// import'):
            continue
        body_lines.append(line)
    
    body_code = "\n".join(body_lines)
    
    # Remove 'export default'
    body_code = body_code.replace('export default function', 'function')
    
    # Identify the component name (usually App or LaserCheckApp etc.)
    match = re.search(r'function (\w+)\(\)', body_code)
    component_name = match.group(1) if match else "App"

    # 2. Fix the API URL and Prompt Logic
    # All tools should use /api/ai
    body_code = re.sub(r'const url = `https://generativelanguage.googleapis.com/v1beta/models/[^`]+`;', 'const url = "/api/ai";', body_code)
    body_code = re.sub(r'https://generativelanguage.googleapis.com/v1beta/models/[^?]+\?key=\${apiKey}', '/api/ai', body_code)
    body_code = re.sub(r'https://generativelanguage.googleapis.com/v1beta/models/[^?]+\?key=[\$]?\{?API_KEY\}?', '/api/ai', body_code)

    # 3. Create the standalone HTML template
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

        // --- Lucide Icon Helper ---
        // Replace Lucide components with a wrapper that uses lucide-static
        const Icon = ({{ name, size = 24, className = "" }}) => {{
            const ref = useRef(null);
            useEffect(() => {{
                if (ref.current) {{
                    const icon = lucide.icons[name];
                    if (icon) {{
                        const svg = lucide.createIcons({{
                            icons: {{ [name]: icon }},
                            nameAttr: 'data-lucide',
                            attrs: {{ 'stroke-width': 2, width: size, height: size, class: className }}
                        }});
                    }}
                }}
            }}, [name, size, className]);
            return <i ref={{ref}} data-lucide={{name.toLowerCase()}} className={{className}} style={{ {{ width: size, height: size, display: 'inline-block' }} }}></i>;
        }};

        // Mock Lucide components for the React code
        const Lucide = {{
            Upload: (props) => <Icon name="Upload" {{...props}} />,
            Download: (props) => <Icon name="Download" {{...props}} />,
            Wand2: (props) => <Icon name="Wand2" {{...props}} />,
            Image: (props) => <Icon name="Image" {{...props}} />,
            Sparkles: (props) => <Icon name="Sparkles" {{...props}} />,
            RefreshCw: (props) => <Icon name="RefreshCw" {{...props}} />,
            X: (props) => <Icon name="X" {{...props}} />,
            Palette: (props) => <Icon name="Palette" {{...props}} />,
            Zap: (props) => <Icon name="Zap" {{...props}} />,
            AlertTriangle: (props) => <Icon name="AlertTriangle" {{...props}} />,
            CheckCircle: (props) => <Icon name="CheckCircle" {{...props}} />,
            Info: (props) => <Icon name="Info" {{...props}} />,
            XCircle: (props) => <Icon name="XCircle" {{...props}} />,
            Settings: (props) => <Icon name="Settings" {{...props}} />,
            Printer: (props) => <Icon name="Printer" {{...props}} />,
            BarChart: (props) => <Icon name="BarChart" {{...props}} />,
            Layers: (props) => <Icon name="Layers" {{...props}} />,
            PaintBucket: (props) => <Icon name="PaintBucket" {{...props}} />,
            Eraser: (props) => <Icon name="Eraser" {{...props}} />,
            Maximize: (props) => <Icon name="Maximize" {{...props}} />,
            ZoomIn: (props) => <Icon name="ZoomIn" {{...props}} />,
            ZoomOut: (props) => <Icon name="ZoomOut" {{...props}} />,
            Scan: (props) => <Icon name="Scan" {{...props}} />,
            Flame: (props) => <Icon name="Flame" {{...props}} />,
            ChevronRight: (props) => <Icon name="ChevronRight" {{...props}} />,
            ChevronLeft: (props) => <Icon name="ChevronLeft" {{...props}} />,
            Languages: (props) => <Icon name="Languages" {{...props}} />,
            Copy: (props) => <Icon name="Copy" {{...props}} />,
            Check: (props) => <Icon name="Check" {{...props}} />,
            Type: (props) => <Icon name="Type" {{...props}} />,
            Volume2: (props) => <Icon name="Volume2" {{...props}} />,
            Mic: (props) => <Icon name="Mic" {{...props}} />,
            Send: (props) => <Icon name="Send" {{...props}} />,
            Trash2: (props) => <Icon name="Trash2" {{...props}} />,
            Plus: (props) => <Icon name="Plus" {{...props}} />,
            Minus: (props) => <Icon name="Minus" {{...props}} />,
            HelpCircle: (props) => <Icon name="HelpCircle" {{...props}} />,
            ShieldCheck: (props) => <Icon name="ShieldCheck" {{...props}} />,
            Lock: (props) => <Icon name="Lock" {{...props}} />,
            Eye: (props) => <Icon name="Eye" {{...props}} />,
            History: (props) => <Icon name="History" {{...props}} />,
            Share2: (props) => <Icon name="Share2" {{...props}} />,
            ShoppingCart: (props) => <Icon name="ShoppingCart" {{...props}} />,
            Heart: (props) => <Icon name="Heart" {{...props}} />,
            Star: (props) => <Icon name="Star" {{...props}} />,
            User: (props) => <Icon name="User" {{...props}} />,
            Mail: (props) => <Icon name="Mail" {{...props}} />,
            Phone: (props) => <Icon name="Phone" {{...props}} />,
            MapPin: (props) => <Icon name="MapPin" {{...props}} />,
            Calendar: (props) => <Icon name="Calendar" {{...props}} />,
            Clock: (props) => <Icon name="Clock" {{...props}} />,
            Tag: (props) => <Icon name="Tag" {{...props}} />,
            Search: (props) => <Icon name="Search" {{...props}} />,
            Filter: (props) => <Icon name="Filter" {{...props}} />,
            SortAsc: (props) => <Icon name="SortAsc" {{...props}} />,
            SortDesc: (props) => <Icon name="SortDesc" {{...props}} />,
            MoreHorizontal: (props) => <Icon name="MoreHorizontal" {{...props}} />,
            MoreVertical: (props) => <Icon name="MoreVertical" {{...props}} />,
            Grid: (props) => <Icon name="Grid" {{...props}} />,
            List: (props) => <Icon name="List" {{...props}} />,
            ExternalLink: (props) => <Icon name="ExternalLink" {{...props}} />,
            Ghost: (props) => <Icon name="Ghost" {{...props}} />,
            Scissors: (props) => <Icon name="Scissors" {{...props}} />,
            Briefcase: (props) => <Icon name="Briefcase" {{...props}} />,
            Coins: (props) => <Icon name="Coins" {{...props}} />,
            MessageSquare: (props) => <Icon name="MessageSquare" {{...props}} />,
            Edit3: (props) => <Icon name="Edit3" {{...props}} />,
            FileText: (props) => <Icon name="FileText" {{...props}} />,
            EyeOff: (props) => <Icon name="EyeOff" {{...props}} />,
            Moon: (props) => <Icon name="Moon" {{...props}} />,
            Sun: (props) => <Icon name="Sun" {{...props}} />,
            Menu: (props) => <Icon name="Menu" {{...props}} />,
            Smartphone: (props) => <Icon name="Smartphone" {{...props}} />,
            Instagram: (props) => <Icon name="Instagram" {{...props}} />,
            Facebook: (props) => <Icon name="Facebook" {{...props}} />,
            Twitter: (props) => <Icon name="Twitter" {{...props}} />,
            Chrome: (props) => <Icon name="Chrome" {{...props}} />,
            CreditCard: (props) => <Icon name="CreditCard" {{...props}} />,
            PlusCircle: (props) => <Icon name="PlusCircle" {{...props}} />,
            MinusCircle: (props) => <Icon name="MinusCircle" {{...props}} />,
            Layout: (props) => <Icon name="Layout" {{...props}} />,
            Box: (props) => <Icon name="Box" {{...props}} />,
            Brush: (props) => <Icon name="Brush" {{...props}} />,
            Gem: (props) => <Icon name="Gem" {{...props}} />,
            Coffee: (props) => <Icon name="Coffee" {{...props}} />,
            Code: (props) => <Icon name="Code" {{...props}} />,
            Music: (props) => <Icon name="Music" {{...props}} />,
            Video: (props) => <Icon name="Video" {{...props}} />,
            Play: (props) => <Icon name="Play" {{...props}} />,
            Pause: (props) => <Icon name="Pause" {{...props}} />,
            Link: (props) => <Icon name="Link" {{...props}} />,
        }};

        // Replace direct Lucide imports in the original code
        // {body_code.replace(' lucide-react', ' Lucide')}

        // Render the app
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<{component_name} />);
    </script>
</body>
</html>"""

    # Final replacement for Lucide tags in body_code
    # The original code likely has <Upload ..., <Download ... which we mapped to <Lucide.Upload ...
    # Wait, the easiest way is to define constants for each icon.
    
    icons_to_define = [
        "Upload", "Download", "Wand2", "Image", "Sparkles", "RefreshCw", "X", "Palette", "Zap",
        "AlertTriangle", "CheckCircle", "Info", "XCircle", "Settings", "Printer", "BarChart",
        "Layers", "PaintBucket", "Eraser", "Maximize", "ZoomIn", "ZoomOut", "Scan", "Flame",
        "ChevronRight", "ChevronLeft", "Languages", "Copy", "Check", "Type", "Volume2", "Mic",
        "Send", "Trash2", "Plus", "Minus", "HelpCircle", "ShieldCheck", "Lock", "Eye", "History",
        "Share2", "ShoppingCart", "Heart", "Star", "User", "Mail", "Phone", "MapPin", "Calendar",
        "Clock", "Tag", "Search", "Filter", "SortAsc", "SortDesc", "MoreHorizontal", "MoreVertical",
        "Grid", "List", "ExternalLink", "Ghost", "Scissors", "Briefcase", "Coins", "MessageSquare",
        "Edit3", "FileText", "EyeOff", "Moon", "Sun", "Menu", "Smartphone", "Instagram", "Facebook",
        "Twitter", "Chrome", "CreditCard", "PlusCircle", "MinusCircle", "Layout", "Box", "Brush",
        "Gem", "Coffee", "Code", "Music", "Video", "Play", "Pause", "Link"
    ]
    
    icon_defs = "\n        ".join([f"const {icon} = Lucide.{icon};" for icon in icons_to_define])
    
    # Special fix for 'Image' since it conflicts with global Image constructor
    # We rename it to 'ImageIcon' in mapping if needed, but original code might have 'ImageIcon'
    body_code = body_code.replace(' lucide-react', ' Lucide')
    
    final_standalone = standalone_html.replace('// Render the app', f"{icon_defs}\n\n        {body_code}\n\n        const root = ReactDOM.createRoot(document.getElementById('root'));\n        root.render(<{component_name} />);")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_standalone)

# Target files from grep results
files_to_convert = [
    "anime.html", "Bookmark.html", "Charm.html", "check.html", "Comment.html", "copy.html", "Copyright.html", 
    "dougu.html", "email.html", "Eyes looking forward.html", "Fortune-telling.html", 
    "Googly eyes - Back side.html", "Instagram.html", "Mercari.html", "oekaki.html"
]

directory = r'c:\Users\etern\OneDrive\完成データー\Antigravity\Linklabo'
for filename in files_to_convert:
    path = os.path.join(directory, filename)
    if os.path.exists(path):
        try:
            convert_react_to_standalone(path)
            print(f"Converted to standalone: {filename}")
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")
