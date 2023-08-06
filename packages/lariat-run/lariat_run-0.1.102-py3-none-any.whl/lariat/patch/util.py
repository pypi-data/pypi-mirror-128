import json
import pandas


def _type_specific_json_convert(obj):
    if isinstance(obj, pandas.core.frame.DataFrame):
        return obj.to_json()

    # not json-able if we get here
    raise Exception

def try_make_json(obj):
    try:
        result = json.dumps(obj)
        return result
    except:
        try:
            result = _type_specific_json_convert(obj)
            return result
        except:
            return f"Non JSON-able object of type {type(obj.__name__)}"
