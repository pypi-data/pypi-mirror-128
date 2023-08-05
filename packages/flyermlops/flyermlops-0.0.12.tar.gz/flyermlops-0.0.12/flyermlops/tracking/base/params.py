class FlightParams:
    def __init__(self, val_dict):
        self.val_dict = val_dict
        self.values = {}

    def date(self, value):
        self.values["date"] = str(value)

    def timestamp(self, value):
        self.values["timestamp"] = int(value)

    def project_name(self, value):
        self.values["project_name"] = str(value)

    def table_name(self, value):
        self.values["table_name"] = str(value)

    def table_location(self, value):
        self.values["table_location"] = str(value)

    def table_schema(self, value):
        self.values["table_schema"] = str(value)

    def model_location(self, value):
        self.values["model_location"] = str(value)

    def model_name(self, value):
        self.values["model_name"] = str(value)

    def flight_tracking_id(self, value):
        self.values["flight_tracking_id"] = str(value)

    def data_tracking_id(self, value):
        self.values["data_tracking_id"] = str(value)

    def model_tracking_id(self, value):
        self.values["model_tracking_id"] = str(value)

    def features(self, value):
        self.values["features"] = dict(value)

    def git_link(self, value):
        self.values["git_link"] = str(value)

    def storage_location(self, value):
        self.values["storage_location"] = str(value)

    def in_flight(self, value):
        self.values["in_flight"] = bool(value)

    def get_params(self):
        for key, val in self.val_dict.items():
            if key in self.__dir__():
                if val is None:
                    self.values[key] = None
                else:
                    self.__getattribute__(key)(val)

        return self.values


class Metrics:
    def __init__(self, val_dict):
        self.val_dict = val_dict
        self.values = {}

    def date(self, value):
        self.values["date"] = str(value)

    def timestamp(self, value):
        self.values["timestamp"] = int(value)

    def project_name(self, value):
        self.values["project_name"] = str(value)

    def stage(self, value):
        self.values["stage"] = str(value)

    def model_tracking_id(self, value):
        self.values["model_tracking_id"] = str(value)

    def key(self, value):
        self.values["key"] = str(value)

    def value(self, value):
        self.values["value"] = float(value)

    def get_params(self):
        for key, val in self.val_dict.items():
            if key in self.__dir__():
                if val is None:
                    self.values[key] = None
                else:
                    self.__getattribute__(key)(val)

        return self.values


class Params:
    def __init__(self, val_dict):
        self.val_dict = val_dict
        self.values = {}

    def date(self, value):
        self.values["date"] = str(value)

    def timestamp(self, value):
        self.values["timestamp"] = int(value)

    def project_name(self, value):
        self.values["project_name"] = str(value)

    def stage(self, value):
        self.values["stage"] = str(value)

    def model_tracking_id(self, value):
        self.values["tracking_id"] = str(value)

    def key(self, value):
        self.values["key"] = str(value)

    def value(self, value):
        self.values["value"] = float(value)

    def get_params(self):
        for key, val in self.val_dict.items():
            if key in self.__dir__():
                if val is None:
                    self.values[key] = None
                else:
                    self.__getattribute__(key)(val)

        return self.values


class FlightArtifacts:
    def __init__(self, val_dict):
        self.val_dict = val_dict
        self.values = {}

    def date(self, value):
        self.values["date"] = str(value)

    def timestamp(self, value):
        self.values["timestamp"] = int(value)

    def project_name(self, value):
        self.values["project_name"] = str(value)

    def flight_tracking_id(self, value):
        self.values["flight_tracking_id"] = str(value)

    def key(self, value):
        self.values["key"] = str(value)

    def value(self, value):
        self.values["value"] = dict(value)

    def get_params(self):
        for key, val in self.val_dict.items():
            if key in self.__dir__():
                if val is None:
                    self.values[key] = None
                else:
                    self.__getattribute__(key)(val)

        return self.values
