"""Models for OC Transpo data"""
from dataclasses import dataclass
from enum import Enum
from typing import TypedDict, List, Literal, Union


# pylint: disable=invalid-name,too-many-instance-attributes

# PseudoBoolean = Union[Literal["0"], Literal["1"]]
# """Found in GTFS tables. Either the string "0" or "1", meaning true or false."""


GTFSTable = Union[
    Literal["agency"],
    Literal["calendar"],
    Literal["calendar_dates"],
    Literal["routes"],
    Literal["stops"],
    Literal["stop_times"],
    Literal["trips"],
]


class BusType(Enum):
    """Bus type returned by the API"""

    NONE = 0
    FORTY_FOOT = 1
    SIXTY_FOOT = 2
    FORTY_OR_SIXTY = 3
    DOUBLE_DECKER = 4
    BIKE_RACK = 5
    HYBRID = 6
    INVIRO = 7
    ORION = 8


@dataclass(frozen=True)
class Route:
    """Describes an OC Transpo route"""

    route_number: str
    """Route number"""
    route_heading: str
    """Route heading"""
    direction: str
    """Direction description"""
    direction_id: int
    """Direction identifier"""


@dataclass(frozen=True)
class RouteSummary:
    """Returned from the GetRouteSummaryForStop API method"""

    stop_number: str
    """4-digit bus stop number"""
    stop_label: str
    """Label for the stop (eg. "RIDEAU")"""
    routes: List[Route]
    """The routes for the stop"""


@dataclass(frozen=True)
class Trip:
    """Describes a trip for a route"""

    latitude: str
    """Latitude"""
    longitude: str
    """Longitude"""
    gps_speed: Literal[""]
    """Removed from API; Blank string"""
    trip_destination: str
    """Trip heading"""
    trip_start_time: str
    """Scheduled start time for trip"""
    adjusted_schedule_time: str
    """Time until trip is estimated to arrive at stop"""
    adjustment_age: str
    """The time since the schedule was adjusted in minutes"""
    last_trip_of_schedule: bool
    """Whether it is the last trip of the day"""
    bus_type: BusType
    """The type of bus"""


@dataclass(frozen=True)
class RouteWithTrips:
    """Describes a route with info on future trips"""

    route_number: str
    """Route number"""
    route_description: str
    """Route description"""
    direction: str
    """Direction description"""
    request_processing_time: str
    """The time it took to process the request"""
    trips: List[Trip]
    """The trips for the route"""


@dataclass(frozen=True)
class NextTripsForStop:
    """Returned from the GetNextTripsForStop API method"""

    stop_number: str
    """4-digit bus stop number"""
    stop_label: str
    """Label for the stop (eg. "RIDEAU")"""
    routes: List[RouteWithTrips]
    """Routes with trip info"""


@dataclass(frozen=True)
class RouteWithTripsAllRoutes:
    """Describes a route with info on future trips
    for the GetNextTripsForStopAllRoutes API method"""

    route_number: str
    """Route number"""
    route_heading: str
    """Route heading"""
    direction_id: int
    """Direction ID"""
    direction: str
    """Direction? Seems to be empty string"""
    trips: List[Trip]
    """The trips for the route"""


@dataclass(frozen=True)
class NextTripsForStopAllRoutes:
    """Returned from the GetNextTripsForStopAllRoutes API method"""

    stop_number: str
    """4-digit bus stop number"""
    stop_label: str
    """Label for the stop (eg. "RIDEAU")"""
    routes: List[RouteWithTripsAllRoutes]
    """Routes with trip info"""


### GTFS Data ###


class GTFSConfig(TypedDict):
    """Configuration for GTFS API request functions"""

    id: str
    """Specific row ID to get"""
    column: str
    """A specific column in the table"""
    value: str
    """A specific value in a column. Required if column is specified"""
    order_by: str
    """A column to sort by"""
    direction: Union[Literal["asc"], Literal["desc"]]
    """Ascending or descending order for records"""
    limit: int
    """Maximum amount of returned records"""


@dataclass(frozen=True)
class GTFSAgency:
    """GTFS entry for the agency table"""

    id: str
    """Row ID"""
    agency_name: str
    """The name of the agency"""
    agency_url: str
    """The URL for the agency"""
    agency_timezone: str
    """The timezone of the agency"""
    agency_lang: str
    """The language of the agency"""


@dataclass(frozen=True)
class GTFSCalendar:
    """GTFS entry for the calendar table"""

    id: str
    """Row ID"""
    service_id: str
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    start_date: str
    end_date: str
