import pytest
from pynhtsa import NhtsaApi
from pynhtsa.formatters import json_parse_variable_value_response
import logging

logging.basicConfig(level=logging.DEBUG)
api = NhtsaApi(_format='json')


def test_decode_vin():
    res = api.decode_vin('3FADP4GX3FM207940', 2015)
    data = json_parse_variable_value_response(res)
    assert data['Model Year'] == 2015
    assert data['Make'] == 'FORD'
    assert data['Model'] == 'Fusion'
    assert data['Trim'] == 'ST'


def test_decode_vin_batch():
    pass


def test_decode_vin_extended():
    pass


def test_decode_wmi():
    pass


def test_decode_sae_wmi():
    pass


def test_decode_sae_wmis_for_oem():
    pass


def test_get_all_makes():
    pass


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



