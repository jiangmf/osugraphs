import json
import pprint as python_pprint
from django.db import models

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

def pprint(data):
    pp = python_pprint.PrettyPrinter(indent=4)
    pp.pprint(data)


def delete_duplicates(model, unique_fields):
    duplicates = (model.objects.values(*unique_fields)
         .order_by()
         .annotate(max_id=models.Max('id'),
                   count_id=models.Count('id'))
         .filter(count_id__gt=1))

    for duplicate in duplicates:
        (model.objects.filter(**{x: duplicate[x] for x in unique_fields})
            .exclude(id=duplicate['max_id'])
            .delete())

def list_duplicates(model, unique_fields):
    duplicates = (model.objects.values(*unique_fields)
         .order_by()
         .annotate(max_id=models.Max('id'),
                   count_id=models.Count('id'))
         .filter(count_id__gt=1))

    for duplicate in duplicates:
        for obj in model.objects.filter(**{x: duplicate[x] for x in unique_fields}).exclude(id=duplicate['max_id']):
            pprint(obj.__dict__)