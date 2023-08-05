"""Data model for the API."""
from collections import namedtuple

import attr  # may replace with @dataclass in py37
from datetime import datetime
from geopy import Point
from geopy.distance import Distance
from immutabledict import immutabledict
from itertools import chain
from typing import Iterable, Mapping, Optional, Sequence

from srf_client.paging import paged_items
from . import client, filter as f, paging

__all__ = [
    'Calibration', 'DataType', 'ExternalVehicleClass', 'FieldDef', 'Fleet',
    'FleetEntry', 'Leg', 'Location', 'Measurement', 'Order', 'Organisation',
    'Route', 'Trailer', 'Trial', 'Trip', 'Vehicle', 'VehicleClass'
]


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class Organisation:
    """
    An affiliated or former organisation.

    :param uri: URI for this organisation
    :param name: Name of the organisation
    """

    _client: 'client.SRFData'
    uri: str
    name: str

    def get_fleets(self, lazy=False) -> 'paging.Page[Fleet]':
        """
        Fetch fleets for organisation.

        :param lazy: Defer fetching of the Fleet objects
        """
        return self._client.fleets.find_all(lazy=lazy, **{
            'organisation.name': f.eq(self.name)
        })

    def get_routes(self, lazy=False) -> 'paging.Page[Route]':
        """
        Fetch routes for organisation.

        :param lazy: Defer fetching of the Route objects
        """
        return self._client.routes.find_all(lazy=lazy, **{
            'organisation.name': f.eq(self.name)
        })

    def get_trailers(self, lazy=False) -> 'paging.Page[Trailer]':
        """
        Fetch trailers for organisation.

        :param lazy: Defer fetching of the Trailer objects
        """
        return self._client.trailers.find_all(lazy=lazy, **{
            'organisation.name': f.eq(self.name)
        })

    def get_trials(self, lazy=False) -> 'paging.Page[Trial]':
        """
        Fetch trials for organisation.

        :param lazy: Defer fetching of the Trial objects
        """
        return self._client.trials.find_all(lazy=lazy, **{
            'organisation.name': f.eq(self.name)
        })

    def get_vehicle_classes(self, lazy=False) -> 'paging.Page[VehicleClass]':
        """
        Fetch vehicle classes for organisation.

        :param lazy: Defer fetching of the VehicleClass objects
        """
        return self._client.vehicle_classes.find_all(lazy=lazy, **{
            'organisation.name': f.eq(self.name)
        })

    def get_vehicles(self, lazy=False) -> 'paging.Page[Vehicle]':
        """
        Fetch vehicles for organisation.

        :param lazy: Defer fetching of the Vehicle objects
        """
        return self._client.vehicles.find_all(lazy=lazy, **{
            'organisation.name': f.eq(self.name)
        })


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class Trial:
    """
    A specific project investigation.

    :param uri: URI for this trial
    :param description: Description of the trial
    :param active: Whether data collection is ongoing
    """

    _client: 'client.SRFData'
    _org_uri: str
    uri: str
    description: str
    active: bool

    @property
    def organisation(self) -> 'Organisation':  # noqa: D102
        return self._client.organisations.get(uri=self._org_uri)

    def get_trips(self, lazy=False, **kwargs) -> 'paging.Page[Trip]':
        """
        Fetch trips for trial.

        :param lazy: Defer fetching of the Trip objects
        :param kwargs: Additional field filters
        """
        return self._client.trips.find_by_trial(self, lazy=lazy, **kwargs)


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class Vehicle:
    """
    A motor vehicle.

    :param uri: URI for this vehicle
    :param registration: Vehicle registration (number plate)
    :param vin: Vehicle identification number (ISO 3779)
    :param calibrated: Whether the app was calibrated on installation.
        If missing then data types 11 and 12 are in an arbitrary basis.
    :param make: Vehicle manufacturer
    :param model: Manufacturer’s model designation
    :param type: Vehicle classification (e.g. ``RIGID``, ``ARTIC``, ``VAN``,
        ``BUS``, ``CAR``)
    :param fuel: Fuel type (e.g. ``DIESEL``, ``PETROL``, ``CNG``, ``LNG``,
        ``H2``, ``ELECTRIC``)
    :param weight_class: Max weight class (tonnes)
    :param euro_standard: European emission standard
    :param description: Additional description/notes
    """

    _client: 'client.SRFData'
    _org_uri: str
    uri: str
    registration: Optional[str] = None
    vin: Optional[str] = None
    calibrated: bool = False
    make: Optional[str] = None
    model: Optional[str] = None
    type: Optional[str] = None
    fuel: Optional[str] = None
    weight_class: Optional[float] = None
    euro_standard: Optional[int] = None
    description: Optional[str] = None

    @property
    def organisation(self) -> 'Organisation':  # noqa: D102
        return self._client.organisations.get(uri=self._org_uri)

    def get_trips(self, lazy=False, **kwargs) -> 'paging.Page[Trip]':
        """
        Fetch trips for vehicle.

        :param lazy: Defer fetching of the Trip objects
        :param kwargs: Additional field filters
        """
        return self._client.trips.find_by_vehicle(self, lazy=lazy, **kwargs)


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class Trailer:
    """
    A towed vehicle or container.

    :param uri: URI for this trailer
    :param serial: Trailer serial number
    :param length: Length of trailer chassis (m)
    :param make: Trailer manufacturer
    :param model: Manufacturer’s model designation
    :param type: Trailer classification (e.g. ``SINGLE``, ``HIGH``, ``DOUBLE``,
        ``TEARDROP``, ``LONG``, ``SLOPED``, ``TANK``)
    :param axles: Number of axles
    :param tires_per_axle: Number of tires per axle
    :param description: Additional description/notes
    """

    _client: 'client.SRFData'
    _org_uri: str
    uri: str
    serial: str
    length: Optional[float] = None
    make: Optional[str] = None
    model: Optional[str] = None
    type: Optional[str] = None
    axles: Optional[int] = None
    tires_per_axle: Optional[int] = None
    description: Optional[str] = None

    @property
    def organisation(self) -> 'Organisation':  # noqa: D102
        return self._client.organisations.get(uri=self._org_uri)

    def get_trips(self, lazy=False, **kwargs) -> 'paging.Page[Trip]':
        """
        Fetch trips for trailer.

        :param lazy: Defer fetching of the Trip objects
        :param kwargs: Additional field filters
        """
        return self._client.trips.find_by_trailer(self, lazy=lazy, **kwargs)


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class Trip:
    """
    A single journey.

    Can be defined manually, or as all the legs that begin on a particular day.

    :param uri: URI for this trip
    :param types: Set of available data types
    :param start_time: First recorded timestamp
    :param end_time: Last recorded timestamp
    :param consumption: Fuel usage over the trip (litres)
    :param distance: Distanced travelled over the trip
    """

    _client: 'client.SRFData'
    _trailer_uri: str
    _trial_uri: str
    _vehicle_uri: str
    uri: str
    source: str
    types: frozenset = frozenset()
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    consumption: Optional[float] = None
    distance: Optional[Distance] = None

    @property
    def trailer(self) -> 'Trailer':  # noqa: D102
        return self._client.trailers.get(uri=self._trailer_uri)

    @property
    def trial(self) -> 'Trial':  # noqa: D102
        return self._client.trials.get(uri=self._trial_uri)

    @property
    def vehicle(self) -> 'Vehicle':  # noqa: D102
        return self._client.vehicles.get(uri=self._vehicle_uri)

    def get_legs(self, lazy=False, **kwargs) -> 'paging.Page[Leg]':
        """
        Fetch legs for trip.

        :param lazy: Defer fetching of the Leg objects
        :param kwargs: Additional field filters
        """
        return self._client.legs.find_by_trip(self, lazy=lazy, **kwargs)

    def get_data(self, include=None) -> Iterable['Measurement']:
        """
        Return available measurements.

        :param include: Data types to include. By default all are included.
        """
        return chain.from_iterable(leg.get_data(include=include)
                                   for leg in paged_items(self.get_legs()))


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class Leg:
    """
    A largely arbitrary section of a vehicle’s journey.

    Remaining stopped for an amount of time triggers the end of a leg.

    :param uri: URI for this leg
    :param trip: Parent trip
    :param start_time: First recorded timestamp
    :param end_time: Last recorded timestamp
    :param types: Set of available data types
    :param start_location: Location at start of leg
    :param end_location: Location at end of leg
    :param start_distance: Odometer reading at start of leg
    :param end_distance: Odometer reading at end of leg
    :param consumption: Fuel usage over the leg (litres)
    :param fuel_level: Fuel level at end of leg (percent)
    :param calibration: Calibration data
    :param weight: Gross vehicle weight during the leg (kilograms)
    :param weight_source: Source of the weight value
    """

    _client: 'client.SRFData'
    _trip_uri: str
    uri: str
    start_time: datetime
    end_time: datetime
    types: frozenset = frozenset()
    start_location: Optional[Point] = None
    end_location: Optional[Point] = None
    start_distance: Optional[Distance] = None
    end_distance: Optional[Distance] = None
    consumption: Optional[float] = None
    fuel_level: Optional[float] = None
    weight: Optional[int] = None
    weight_source: Optional[str] = None

    @property
    def trip(self) -> 'Trip':  # noqa: D102
        return self._client.trips.get(uri=self._trip_uri)

    @property
    def calibration(self) -> 'Calibration':  # noqa: D102
        return self._client.legs.get_calibration(self)

    def get_data(self, include=None) -> Iterable['Measurement']:
        """
        Return available measurements.

        :param include: Data types to include. By default all are included.
        """
        return self._client.legs.get_data(self, include=include)

    def get_raw_data(self, include=None) -> Iterable['Measurement']:
        """
        Return the raw measurements.

        :param include: Data types to include. By default all are included.
        """
        return self._client.legs.get_raw_data(self, include=include)


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class Calibration:
    """
    Leg calibration data for vehicle dynamics.

    :param forward: Unit vector pointing in the direction of forward travel
    :param left: Lateral unit vector (forward × up)
    :param up: Unit vector pointing against the action of gravity
    :param inv_gravity: Inverse gravitational acceleration in device's basis
    """

    forward: tuple
    left: tuple
    up: tuple
    inv_gravity: tuple


Measurement = namedtuple('Measurement', ['timestamp', 'type', 'data'])
DataType = namedtuple('DataType', ['type', 'description', 'fields'])
FieldDef = namedtuple('FieldDef', ['name', 'unit'])


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class Fleet:
    """
    Set of vehicles available for operations.

    :param uri: URI for this fleet
    :param organisation: Owning organisation
    :param name: Name of this fleet
    :param entries: Fleet composition
    """

    _client: 'client.SRFData'
    _org_uri: str
    uri: str
    name: str
    entries: Sequence['FleetEntry']

    @property
    def organisation(self) -> Organisation:  # noqa: D102
        return self._client.organisations.get(uri=self._org_uri)


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class FleetEntry:
    """
    Component of a fleet.

    :param location: Vehicle home location
    :param vehicle_class: Vehicle description
    :param count: Number of vehicles of this type at this location
    """

    _client: 'client.SRFData'
    _location_uri: str
    _vehicle_class_uri: str
    count: int

    @property
    def location(self) -> 'Location':  # noqa: D102
        return self._client.locations.get(uri=self._location_uri)

    @property
    def vehicle_class(self) -> 'VehicleClass':  # noqa: D102
        return self._client.vehicle_classes.get(uri=self._vehicle_class_uri)


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class Location:
    """
    Significant location.

    :param uri: URI for this location
    :param organisation: Owning organisation
    :param name: Name for this location
    :param post_code: Location's postal code
    :param point: Coordinates of the location
    """

    _client: 'client.SRFData'
    _org_uri: str
    uri: str
    name: Optional[str]
    post_code: Optional[str]
    point: Optional[Point]

    @property
    def organisation(self) -> 'Organisation':  # noqa: D102
        return self._client.organisations.get(uri=self._org_uri)

    def get_routes(self, lazy=False, **kwargs) -> 'paging.Page[Route]':
        """
        Fetch routes for location.

        :param lazy: Defer fetching of the Leg objects
        :param kwargs: Additional field filters
        """
        return self._client.routes.find_by_location(self, lazy, **kwargs)


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class Route:
    """
    A logistics operation route, planned or completed.

    :param uri: URI for this route
    :param organisation: Owning organisation
    :param start_location: Start of the route
    :param end_location: End of the route
    :param depot: Operational base location
    :param vehicle_class: Type of vehicle used
    :param plan: Whether this route describes a planned or an actual route
    :param start_time: Start time
    :param end_time: End time
    :param distance: Total distance travelled
    :param shift_start: Start of driver's shift
    :param shift_end: End of driver's shift
    :param registration: Specific vehicle that was used
    :param orders: Total number of orders involved
    :param total_units: Total number of units moved
    :param total_weight: Total weight of goods moved (kilograms)
    """

    _client: 'client.SRFData'
    _org_uri: str
    _start_location_uri: str
    _end_location_uri: str
    _depot_uri: str
    _vehicle_class_uri: str
    uri: str
    plan: bool
    start_time: datetime
    end_time: datetime
    distance: Optional[Distance] = None
    shift_start: Optional[datetime] = None
    shift_end: Optional[datetime] = None
    registration: Optional[str] = None
    orders: int = 0
    total_units: Optional[float] = None
    total_weight: Optional[float] = None

    @property
    def organisation(self) -> 'Organisation':  # noqa: D102
        return self._client.organisations.get(uri=self._org_uri)

    @property
    def start_location(self) -> 'Location':  # noqa: D102
        return self._client.locations.get(uri=self._start_location_uri)

    @property
    def end_location(self) -> 'Location':  # noqa: D102
        return self._client.locations.get(uri=self._end_location_uri)

    @property
    def depot(self) -> 'Location':  # noqa: D102
        return self._client.locations.get(uri=self._depot_uri)

    @property
    def vehicle_class(self) -> 'VehicleClass':  # noqa: D102
        return self._client.vehicle_classes.get(uri=self._vehicle_class_uri)

    def get_orders(self, lazy=False, **kwargs) -> 'paging.Page[Order]':
        """
        Fetch orders for route.

        :param lazy: Defer fetching of the Leg objects
        :param kwargs: Additional field filters
        """
        return self._client.orders.find_by_route(self, lazy=lazy, **kwargs)


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class Order:
    """
    Transported cargo.

    :param uri: URI for this order
    :param route: Route transporting this cargo
    :param pickup: Postal code of pickup location
    :param destination: Postal code of destination location
    :param time_window_start: Start of the delivery window
    :param time_window_end: End of the delivery window
    :param pickup_arrive: Arrival at pickup location
    :param pickup_depart: Departure from pickup location
    :param destination_arrive: Arrival at destination
    :param destination_depart: Departure from destination
    :param distance: Distance travelled for delivery
    :param ambient: Number of ambient units
    :param chilled: Number of chilled units
    :param frozen: Number of frozen units
    :param weight: Weight of order (kilograms)
    """

    _client: 'client.SRFData'
    _route_uri: str
    uri: str
    pickup: str
    destination: str
    time_window_start: Optional[datetime] = None
    time_window_end: Optional[datetime] = None
    pickup_arrive: Optional[datetime] = None
    pickup_depart: Optional[datetime] = None
    destination_arrive: Optional[datetime] = None
    destination_depart: Optional[datetime] = None
    distance: Optional[Distance] = None
    ambient: Optional[float] = None
    chilled: Optional[float] = None
    frozen: Optional[float] = None
    weight: Optional[float] = None

    @property
    def route(self) -> 'Route':  # noqa: D102
        return self._client.routes.get(uri=self._route_uri)


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class VehicleClass:
    """
    A specific make/model/configuration of road vehicle.

    :param uri: URI for this vehicle class
    :param organisation: Owning organisation
    :param description: Additional description/notes
    :param make: Vehicle manufacturer
    :param model: Manufacturer’s model designation
    :param type: Vehicle classification (e.g. ``RIGID``, ``ARTIC``, ``VAN``,
        ``BUS``, ``CAR``)
    :param fuel: Fuel type (e.g. ``DIESEL``, ``PETROL``, ``CNG``, ``LNG``,
        ``H2``, ``ELECTRIC``)
    :param fuel_capacity: Full fuel capacity (L or kg or kWh)
    :param fuel_efficiency: Fuel usage over distance (L/km or kg/km or kWh/km)
    :param weight_class: Max weight class (tonnes)
    :param euro_standard: European emission standard
    :param drive_power: Power output of the drive system (kilowatts)
    :param fridge_power: Power output of the cargo cooling system (kilowatts)
    :param limits: Various numeric limits for constraint problems
    """

    _client: 'client.SRFData'
    _org_uri: str
    uri: str
    description: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    type: Optional[str] = None
    fuel: Optional[str] = None
    fuel_capacity: Optional[float] = None
    fuel_efficiency: Optional[float] = None
    weight_class: Optional[float] = None
    euro_standard: Optional[int] = None
    drive_power: Optional[float] = None
    fridge_power: Optional[float] = None
    limits: Mapping[str, float] = immutabledict()

    @property
    def organisation(self) -> 'Organisation':  # noqa: D102
        return self._client.organisations.get(uri=self._org_uri)

    def get_routes(self, lazy=False, **kwargs) -> 'paging.Page[Route]':
        """
        Fetch routes for vehicle class.

        :param lazy: Defer fetching of the Leg objects
        :param kwargs: Additional field filters
        """
        return self._client.routes.find_by_vehicle_class(self, lazy, **kwargs)


@attr.s(frozen=True, slots=True, auto_attribs=True, kw_only=True)
class ExternalVehicleClass:
    """
    A specific make/model/configuration of vehicle from an external system.

    See :class:`~.VehicleClass`.
    """

    description: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    type: Optional[str] = None
    fuel: Optional[str] = None
    fuel_capacity: Optional[float] = None
    fuel_efficiency: Optional[float] = None
    weight_class: Optional[float] = None
    euro_standard: Optional[int] = None
    drive_power: Optional[float] = None
    fridge_power: Optional[float] = None
