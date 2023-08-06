from abc import ABC, abstractmethod
from flyermlops.tracking.tracking_objects import FlightTracker
import yaml
import glob
import flyermlops.exceptions as exceptions
import os
import click
from .cli_utils import get_time, stdout_msg


class Flight(ABC):
    def __init__(
        self, config=None, *args, **kwargs,
    ):

        stdout_msg("Beginning initial flight plan diagnostics", fg="red", bold=True)
        self._config = config
        self._get_aircraft_config()
        self._set_flight_tracker()

    def _set_flight_tracker(self):
        """Create unique flight tracking id
        """

        stdout_msg("Setting up flight tracker")
        self._flight_tracker = FlightTracker(part_of_flight=True, **self._config,)

        stdout_msg("Generating unique flight number")
        self._flight_tracking_id = self._flight_tracker.set_tracking_connection()

    def _get_aircraft_config(self):
        """Pulls config that has flight pipelines parameters
        """
        if self._config is None:

            try:
                path = glob.glob(f"./*.yaml")
                path = "".join(path)
                with open(path, "r") as f:
                    self._config = yaml.safe_load(f)

            except FileNotFoundError as not_found:
                raise exceptions.NoConfig(
                    """A yaml configuration file is expected in the current directory 
                    if not povided during base class instantiation"""
                )

        if not isinstance(self._config, dict):
            raise exceptions.NotofTypeDictionary("""A config dictionary is expected""")
