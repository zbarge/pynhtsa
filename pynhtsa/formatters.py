

def json_parse_variable_value_response(r):
    d = r.json()
    results = d['Results']
    return {section['Variable']: section['Value']
            for section in results}

