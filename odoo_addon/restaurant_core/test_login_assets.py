import requests

r_login = requests.get('http://localhost:8070/web/login')
print('Login status:', r_login.status_code)
lines = [l for l in r_login.text.splitlines() if 'web.assets_frontend.min.css' in l]
if lines:
    link = lines[0]
    href = link.split('href=')[1].split('>')[0].strip('"\' /')
    css_url = 'http://localhost:8070/' + href
    r_css = requests.get(css_url)
    print('CSS URL:', css_url)
    print('CSS Status:', r_css.status_code)
    print('714B67 in CSS:', '#714b67' in r_css.text.lower())
    print('fffde7 in CSS:', '#fffde7' in r_css.text.lower())
    print('card.o_database_list in CSS:', 'card.o_database_list' in r_css.text)
    print('oe_login_buttons in CSS:', 'oe_login_buttons' in r_css.text)
