"""Contains the main OC Transpo class"""
import os
import json
from typing import List
import requests

from .data import (
    BusType,
    Route,
    RouteSummary,
    NextTripsForStop,
    RouteWithTrips,
    Trip,
    RouteWithTripsAllRoutes,
    NextTripsForStopAllRoutes,
    GTFSTable,
    GTFSConfig,
    GTFSAgency,
    GTFSCalendar,
)
from .error import ERROR_CODES, InvalidKeyError, MissingKeyError


# pylint: disable=invalid-name


def bus_to_enum(bus_type: str) -> BusType:
    """Convert an API-returned bus type to an enum

    Args:
        bus_type (str): The bus type returned by the API

    Returns:
        BusType: An enum representation of the bus type
    """
    # pylint: disable=too-many-return-statements
    if bus_type in ("4", "40"):
        return BusType.FORTY_FOOT
    if bus_type in ("6", "60"):
        return BusType.SIXTY_FOOT
    if bus_type == "4 and 6":
        return BusType.FORTY_OR_SIXTY
    if bus_type == "DD":
        return BusType.DOUBLE_DECKER
    if bus_type == "B":
        return BusType.BIKE_RACK
    if bus_type == "DEH":
        return BusType.HYBRID
    if bus_type == "IN":
        return BusType.INVIRO
    if bus_type == "ON":
        return BusType.ORION

    return BusType.NONE


def api_errors(response: dict, main_key: str) -> dict:
    """Throw errors returned by the API

    Args:
        response (dict): The API response
        main_key (str): The main key in the response (eg. `GetRouteSummaryForStopResult`)

    Raises:
        APIException: Any error received from the API

    Returns:
        dict: If no error is thrown, `response[main_key]`
    """
    if "error" in response:
        raise InvalidKeyError(response["error"])

    response = response[main_key]

    if "Error" in response and response["Error"] != "":
        raise ERROR_CODES[response["Error"]]

    return response


class OCTranspo:
    """The main OC Transpo class

    Args:
        app_id (str): OC Transpo-provided App ID
        api_key (str): OC Transpo-provided API Key
    """

    def __init__(self, app_id: str = None, api_key: str = None):
        self._s = requests.Session()
        # self._headers = {'Content-Type': 'application/json'}
        self._headers = {}

        if app_id is None:
            app_id = os.environ.get("OC_APP_ID")

        if api_key is None:
            api_key = os.environ.get("OC_API_KEY")

        if app_id is None or api_key is None:
            raise MissingKeyError("Missing App ID and/or API Key")

        self._app_id = app_id
        self._api_key = api_key

    def get_route_summary(self, stop: str) -> RouteSummary:
        """Get the routes for a given stop number

        Args:
            stop (str): The 4-digit stop number

        Raises:
            APIException: Any error received from the API

        Returns:
            RouteSummary: The route info
        """
        request_url = (
            "https://api.octranspo1.com/v2.0/GetRouteSummaryForStop"
            f"?appID={self._app_id}&apiKey={self._api_key}&stopNo={stop}&format=json"
        )

        r = self._s.get(request_url, headers=self._headers)
        r_json = api_errors(json.loads(r.content), "GetRouteSummaryForStopResult")

        # Format routes
        routes: List[Route] = []

        for route in r_json["Routes"]["Route"]:
            routes.append(
                Route(
                    route_number=route["RouteNo"],
                    route_heading=route["RouteHeading"],
                    direction=route["Direction"],
                    direction_id=route["DirectionID"],
                )
            )

        return RouteSummary(
            stop_number=r_json["StopNo"],
            stop_label=r_json["StopDescription"],
            routes=routes,
        )

    def get_next_trips(self, stop: str, route_number: str) -> NextTripsForStop:
        """Gets the trips for a given stop and route number.
        Route numbers can be retrieved with OCTranspo.get_route_summary

        Args:
            stop (str): The 4-digit stop number
            route_number (str): The route number

        Raises:
            APIException: Any error received from the API

        Returns:
            NextTripsForStop: The returned data
        """
        request_url = (
            "https://api.octranspo1.com/v2.0/GetNextTripsForStop"
            f"?appID={self._app_id}&apiKey={self._api_key}&stopNo={stop}&routeNo={route_number}"
            "&format=json"
        )

        r = self._s.get(request_url, headers=self._headers)
        r_json = api_errors(json.loads(r.content), "GetNextTripsForStopResult")

        # Convert value to array if it isn't
        if not isinstance(r_json["Route"]["RouteDirection"], list):
            r_json["Route"]["RouteDirection"] = [r_json["Route"]["RouteDirection"]]

        routes: List[RouteWithTrips] = []

        for route in r_json["Route"]["RouteDirection"]:
            trips: List[Trip] = []

            for trip in route["Trips"]["Trip"]:
                trips.append(
                    Trip(
                        latitude=trip["Latitude"],
                        longitude=trip["Longitude"],
                        gps_speed=trip["GPSSpeed"],
                        trip_destination=trip["TripDestination"],
                        trip_start_time=trip["TripStartTime"],
                        adjusted_schedule_time=trip["AdjustedScheduleTime"],
                        adjustment_age=trip["AdjustmentAge"],
                        last_trip_of_schedule=trip["LastTripOfSchedule"],
                        bus_type=bus_to_enum(trip["BusType"]),
                    )
                )

            routes.append(
                RouteWithTrips(
                    route_number=route["RouteNo"],
                    route_description=route["RouteLabel"],
                    direction=route["Direction"],
                    request_processing_time=route["RequestProcessingTime"],
                    trips=trips,
                )
            )

        return NextTripsForStop(
            stop_number=r_json["StopNo"],
            stop_label=r_json["StopLabel"],
            routes=routes,
        )

    def get_next_trips_all_routes(self, stop: str) -> NextTripsForStopAllRoutes:
        """Gets the trips for all routes for a given stop number.

        Args:
            stop (str): The 4-digit stop number

        Raises:
            APIException: Any error received from the API

        Returns:
            NextTripsForStopAllRoutes: The returned data
        """
        request_url = (
            "https://api.octranspo1.com/v2.0/GetNextTripsForStopAllRoutes"
            f"?appID={self._app_id}&apiKey={self._api_key}&stopNo={stop}&format=json"
        )

        r = self._s.get(request_url, headers=self._headers)

        r_json = api_errors(json.loads(r.content), "GetRouteSummaryForStopResult")

        # Convert value to array if it isn't
        if not isinstance(r_json["Routes"]["Route"], list):
            r_json["Routes"]["Route"] = [r_json["Routes"]["Route"]]

        routes: List[RouteWithTripsAllRoutes] = []

        for route in r_json["Routes"]["Route"]:
            trips: List[Trip] = []

            for trip in route["Trips"]:
                if isinstance(trip, str):
                    continue

                trips.append(
                    Trip(
                        latitude=trip["Latitude"],
                        longitude=trip["Longitude"],
                        gps_speed=trip["GPSSpeed"],
                        trip_destination=trip["TripDestination"],
                        trip_start_time=trip["TripStartTime"],
                        adjusted_schedule_time=trip["AdjustedScheduleTime"],
                        adjustment_age=trip["AdjustmentAge"],
                        last_trip_of_schedule=trip["LastTripOfSchedule"],
                        bus_type=bus_to_enum(trip["BusType"]),
                    )
                )

            routes.append(
                RouteWithTripsAllRoutes(
                    route_number=route["RouteNo"],
                    route_heading=route["RouteHeading"],
                    direction=route["Direction"],
                    direction_id=route["DirectionID"],
                    trips=trips,
                )
            )

        return NextTripsForStopAllRoutes(
            stop_number=r_json["StopNo"],
            stop_label=r_json["StopDescription"],
            routes=routes,
        )

    def get_gtfs_table(self, table: GTFSTable, **kwargs: GTFSConfig) -> dict:
        """Get the results from a specified GTFS table

        Args:
            table (GTFSTable): The table ID

        Raises:
            APIException: Any error received from the API

        Returns:
            dict: The parsed returned data
        """
        request_url = "https://api.octranspo1.com/v2.0/Gtfs"

        params = {
            "appID": self._app_id,
            "apiKey": self._api_key,
            "table": table,
            "format": "json",
            **kwargs,
        }

        r = self._s.get(request_url, params=params, headers=self._headers)
        return api_errors(json.loads(r.content), "Gtfs")

    def gtfs_agency(self, **kwargs: GTFSConfig) -> List[GTFSAgency]:
        """Get the `agency` table from the GTFS API

        Raises:
            APIException: Any error received from the API

        Returns:
            List[GTFSAgency]: Data from the agency table
        """
        r_json = self.get_gtfs_table("agency", **kwargs)

        agencies: List[GTFSAgency] = []

        for agency in r_json:
            agencies.append(
                GTFSAgency(
                    id=agency["id"],
                    agency_name=agency["agency_name"],
                    agency_url=agency["agency_url"],
                    agency_timezone=agency["agency_timezone"],
                    agency_lang=agency["agency_lang"],
                )
            )

        return agencies

    def gtfs_calendar(self, **kwargs: GTFSConfig) -> List[GTFSCalendar]:
        """Get the `calendar` table from the GTFS API

        Raises:
            APIException: Any error received from the API

        Returns:
            List[GTFSCalendar]: Data from the calendar table
        """
        r_json = self.get_gtfs_table("calendar", **kwargs)

        calendar: List[GTFSCalendar] = []

        convert = lambda pseudo_bool : pseudo_bool == "1"

        for item in r_json:
            calendar.append(
                GTFSCalendar(
                    id=item["id"],
                    service_id=item["service_id"],
                    monday=convert(item["monday"]),
                    tuesday=convert(item["tuesday"]),
                    wednesday=convert(item["wednesday"]),
                    thursday=convert(item["thursday"]),
                    friday=convert(item["friday"]),
                    saturday=convert(item["saturday"]),
                    sunday=convert(item["sunday"]),
                    start_date=item["start_date"],
                    end_date=item["end_date"],
                )
            )

        return calendar
