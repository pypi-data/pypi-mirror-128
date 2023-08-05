from .. import exceptions
from ..tracking.base.tracking_base import TrackingBase
from ..tracking.base.params import Params
from ..tracking import tracking_utils
from ..data.connector import DataConnector
import os
import pandas as pd
from typing import List, Dict
import datetime
import time

from flyermlops import tracking


class FlightTracker(TrackingBase):
    def __init__(
        self,
        project_name=None,
        tracking_uri=None,
        tracking_schema=None,
        part_of_flight: bool = False,
        flight_tracking_id: str = None,
        *args,
        **kwargs,
    ):

        super().__init__(
            project_name=project_name,
            tracking_uri=tracking_uri,
            tracking_schema=tracking_schema,
            part_of_flight=part_of_flight,
            flight_tracking_id=flight_tracking_id,
            tracker_type="flight",
            *args,
            **kwargs,
        )

    def set_tracking_connection(self, engine="postgres"):
        super().set_tracking_connection(
            engine=engine,
            flight_tracking_id=self.flight_tracking_id,
            tracking_id=self.tracking_id,
        )

        return self.flight_tracking_id

    def log_artifacts(
        self, key, value, tag=None,
    ):

        data = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "timestamp": time.time(),
            "flight_tracking_id": self.flight_tracking_id,
            "project_name": self.project_name,
            "key": key,
            "value": value,
            "tag": tag,
        }

        tracking_utils.log_registry_values(
            engine=self.tracking_engine,
            registry_schema=self.registries["tracker"],
            data=data,
        )

    def log_to_registry(self, data: dict, tracking_id):
        """Logs data features to data tracking_registry
        
        Args:
            feature_dict: Dictionary of features ({'feature name': feature type})
        """

        tracking_utils.log_registry_values(
            engine=self.tracking_engine,
            registry_schema=self.registries["flight"],
            data=data,
            tracking_id=tracking_id,
        )


class DataTracker(TrackingBase):
    def __init__(
        self,
        project_name,
        tracking_uri,
        tracking_schema,
        part_of_flight: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(
            project_name=project_name,
            tracking_uri=tracking_uri,
            tracking_schema=tracking_schema,
            part_of_flight=part_of_flight,
            tracker_type="data",
            *args,
            **kwargs,
        )

    def set_tracking_connection(self, engine="postgres"):
        return super().set_tracking_connection(engine=engine)

    def set_data_connector(self, style, **kwargs):
        if style == "athena":
            self.athena_client = DataConnector("athena").client(**kwargs)
            print("athena_client")

        elif style == "teradata":
            self.teradata_client = DataConnector("teradata").client(**kwargs)
            print("teradata_client created")

        elif style == "postgres":
            self.postgres_client = DataConnector("postgres").client(**kwargs)
            print("postgres_client created")

    def log_features(self, feature_dict: dict):
        """Logs data features to data tracking_registry
        
        Args:
            feature_dict: Dictionary of features ({'feature name': feature type})
        """

        if type(feature_dict) is not dict:
            raise exceptions.NotofTypeDictionary(
                "A dictionary of feature names and types is expected"
            )

        data = {"features": feature_dict}
        tracking_utils.log_registry_values(
            engine=self.tracking_engine,
            registry_schema=self.registries["tracker"],
            data=data,
            tracking_id=self.tracking_id,
        )

    def run_drift_diagnostics(
        self, reference_data, current_data, column_mapping=None, style="dataframe"
    ):
        pass
        # if style == "dataframe":
        # compute_feature_drift(reference_data, current_data, column_mapping)

    # def run_data_diagnostics(self, reference_data, current_data, numerical_columns=None, categorical_columns=None):
    # if column_mapping is None:
    # feature_dict = current_data.dtypes
    # else:

