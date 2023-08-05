"""Core HTTP client."""
import logging
from collections import OrderedDict
from typing import Iterable, Mapping, Optional
from urllib.parse import urljoin

from cachecontrol import CacheControl
from geopy import Point
from requests import RequestException, Response, Session
from requests.auth import AuthBase
from requests.utils import default_user_agent

from . import (
    __version__, fleets, legs, locations, orders, organisations, routes,
    trailers, trials, trips, vehicle_classes, vehicles,
)

__all__ = ['SRFData']


class ApiKeyAuth(AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.api_key
        return r


class SRFData:
    """
    SRF Data client. Provides basic access to the REST API.

    Access to objects is via typed attributes.
    Most users should only need the ``find_*`` methods.

    :param fleets: Access to fleets API.
    :param legs: Access to legs API.
    :param locations: Access to locations API.
    :param orders: Access to orders API.
    :param organisations: Access to organisations API.
    :param routes: Access to routes API.
    :param trailers: Access to trailers API.
    :param trials: Access to trials API.
    :param trips: Access to trips API.
    :param vehicle_classes: Access to vehicles classes API.
    :param vehicles: Access to vehicles API.
    """

    from .model import DataType
    _log = logging.getLogger('srf_client.SRFData')

    def __init__(self, root='https://data.csrf.ac.uk/api/', cache=None,
                 **kwargs):
        """
        Initialise a new instance.

        :param api_key: Personal authentication token for the API
        :param root: (optional) API root URL
        :param cache: (optional) provide an alternate cache implementation,
            or ``False`` to disable the cache
        """
        self._root = root
        if self._root[-1] != '/':
            self._root += '/'

        self._make_session(**kwargs)
        if cache is not False:
            self._session = CacheControl(self._session, cache=cache)
        self._session.verify = True
        self._session.headers.update({
            'Accept': 'application/json, */*;q=0.8',
            'User-Agent': '{}/{} {}'.format('srf-client', __version__,
                                            default_user_agent())
        })

        self.fleets = fleets.FleetsClient(self)
        self.legs = legs.LegsClient(self)
        self.locations = locations.LocationsClient(self)
        self.orders = orders.OrdersClient(self)
        self.organisations = organisations.OrganisationsClient(self)
        self.routes = routes.RoutesClient(self)
        self.trailers = trailers.TrailersClient(self)
        self.trials = trials.TrialsClient(self)
        self.trips = trips.TripsClient(self)
        self.vehicle_classes = vehicle_classes.VehicleClassesClient(self)
        self.vehicles = vehicles.VehiclesClient(self)

    def _make_session(self, **kwargs):
        self._session = Session()
        self._session.auth = ApiKeyAuth(kwargs['api_key'])

    def _prepare_request(self, url, kwargs):
        if url[0] == '/':  # avoid urljoin confusion with leading slash
            url = url[1:]
        url = urljoin(self._root, url)
        if not url.startswith(self._root):
            raise ValueError('Resolved url not part of the configured API')
        if 'timeout' not in kwargs:
            kwargs['timeout'] = (10, 60)
        return url, kwargs

    def get(self, url, **kwargs) -> Response:
        """
        Perform a raw GET request.

        :param url: Request URL. Will be resolved relative to the API root.
        :param kwargs: Additional options for request
        """
        url, kwargs = self._prepare_request(url, kwargs)
        return self._session.get(url=url, **kwargs)

    def ping(self, timeout=2) -> bool:
        """
        Check whether the service is reachable.

        May fail due to server-side errors, invalid authentication,
        or incorrect configuration.

        :param timeout: Time in seconds to wait for a response.
        """
        try:
            response = self.get('/', timeout=timeout)
        except RequestException:
            self._log.warning('Exception during ping()', exc_info=True)
            return False
        return response.headers['Server'].startswith('data-platform/') \
            and response.status_code in (200, 404)

    def get_types(self, raw: bool = False) -> Mapping[str, 'DataType']:
        """
        Get the ``type`` definitions for the ``get_data`` measurements.

        :param raw: Return the types for ``get_raw_data`` instead..
        """
        from .model import DataType, FieldDef
        response = self.get('/types', params={'raw': raw})

        def parse(data_type):
            return DataType(
                type=data_type['type'],
                description=data_type['description'],
                fields=None if raw else tuple(
                    FieldDef(**f) for f in data_type['fields']
                )
            )
        return OrderedDict((t['type'], parse(t)) for t in response.json())

    def get_elevation(self, points: Iterable[Point]
                      ) -> Iterable[Optional[float]]:
        """
        Lookup elevation for given points.

        :param points: (latitude, longitude) points to query
        :return: iterable of corresponding elevation in metres
        """
        url, kwargs = self._prepare_request('/elevation', {})
        response = self._session.post(
            url,
            headers={'Content-Type': 'text/csv'},
            data=(f'{p[0]},{p[1]}\r\n'.encode('us-ascii') for p in points),
            stream=True,
            **kwargs)
        response.raise_for_status()
        return (None if s == b'null' else float(s)
                for s in response.iter_lines())
