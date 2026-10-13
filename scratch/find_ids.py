import re

with open('backend/app/web/router.py', 'r', encoding='utf-8') as f:
    content = f.read()

ids = re.findall(r'document\.getElementById\([\'\"]([^\'\"]+)[\'\"]\)', content)
relevant_ids = [i for i in ids if any(k in i.lower() for k in ['inv', 'print', 'dgi', 'modal', 'rec'])]
print('Total matching IDs:', len(relevant_ids))
print('Unique matching IDs:')
for i in sorted(set(relevant_ids)):
    print(f'  {i}')
