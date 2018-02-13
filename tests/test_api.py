import pytest, os, logging
from pynhtsa import NhtsaApi
from pynhtsa.formatters import json_parse_variable_value_response, read_data_frame

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
SAMPLE_VIN_PATH = os.path.join(FIXTURES_DIR, 'sample_vin_list.csv')

VIN_DATA = [
    ('2C4RDGCG4DR524227', 2013),
    ('3VW637AJ4DM283861', 2013),
    ('3VW637AJ4DM283861', 2013),
    ('1C4AJWAG2DL692427', 2013),
    ('2T1BU4EE1DC922216', 2013),
]

logging.basicConfig(level=logging.DEBUG)
api = NhtsaApi(_format='json')


def test_decode_vin():
    res = api.decode_vin('3FADP4GX3FM207940', 2015)
    data = json_parse_variable_value_response(res)
    assert int(data['Model Year']) == 2015
    assert data['Make'] == 'FORD'
    assert data['Model'] == 'Fiesta'
    assert data['Trim'] == 'ST'


def test_decode_vin_batch():
    res = api.decode_vin_batch(VIN_DATA)
    data = res.json()
    assert data['Count'] == len(VIN_DATA)


def test_decode_vin_big_batch():
    df = read_data_frame(SAMPLE_VIN_PATH)
    count = 50
    vin_data = zip(df['vin'].fillna(0).tolist()[:count],
                   df['year'].fillna(0).tolist()[:count])
    resp = api.decode_vin_batch(vin_data)
    data = resp.json()
    assert data['Count'] == count


def test_decode_vin_extended():
    resp = api.decode_vin('3FADP4GX3FM207940', 2015)
    data = json_parse_variable_value_response(resp)
    assert int(data['Model Year']) == 2015
    assert data['Make'] == 'FORD'
    assert data['Model'] == 'Fiesta'
    assert data['Trim'] == 'ST'


def test_decode_wmi():
    resp = api.decode_wmi('1G1')
    data = resp.json()
    result = data['Results'][0]
    assert result['Make'] == 'Chevrolet'
    assert result['ManufacturerName'] == 'GENERAL MOTORS LLC'


def test_get_all_makes():
    resp = api.get_all_makes()
    data = resp.json()['Results']
    make_names = [d['Make_Name'] for d in data]
    assert 'Aston Martin' in make_names
    assert 'MINI' in make_names
    assert 'Cadillac' in make_names


def test_get_parts():
    pass


def test_get_all_oems():
    pass


def test_get_oem_details():
    pass


def test_get_makes_by_oem():
    pass


def test_get_makes_by_vehicle_type():
    pass




if __name__ == '__main__':
    test_decode_vin()



