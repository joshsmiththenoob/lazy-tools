from bs4 import BeautifulSoup

input_file = r"C:\Users\ai\Desktop\smithfu\repositories\lazy-tools\html_pdf_converter\intput\2026-03-23-ZAP-Report-localhost.html"
output_file = r"C:\Users\ai\Desktop\smithfu\repositories\lazy-tools\html_pdf_converter\output\2026-03-23-ZAP-Report-no-medium.html"

with open(input_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# 刪除 Alerts 裡面的 Medium 區塊
for alert_id in [
    "alerts--risk-2-confidence-3",
    "alerts--risk-2-confidence-2",
]:
    tag = soup.find(id=alert_id)
    if tag:
        tag.decompose()

# 刪除目錄中指向 Medium 區塊的連結
for a in soup.find_all("a", href=True):
    if a["href"] in [
        "#alerts--risk-2-confidence-3",
        "#alerts--risk-2-confidence-2",
    ]:
        li = a.find_parent("li")
        if li:
            li.decompose()

# 將 localhost:8000 改成 apsvp.atri.org.tw
html = str(soup)
html = html.replace("localhost:8000", "apsvp.atri.org.tw")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)