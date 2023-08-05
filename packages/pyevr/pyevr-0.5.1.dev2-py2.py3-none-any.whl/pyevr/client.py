# -*- coding: utf-8 -*-

"""Main module."""
from pyevr import apis
from pyevr.openapi_client.api_client import ApiClient
from pyevr.openapi_client.configuration import Configuration


HOLDING_BASE_CHILDREN = (
    'ForestNotice',
    'ForestNoticeAllOf',
    'InventoryAct',
    'InventoryActAllOf',
    'ConsolidatedAct',
    'ConsolidatedActAllOf',
    'SalesContract',
    'SalesContractAllOf',
    'ForestAct',
    'ContractForTransferOfCuttingRights',
)


class ExtendedApiClient(ApiClient):
    """Extended API client generated by openapi-generator-cli."""

    def sanitize_for_serialization(self, obj):
        """Builds a JSON POST object.

        If obj is one of the subclasses of `pyevr.openapi_client.models.holding_base.HoldingBase` adds the corresponding
        type to dictionary. Otherwise returns the dictionary from `pyevr.openapi_client.api_client.ApiClient`

        :param obj: The data to serialize.
        :return: The serialized form of data.
        """
        obj_dict = super().sanitize_for_serialization(obj)

        # Add holding base type to dictionary
        class_name = obj.__class__.__name__
        if class_name in HOLDING_BASE_CHILDREN:
            if class_name.endswith('AllOf'):
                class_name = class_name[:-5]
            obj_dict['type'] = class_name

        return obj_dict


class EVRClient(object):
    """API client class for EVR.

    :param api_key: Company API key in EVR
    :param host: EVR host. Defaults to test host (optional)
    """

    def __init__(self, api_key: str, host: str = None):
        configuration = Configuration(api_key={'EVR-APIKEY': api_key})
        if host is not None:
            configuration.host = host
        self.openapi_client = ExtendedApiClient(configuration)

        self.assortments = apis.AssortmentsAPI(self.openapi_client)
        self.certificates = apis.CertificatesAPI(self.openapi_client)
        self.measurements = apis.MeasurementsAPI(self.openapi_client)
        self.measurement_units = apis.MeasurementUnitsAPI(self.openapi_client)
        self.organizations = apis.OrganizationsAPI(self.openapi_client)
        self.place_of_deliveries = apis.PlaceOfDeliveriesAPI(self.openapi_client)
        self.waybills = apis.WaybillsAPI(self.openapi_client)
