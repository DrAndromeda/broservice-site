import re

with open('/tmp/bro_raw.html', 'r') as f:
    html = f.read()

phone = re.search(r'tel:(\d+)', html)
phone = phone.group(1) if phone else '0932704696'
phone_fmt = f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"

# Extract services
lists = re.findall(r'<li[^>]*>(.*?)</li>', html, re.DOTALL)
all_services = []
for l in lists:
    clean = re.sub(r'<[^>]+>', '', l).strip()
    clean = re.sub(r'&nbsp;', ' ', clean)
    if clean and len(clean) > 3:
        all_services.append(clean)

real_services = []
for s in all_services:
    if any(k in s.lower() for k in ['ремонт','прокат','вызов','электрик','сантехник','холодильник','скутер','велосипед','ноутбук','компьютер','мопед','мотоцикл','шлем','аренд']):
        real_services.append(s)

# Extract paragraphs
body = html[html.find('<section'):html.find('<footer')]
body_clean = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
texts = re.findall(r'<p[^>]*>(.*?)</p>', body_clean, re.DOTALL)
paragraphs = []
for t in texts:
    clean = re.sub(r'<[^>]+>', '', t).strip()
    clean = re.sub(r'&nbsp;', ' ', clean)
    if clean and len(clean) > 50:
        paragraphs.append(clean)

svc_map = {
    'велосипед': ('🚲', 'Ремонт та обслуговування'),
    'скутер': ('🛴', 'Ремонт скутерів, мопедів'),
    'мотоцикл': ('🏍️', 'Ремонт та обслуговування'),
    'ноутбук': ('💻', 'Ремонт та налаштування'),
    'телефон': ('📱', 'Ремонт телефонів'),
    'пральн': ('🔧', 'Ремонт побутової техніки'),
    'сантехнік': ('🚿', 'Сантехнічні послуги'),
    'електрик': ('⚡', 'Електромонтажні роботи'),
    'прокат': ('📦', 'Прокат та оренда'),
    'холодильник': ('🔧', 'Ремонт холодильників'),
}

services_html = ''
for svc_text in real_services:
    matched = False
    for keyword, (icon, desc) in svc_map.items():
        if keyword.lower() in svc_text.lower():
            services_html += f'    <div class="card"><div class="icon">{icon}</div><h3>{svc_text}</h3><p>{desc}</p></div>\n'
            matched = True
            break
    if not matched and len(svc_text) < 80:
        services_html += f'    <div class="card"><div class="icon">✅</div><h3>{svc_text}</h3></div>\n'

about_html = ''
for p in paragraphs[:4]:
    about_html += f'    <p>{p}</p>\n'

# Background images as base64 data URIs (small geometric patterns)
# I'll use CSS gradients to replicate the original dark/industrial feel
bg_pattern = "background: #1a1414;"
header_bg = "background: linear-gradient(180deg, #2b2424 0%, #1f1919 100%);"
nav_bg = "background: linear-gradient(180deg, #e57c00 0%, #c47000 100%);"

page = f'''<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BroService — Сервісний центр у Броварах</title>
<style>
:root {{ --orange: #e88800; --orange-dark: #c47000; --dark: #1f1919; --gray: #8f8b8c; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font: 15px/1.6 system-ui, -apple-system, sans-serif;
  color: #333;
  min-height: 100vh;
}}
.bg {{
  background: #1a1414;
  background-image:
    radial-gradient(ellipse at 20% 50%, rgba(232,136,0,0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 50%, rgba(200,200,200,0.05) 0%, transparent 50%);
}}

.container {{ max-width: 1000px; margin: 0 auto; padding: 0 20px; }}

/* HEADER */
header {{
  background: linear-gradient(180deg, #2b2424 0%, #1f1919 100%);
  box-shadow: 0 2px 20px rgba(0,0,0,0.5);
  position: sticky; top: 0; z-index: 100;
}}
.header-inner {{
  display: flex; align-items: center;
  justify-content: space-between; flex-wrap: wrap;
  padding: 15px 20px; max-width: 1000px; margin: 0 auto;
}}
.logo h1 {{ font-size: 26px; color: #fff; }}
.logo h1 b {{ color: #d3d3d3; }}
.logo span {{ font-size: 13px; color: var(--orange); }}
nav ul {{ display: flex; list-style: none; gap: 4px; flex-wrap: wrap; }}
nav ul li a {{
  display: block; padding: 10px 18px; color: #fff;
  text-decoration: none; font-size: 14px; font-weight: 600;
  border-radius: 6px; transition: background 0.2s;
}}
nav ul li a:hover {{ background: rgba(0,0,0,0.25); }}
nav ul li a.active {{ background: var(--orange); box-shadow: 0 2px 8px rgba(0,0,0,0.3); }}

/* HERO */
.hero {{
  background: linear-gradient(135deg, #1f1919 0%, #2b2424 50%, #1f1919 100%);
  color: #fff; padding: 70px 0; text-align: center;
  position: relative; overflow: hidden;
}}
.hero::before {{
  content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background:
    radial-gradient(circle at 30% 50%, rgba(232,136,0,0.12) 0%, transparent 60%),
    radial-gradient(circle at 70% 50%, rgba(255,255,255,0.05) 0%, transparent 60%);
  pointer-events: none;
}}
.hero h2 {{ font-size: 36px; margin-bottom: 10px; position: relative; }}
.hero h2 span {{ color: var(--orange); }}
.hero p {{ color: #bbb; max-width: 600px; margin: 0 auto 25px; position: relative; }}
.hero-phone {{
  display: inline-block; background: linear-gradient(180deg, var(--orange), var(--orange-dark));
  color: #fff; padding: 14px 40px; border-radius: 8px; font-size: 22px;
  font-weight: bold; text-decoration: none; position: relative;
  box-shadow: 0 4px 15px rgba(232,136,0,0.3); transition: transform 0.2s;
}}
.hero-phone:hover {{ transform: scale(1.05); }}

/* SECTION */
.section {{ padding: 60px 0; }}
.section-title {{ text-align: center; font-size: 30px; color: var(--dark); margin-bottom: 40px; }}
.section-title span {{ color: var(--orange); }}

/* CARDS */
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
.card {{
  background: #fff; border-radius: 12px; padding: 25px;
  box-shadow: 0 2px 15px rgba(0,0,0,0.08);
  border-top: 4px solid var(--orange); transition: all 0.2s;
}}
.card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 25px rgba(0,0,0,0.12); }}
.card .icon {{ font-size: 36px; margin-bottom: 12px; }}
.card h3 {{ font-size: 16px; margin-bottom: 5px; }}
.card p {{ font-size: 13px; color: #888; }}

/* CONTENT */
.content {{ background: #fff; border-radius: 12px; padding: 35px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); }}
.content p {{ margin-bottom: 18px; text-align: justify; }}

/* CONTACTS */
.contacts {{ display: flex; flex-wrap: wrap; gap: 30px; justify-content: center; margin-top: 20px; }}
.c-item {{ text-align: center; min-width: 150px; }}
.c-item .ic {{ font-size: 30px; margin-bottom: 5px; }}
.c-item a {{ color: var(--orange); font-weight: 700; font-size: 18px; text-decoration: none; }}
.c-item a:hover {{ text-decoration: underline; }}
.c-item p {{ font-size: 14px; color: #888; }}

/* FOOTER */
footer {{
  background: var(--dark); color: var(--gray); text-align: center;
  padding: 30px 0; font-size: 13px;
}}
footer a {{ color: var(--orange); text-decoration: none; }}

@media (max-width: 768px) {{
  .header-inner {{ flex-direction: column; text-align: center; gap: 10px; }}
  nav ul {{ justify-content: center; }}
  .hero h2 {{ font-size: 26px; }}
}}
</style>
</head>
<body class="bg">

<header>
<div class="header-inner">
  <div class="logo">
    <h1><b>Bro</b>Service</h1>
    <span>Сервісний центр • Бровари</span>
  </div>
  <nav>
    <ul>
      <li><a href="#" class="active">Головна</a></li>
      <li><a href="#services">Послуги</a></li>
      <li><a href="#about">Про нас</a></li>
      <li><a href="#contacts">Контакти</a></li>
    </ul>
  </nav>
</div>
</header>

<section class="hero">
<div class="container">
  <h2>Сервісний центр <span>у Броварах</span></h2>
  <p>Ремонт, обслуговування та прокат техніки й транспорту. Швидко, якісно, з гарантією.</p>
  <a href="tel:{phone}" class="hero-phone">📞 {phone_fmt}</a>
</div>
</section>

<section class="section" id="services">
<div class="container">
  <h2 class="section-title">Наші <span>послуги</span></h2>
  <div class="grid">
{services_html}
  </div>
</div>
</section>

<section class="section" id="about" style="background:rgba(255,255,255,0.95);">
<div class="container">
  <h2 class="section-title">Про <span>BroService</span></h2>
  <div class="content">
{about_html}
  </div>
</div>
</section>

<section class="section" id="contacts">
<div class="container">
  <h2 class="section-title">Наші <span>контакти</span></h2>
  <div class="content" style="text-align:center;">
    <p style="font-size:18px;text-align:center;">Працюємо в Броварах та районі. Виїзд майстра додому.</p>
    <div class="contacts">
      <div class="c-item"><div class="ic">📞</div><a href="tel:{phone}">{phone_fmt}</a></div>
      <div class="c-item"><div class="ic">✉️</div><a href="mailto:info@broservice.com.ua">info@broservice.com.ua</a></div>
      <div class="c-item"><div class="ic">📍</div><p>м. Бровари<br>Київська область</p></div>
      <div class="c-item"><div class="ic">⏰</div><p>Пн-Сб: 9:00-19:00<br>Нд: домовленість</p></div>
      <div class="c-item"><div class="ic">💬</div><a href="viber://chat?number=380{phone}">Viber</a></div>
    </div>
  </div>
</div>
</section>

<footer>
<div class="container">
  <p>© 2015-2026 BroService — Сервісний центр у Броварах</p>
  <p>Ремонт • Прокат • Обслуговування</p>
</div>
</footer>

</body>
</html>'''

with open('/Users/andromeda/.openclaw/workspace/broservice_site/index_new.html', 'w') as f:
    f.write(page)

print(f"Created: {len(page)} bytes, {len(real_services)} services, {len(paragraphs)} paragraphs")