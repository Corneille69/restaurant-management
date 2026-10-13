import re

with open('odoo_addon/restaurant_core/views/report_invoice.xml', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'<template[^>]*id=[\'\"]([^\'\"]+)[\'\"]', text)
print('Templates found in report_invoice.xml:')
for m in matches:
    print(f" - {m}")
