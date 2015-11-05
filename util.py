import json

class StringifyEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except:
            pass
        # Ensure that html is encoded well
        return html.escape(str(obj))

def pretty_json(data):
    try:
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), cls=StringifyEncoder)
    except Exception:
        pass
    
    return '--- Could not serialize to JSON ---'

def print_json(data):
    print(pretty_json(data))