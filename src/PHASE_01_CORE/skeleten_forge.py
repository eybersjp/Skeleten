import json, os

class MncForge:
    def __init__(self, out_dir):
        self.out_dir = out_dir

    def forge(self, name, bones, uri):
        os.makedirs(self.out_dir, exist_ok=True)
        payload = {"@context": "https://schema.org", "@type": "SoftwareSourceCode", "nm": name, "rep": uri, 
                   "pts": [{"nm": b["nm"], "typ": b["typ"], "in": b["in"], "rat": b["rat"], "stl": b.get("stl", False)} for b in bones]}
        with open(os.path.join(self.out_dir, "skeleten_mnc.json"), 'w', encoding='utf-8') as f:
            json.dump(payload, f, separators=(',', ':'))