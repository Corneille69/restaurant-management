import subprocess
import tempfile
import PyPDF2

html1 = "<div>Numéro de facture: GM/2026/0016 - Échéance - Référence</div>"
with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
    f.write(html1.encode('utf-8'))
    p1 = f.name
subprocess.run(['wkhtmltopdf', '--quiet', p1, p1 + '.pdf'])
r1 = PyPDF2.PdfFileReader(open(p1 + '.pdf', 'rb'))
print('WITHOUT META:', repr(r1.getPage(0).extractText()))

html2 = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/><meta charset="utf-8"/></head><body><div>Numéro de facture: GM/2026/0016 - Échéance - Référence</div></body></html>'
with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
    f.write(html2.encode('utf-8'))
    p2 = f.name
subprocess.run(['wkhtmltopdf', '--quiet', p2, p2 + '.pdf'])
r2 = PyPDF2.PdfFileReader(open(p2 + '.pdf', 'rb'))
print('WITH META:', repr(r2.getPage(0).extractText()))
