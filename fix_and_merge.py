import re

# Read files
with open('/Users/andromeda/.openclaw/workspace/broservice_site/original_clean.html', 'r') as f:
    html = f.read()

with open('/tmp/bro_css_raw.css', 'r') as f:
    css = f.read()

# Clean CSS - replace all image backgrounds with solid/gradient
# Remove all url() references
css = re.sub(r'url\([^)]*\)', '', css)

# Remove Wayback comments
css = re.sub(r'<!--.*?-->', '', css, flags=re.DOTALL)

# Remove extra CSS junk (ping-pong, etc)
css = re.sub(r'@import[^;]*;', '', css)
css = re.sub(r'@keyframes.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'#ping.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'#pong.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'#c[1-4].*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'#b[1-4].*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'#pingpong.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'#table.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'#net-.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'#line.*?\n\}', '', css, flags=re.DOTALL)
css = re.sub(r'BACKGROUND_PLACEHOLDER', '', css)

# Fix image paths to point locally
css = css.replace('../images/', './assets/images/')

# Remove extra empty lines
css = re.sub(r'\n\s*\n+', '\n', css)

# Add modern replacement CSS for missing images
modern_css = '''
/* === FIXES FOR MISSING ORIGINAL IMAGES === */
body { background: #1a1414 !important; }
header { background: linear-gradient(180deg, #2b2424, #1f1919) !important; }
nav { background: linear-gradient(180deg, #e57c00, #c47000) !important; }
.nav-shadow > div { background: linear-gradient(180deg, #e57c00, #c47000) !important; }
a.button, a.button-1 { background: #e88800 !important; border: none !important; }
a.button:hover { background: #1f1919 !important; }
#upbutton { background: #e88800 !important; display: none !important; }
ul.menu li { background: none !important; }
.block-1 { background: transparent !important; }
.header-content { background: #edeef0 !important; }
.border-1, .border-2 { background: none !important; }
#form input, #form textarea { background: #fff !important; }
.circle, .circle1, .circle2 { background: #e88800 !important; }
'''

final_css = css + '\n' + modern_css

# Remove external CSS link
html = re.sub(r'<link[^>]*style\.css[^>]*>', '', html)

# Insert CSS inline before </head>
html = html.replace('</head>', f'<style>\n{final_css}\n</style>\n</head>')

# Remove any remaining <link> to IE css
html = re.sub(r'<link[^>]*ie\.css[^>]*>', '', html)

with open('/Users/andromeda/.openclaw/workspace/broservice_site/index.html', 'w') as f:
    f.write(html)

print(f"Final: {len(html)} bytes")
print("CSS inlined into index.html")