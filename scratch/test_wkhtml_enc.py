import subprocess

html = """<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<meta charset="utf-8"/>
</head>
<body>
<h1>Numéro de facture : GM/2026/0016</h1>
<p>Ministère de l'Économie et des Finances</p>
<p>Échéance : 2026-10-13</p>
</body>
</html>"""

with open('/tmp/test_enc.html', 'w', encoding='utf-8') as f:
    f.write(html)

subprocess.run(['wkhtmltopdf', '--encoding', 'utf-8', '/tmp/test_enc.html', '/tmp/test_enc.pdf'])
print("Generated /tmp/test_enc.pdf")
