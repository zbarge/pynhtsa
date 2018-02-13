

def json_parse_variable_value_response(r):
    d = r.json()
    results = d['Results']
    return {section['Variable']: section['Value']
            for section in results}


def read_data_frame(file_path, method='read_csv', **kwargs):
    import pandas as pd
    read = getattr(pd, method, pd.read_csv)
    return read(file_path, **kwargs)
