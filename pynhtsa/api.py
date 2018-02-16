import requests


NHTSA_BASE_URL = 'https://vpic.nhtsa.dot.gov/api/'


class NhtsaApi:
    """
    https://vpic.nhtsa.dot.gov/api/
    """
    def __init__(self, _format='json', base_url=NHTSA_BASE_URL):
        self.format = _format
        self.base_url = base_url

    def get(self, service_name, params=None, **kwargs):
        """
        Calls method:requests.get after constructing the full API request URL
        and injecting 'format' into params.

        :param service_name: (str)
            The service name to be added to NHTSA_BASE_URL
            e.g. 'vehicles/DecodeVin/ABKXJ23235JAWF5212'

        :param params: (dict, default None)
            An optional dictionary of supported parameters for the get request.
            'format' parameter is overwritten with NhtsaApi.format.

        :param kwargs:
            Optional parameters passed along to requests.get
        :return:
        """
        if params is None:
            params = dict()

        url = self.base_url + service_name
        params['format'] = self.format
        return requests.get(url, params=params, **kwargs)

    def post(self, service_name, **kwargs):
        """
        Calls method:requests.post after constructing the full API request URL
        and injecting 'format' into the data.

        :param service_name: (str)
            The service name to be added to NHTSA_BASE_URL
        :param kwargs:
        :return:
        """
        url = self.base_url + service_name
        data = kwargs.get('data', dict())
        data['format'] = self.format
        kwargs['data'] = data
        return requests.post(url, **kwargs)

    def decode_vin(self, vin, model_year=None):
        """
        The Decode VIN API will decode the VIN and the decoded output
        will be made available in the format of Key-value pairs.

        The IDs (VariableID and ValueID) represent the unique ID associated with the Variable/Value.
        In case of text variables, the ValueID is not applicable.

        Model Year in the request allows for the decoding to specifically be done in the current,
        or older (pre-1980), model year ranges.

        It is recommended to always send in the model year.

        This API also supports partial VIN decoding (VINs that are less than 17 characters).
            In this case, the VIN will be decoded partially with the available characters.
            In case of partial VINs, a "*" could be used to indicate the unavailable characters.
            The 9th digit is not necessary.

        :param vin:
        :param model_year:
        :return:
        """
        if model_year is not None:
            p = {'modelyear': model_year}
        else:
            p = None
        return self.get('vehicles/DecodeVin/{}'.format(vin), params=p)

    def decode_vin_batch(self, list_of_lists_with_vin_and_year):
        """
        Decodes multiple VIN, year combinations in one request.

        :param list_of_lists_with_vin_and_year: (list)
            This should be a list containing lists containing (VIN, Model Year).
            These will be concatenated into a string and posted to the API.
        :return: (requests.Response)
            Example Data:
            {
            'SearchCriteria':'',
            'Results': [{}, {}, {}, {}]
            }
        """
        vals = [('{},{}'.format(v, y) if y else v)
                for v, y in list_of_lists_with_vin_and_year]
        return self.post('vehicles/DecodeVINValuesBatch', data={'data': ';'.join(vals)})

    def decode_vin_extended(self, vin, model_year=None):
        """
        This is exactly like the NhtsaApi.decode_vin method but provides additional information on
        variables related to other NHTSA programs like NCSA, Artemis etc.

        :param vin:
        :param model_year:
        :return:
        """
        if model_year is not None:
            p = {'modelyear': model_year}
        else:
            p = None
        return self.get('vehicles/DecodeVinExtended/{}'.format(vin), params=p)

    def decode_wmi(self, wmi):
        """
        This provides information on the World Manufacturer Identifier for a specific WMI code.

        :param wmi:
            WMIs may be put in as either 3 characters representing VIN position 1-3 or 6 characters representing
            VIN positions 1-3 & 12-14. Example "JTD", "1T9131".

        :return:
        """
        return self.get('vehicles/DecodeWMI/{}'.format(wmi))

    def decode_sae_wmi(self, wmi):
        return self.get('vehicles/DecodeSAEWMI/{}'.format(wmi))

    def get_wmis_for_oem(self, oem):
        """
        Provides information on the all World Manufacturer Identifier (WMI) for a specified Manufacturer.
        Only WMI registered in vPICList are displayed.
        For a list of all WMIs for a specified Manufacturer see GetSAEWMIsForManufacturer
        :param oem:
        :return:
        """
        return self.get('vehicles/GetWMIsForManufacturer/{}'.format(oem))

    def get_sae_wmis_for_oem(self, oem):
        return self.get('vehicles/GetSAEWMIsForManufacturer/{}'.format(oem))

    def get_all_makes(self):
        """
        This provides a list of all the Makes available in vPIC Dataset.
        :return:
        """
        return self.get('vehicles/GetAllMakes')

    def get_parts(self, _type, from_date, to_date, page=1):
        """
        This provides a list of ORGs with letter date in the given range
        of the dates and with specified Type of ORG.
        Up to 1000 results will be returned at a time.

        :param _type:
        :param from_date:
        :param to_date:
        :param page:
        :return:
        """
        p = dict(type=_type, fromDate=from_date, toDate=to_date, page=page)
        return self.get('vehicles/GetParts', params=p)

    def get_all_oems(self, page=1):
        """
        This provides a list of all the Manufacturers available in vPIC Dataset.
        Results are provided in pages of 100 items, use parameter "page"
        to specify 1-st (default, 2nd, 3rd, ...Nth ... page.)
        :param page:
        :return:
        """
        p = dict(page=page)
        return self.get('vehicles/GetAllManufacturers', params=p)

    def get_oem_details(self, oem):
        """
        This provides the details for a specific manufacturer that is requested.
        This gives the results of all the manufacturers whose name is LIKE the manufacturer name.
        It accepts a partial manufacturer name as an input. Multiple results are returned in case of multiple matches.

        :param oem:
        :return:
        """
        return self.get('vehicles/GetManufacturerDetails/{}'.format(oem))

    def get_makes_by_oem(self, oem, year=None):
        """
        This returns all the Makes in the vPIC dataset for a specified manufacturer whose
        name is LIKE the manufacturer name in vPIC Dataset.
        Manufacturer name can be a partial name, or a full name for more specificity
        (e.g., "HONDA", "HONDA OF CANADA MFG., INC.", etc.)

        :param oem:
        :param year:
        :return:
        """
        if year is None:
            return self.get('vehicles/GetMakesForManufacturer/{}'.format(oem))
        return self.get(
            'vehicles/GetMakesForManufacturerAndYear/{}'.format(oem), params=dict(year=year))

    def get_makes_by_vehicle_type(self, veh_type='car'):
        """
        This returns all the Makes in the vPIC dataset for a specified vehicle type whose name is
        LIKE the vehicle type name in vPIC Dataset.

        Vehicle Type name can be a partial name, or a full name for more
        specificity (e.g., "Vehicle", "Moto", "Low Speed Vehicle", etc.)

        :param veh_type:
        :return:
        """
        return self.get('vehicles/GetMakesForVehicleType/{}'.format(veh_type))

    def get_vehicle_types_for_make_by_name(self, make):
        """
        This returns all the Vehicle Types in the vPIC dataset for a specified
        Make whose name is LIKE the make name in vPIC Dataset.

        Make name can be a partial name, or a full name for more specificity (e.g., "Merc", "Mercedes Benz", etc.)
        :param make:
        :return:
        """
        return self.get('vehicles/GetVehicleTypesForMake/{}'.format(make))

    def get_vehicle_types_for_make_by_id(self, make_id):
        return self.get('vehicles/GetVehicleTypesForMakeId/{}'.format(make_id))

    def get_equipment_plant_codes(self, year=2016, equip_type=None, report_type='all'):
        """
        Returns assigned Equipment Plant Codes. Can be filtered by Year, Equipment Type and Report Type.

        Year
            2016: Only years 2016 and above are supported

        Equipment Type
            1: Tires
            3: Brake Hoses
            13: Glazing
            16: Retread

        Report Type
            New The Equipment Plant Code was assigned during the selected year
            Updated The Equipment Plant data was modified during the selected year
            Closed The Equipment Plant is no longer Active
            All All Equipment Plant Codes regardless of year, including their status (active or closed)
        :return: (requests.Response)
            Example object in Results list:
            {
            "Address":"2950 INTERNATIONAL BLVD.",
            "City":"CLARKSVILLE",
            "Country":"USA",
            "DOTCode":"00T",
            "Name":"HANKOOK TIRE MANUFACTURING TENNESSEE, LP",
            "OldDotCode":"",
            "PostalCode":"37040",
            "StateProvince":"TENNESSEE",
            "Status":"Active"
            }
        """

        p = dict()
        if year:
            p['year'] = year
        if equip_type:
            p['equipmentType'] = equip_type
        if report_type:
            p['reportType'] = report_type

        return self.get('vehicles/GetEquipmentPlantCodes', params=p)

    def get_models_for_make(self, make):
        """
        This returns the Models in the vPIC dataset for a specified Make whose name is LIKE the Make in vPIC Dataset.
        Make can be a partial, or a full for more specificity (e.g., "Harley", "Harley Davidson", etc.)
        :param make:
        :return:
        """
        return self.get('vehicles/GetModelsForMake/{}'.format(make))

    def get_models_for_make_id(self, make_id):
        """
        This returns the Models in the vPIC dataset for a specified Make
        whose Id is EQUAL the MakeId in vPIC Dataset.
        :param make_id:
        :return:
        """
        return self.get('vehicles/GetModelsForMakeId/{}'.format(make_id))

    def get_models_for_make_id_year_type(self, make_id, year=None, veh_type=None):
        """
        This returns the Models in the vPIC dataset for a specified year and Make
        whose Id is EQUAL the MakeId in vPIC Dataset.

        :param make_id: (int)
        :param year: (int)
            Must be greater than 1995
        :param veh_type: (str)
            car, truck, vehicle, moto
        :return: (requests.Response)
            Example record found in Results:
            {
                "Make_ID":474,
                "Make_Name":"Honda",
                "Model_ID":1861,
                "Model_Name":"Accord"
            }
        """
        base = 'vehicles/GetModelsForMakeIdYear/makeId/{}'.format(make_id)
        if year:
            base += '/modelyear/{}'.format(year)
        if veh_type:
            base += '/vehicletype/{}'.format(veh_type)

        return self.get(base)

    def get_vehicle_variables_list(self):
        """
        This provides a list of all the Vehicle related variables that are in vPIC dataset.
        Information on the name, description and the type of the variable is provided.

        :return: (requests.Response)
            {"DataType":"string",
            "Description":"<p>Any other battery information that
                           does not belong to any of the fields above<\/p>",
            "ID":1,
            "Name":"Battery Info"}
        """
        return self.get('vehicles/GetVehicleVariableList')

    def get_vehicle_variable_values_list(self, var='battery'):
        """
        This provides a list of all the accepted values for a given variable that are stored in vPIC dataset.
        This applies to only "Look up" type of variables.
        :param var (str)
            The variable to get allowed lookup values on.
        :return: (requests.Response)
            {"ElementName":"Battery Type",
            "Id":4,
            "Name":"Cobald Dioxide\/Cobalt"}
        """
        return self.get('vehicles/GetVehicleVariableValuesList/{}'.format(var))


