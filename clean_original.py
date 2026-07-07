import re

with open('/tmp/bro_id.html', 'r') as f:
    html = f.read()

# Remove Wayback scripts
html = re.sub(r'<script[^>]*web-static\.archive[^>]*>.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<script>window\.RufflePlayer.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'__wm\.\w+[^;]*;', '', html)
html = re.sub(r'<base[^>]*>', '', html)

# Fix URL prefixes
html = html.replace('/web/20170531070103cs_/http://broservice.com.ua/', '')
html = html.replace('/web/20170531070103js_/http://broservice.com.ua/', '')
html = html.replace('/web/20170531070103im_/http://broservice.com.ua/', '')
html = html.replace('//web.archive.org/web/20170531070103js_/', '')
html = html.replace('//web.archive.org/web/20170531070103cs_/', '')

# Fix Google CDN
html = html.replace('//ajax.googleapis.com', 'https://ajax.googleapis.com')

# Fix asset paths
html = html.replace('assets/templates/Free%20Website%20Template%20Security%20Project/', 'assets/')
html = html.replace('assets/templates/Free Website Template Security Project/', 'assets/')
html = html.replace('href="css/', 'href="assets/css/')
html = html.replace('src="js/', 'src="assets/js/')
html = html.replace('http://broservice.com.ua/', '/')

# Remove Yandex
html = re.sub(r'<!-- Yandex\.Metrika counter -->.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<script[^>]*>[\s\S]*?yaCounter[\s\S]*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<noscript>.*?</noscript>', '', html, flags=re.DOTALL)

# Remove VK
html = re.sub(r'<a[^>]*vk\.com[^>]*>.*?</a>', '', html, flags=re.DOTALL)
html = html.replace('https://plus.google.com/u/0/b/103623959270045742066/103623959270045742066/about', '#')

# Remove comments
html = re.sub(r'<!--\s*playback timings.*?-->', '', html, flags=re.DOTALL)
html = re.sub(r'<!--\s*FILE ARCHIVED.*?-->', '', html, flags=re.DOTALL)
html = re.sub(r'<!--\[if lt IE 8\]>.*?<!\[endif\]-->', '', html, flags=re.DOTALL)
html = re.sub(r'<!--\[if lt IE 9\]>.*?<!\[endif\]-->', '', html, flags=re.DOTALL)

# Remove GA
html = re.sub(r'<script>[\s\S]*?GoogleAnalytics[\s\S]*?</script>', '', html, flags=re.DOTALL)

# Remove empty script
html = re.sub(r'<script>[\s\n ]*</script>', '', html)

with open('/Users/andromeda/.openclaw/workspace/broservice_site/original_clean.html', 'w') as f:
    f.write(html)

print(f"Clean: {len(html)} bytes")
print("Saved: original_clean.html")