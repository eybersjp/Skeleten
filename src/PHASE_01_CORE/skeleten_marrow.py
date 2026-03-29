from tree_sitter_languages import get_parser, get_language

class MarrowParser:
    def __init__(self, lang_id):
        self.lang_id = lang_id
        self.parser = get_parser(lang_id)
        self.language = get_language(lang_id)

    def extract_bones(self, code):
        if self.lang_id == "python":
            query_str = """
            (function_definition) @f
            (class_definition) @f
            """
        else:
            query_str = """
            (function_declaration) @f
            (method_definition) @f
            (class_declaration) @f
            (interface_declaration) @f
            """
        query = self.language.query(query_str)
        captures = query.captures(self.parser.parse(code).root_node)
        
        bones = []
        for n, t in captures:
            if t == "f":
                nm_node = n.child_by_field_name("name")
                in_node = n.child_by_field_name("parameters") or n.child_by_field_name("formal_parameters")
                bones.append({
                    "nm": nm_node.text.decode() if nm_node else "UNKNOWN",
                    "in": in_node.text.decode() if in_node else "NONE",
                    "typ": n.type
                })
        return bones

def run_marrow_probe(path):
    ext_map = {".py": "python", ".ts": "typescript", ".js": "javascript"}
    lang = ext_map.get(path.suffix.lower())
    if not lang: return []
    with open(path, "rb") as f: return MarrowParser(lang).extract_bones(f.read())