import pdfplumber, re

class GraftEngine:
    def __init__(self, path):
        self.text = self._ingest(path)

    def _ingest(self, path):
        if path.endswith('.pdf'):
            with pdfplumber.open(path) as pdf: return "\n".join([p.extract_text() or "" for p in pdf.pages])
        with open(path, 'r', encoding='utf-8') as f: return f.read()

    def reconcile(self, bones):
        for b in bones:
            name_esc = re.escape(b['nm'])
            m = re.search(rf"(.{0,100}{name_esc}.{0,100})", self.text, re.I | re.S)
            b["rat"] = m.group(0).strip() if m else "NO_INTENT"
            b["stl"] = False
        return bones