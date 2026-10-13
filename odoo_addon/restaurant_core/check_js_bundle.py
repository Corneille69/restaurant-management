import requests

s = requests.Session()
r_login = s.get('http://localhost:8070/web/login')
csrf = ''
for line in r_login.text.splitlines():
    if 'csrf_token' in line and 'value=' in line:
        csrf = line.split('value=')[1].split('"')[1]
        break

s.post('http://localhost:8070/web/login', data={'login':'admin', 'password':'admin', 'csrf_token':csrf})
r_web = s.get('http://localhost:8070/web')

print("Backend scripts:")
for line in r_web.text.splitlines():
    if 'script' in line and 'src=' in line:
        print(" -", line.strip())
        parts = line.split('src="')
        if len(parts) > 1:
            href = parts[1].split('"')[0]
            url = 'http://localhost:8070' + href
            r_js = s.get(url)
            print(f"   [{r_js.status_code}] len: {len(r_js.text)}")
            if 'disable_odoobot' in r_js.text:
                print("   -> FOUND disable_odoobot in", href)
            if 'canPromptToInstall' in r_js.text:
                print("   -> FOUND canPromptToInstall in", href)
