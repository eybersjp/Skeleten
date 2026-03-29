import json
class AutoDoc:
    def __init__(self, mnc_path):
        with open(mnc_path, 'r') as f: self.data = json.load(f)

    def to_markdown(self):
        md = f"# {self.data['nm']} API REFERENCE\n\n"
        for p in self.data['pts']:
            md += f"## {p['nm']}\n- **Type:** {p['typ']}\n- **Params:** {p['in']}\n- **Rationale:** {p['rat']}\n\n"
        return md