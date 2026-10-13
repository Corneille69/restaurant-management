import xml.etree.ElementTree as ET

xml_path = "odoo_addon/restaurant_core/views/report_invoice.xml"
with open(xml_path, "r", encoding="utf-8") as f:
    text = f.read()

# Fix the stray </t>
text = text.replace("                            \n                            </t>\n                        </tbody>", "                        </tbody>")

with open(xml_path, "w", encoding="utf-8") as f:
    f.write(text)

try:
    tree = ET.parse(xml_path)
    print("SUCCESS: XML is 100% syntactically valid!")
except ET.ParseError as e:
    print(f"Parse error at {e.position}: {e}")
    lines = text.splitlines()
    line_num = e.position[0]
    for idx in range(max(0, line_num - 5), min(len(lines), line_num + 5)):
        print(f"Line {idx+1}: {lines[idx]}")
