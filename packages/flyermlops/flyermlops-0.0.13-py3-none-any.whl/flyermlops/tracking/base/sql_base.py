from sqlalchemy import (
    Column,
    String,
    Table,
    ForeignKey,
    Integer,
    Boolean,
    Float,
    BigInteger,
    JSON,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

import time

base = declarative_base()


class SqlFlightRegistrySchema(base):
    __tablename__ = "flight_registry"

    date = Column("date", String)
    timestamp = Column("timestamp", BigInteger)
    project_name = Column("project_name", String)
    flight_tracking_id = Column("flight_tracking_id", String, primary_key=True)
    data_tracking_id = Column("data_tracking_id", String)
    model_tracking_id = Column("model_tracking_id", String)
    metrics = Column("metrics", JSON)
    git_link = Column("git_link", String)
    storage_location = Column("storage_location", String)
    in_flight = Column("in_flight", Boolean, default=True)

    __table_args__ = {"schema": "ml_metadata"}

    def __repr__(cls):
        return f"<SqlMetric({cls.__tablename__}"


class SqlDataRegistrySchema(base):
    __tablename__ = "data_registry"

    date = Column("date", String)
    timestamp = Column("timestamp", BigInteger)
    project_name = Column("project_name", String)
    data_tracking_id = Column("data_tracking_id", String, primary_key=True)
    table_name = Column("table_name", String)
    features = Column("features", JSON)
    table_location = Column("table_location", String)
    table_schema = Column("table_schema", String)
    git_link = Column("git_link", String)
    in_flight = Column("in_flight", Boolean, default=True)

    __table_args__ = {"schema": "ml_metadata"}

    def __repr__(cls):
        return f"<SqlMetric({cls.__tablename__}"


class SqlModelRegistrySchema(base):
    __tablename__ = "model_registry"

    date = Column("date", String)
    timestamp = Column("timestamp", BigInteger)
    project_name = Column("project_name", String)
    model_tracking_id = Column("model_tracking_id", String, primary_key=True)
    data_tracking_id = Column("data_tracking_id", String)
    model_name = Column("model_name", String)
    model_location = Column("table_location", String)
    features = Column("features", JSON)
    git_link = Column("git_link", String)
    in_flight = Column("in_flight", Boolean, nullable=False, default=True)

    __table_args__ = {"schema": "ml_metadata"}

    def __repr__(cls):
        return f"<SqlMetric({cls.__tablename__}"


class SqlFlightArtifactRegistrySchema(base):
    __tablename__ = "flight_artifact_registry"

    date = Column("date", String)
    timestamp = Column("timestamp", BigInteger)
    project_name = Column("project_name", String)
    flight_tracking_id = Column("flight_tracking_id", String, primary_key=True)
    key = Column("key", String)
    value = Column("value", JSON)
    tag = Column("tag", String)

    __table_args__ = {"schema": "ml_metadata"}

    def __repr__(cls):
        return f"<SqlMetric({cls.__tablename__}"


class SqlMetricRegistrySchema(base):
    __tablename__ = "model_metric_registry"

    date = Column("date", String)
    timestamp = Column("timestamp", BigInteger)
    project_name = Column("project_name", String)
    stage = Column("stage", String)
    model_tracking_id = Column("model_tracking_id", String, primary_key=True)
    key = Column("key", String)
    value = Column("value", Float)

    __table_args__ = {"schema": "ml_metadata"}

    def __repr__(cls):
        return f"<SqlMetric({cls.__tablename__}"


class SqlParamRegistrySchema(base):
    __tablename__ = "model_param_registry"

    date = Column("date", String)
    timestamp = Column("timestamp", BigInteger)
    project_name = Column("project_name", String)
    stage = Column("stage", String)
    model_tracking_id = Column("model_tracking_id", String, primary_key=True)
    key = Column("key", String)
    value = Column("value", Float)

    __table_args__ = {"schema": "ml_metadata"}

    def __repr__(cls):
        return f"<SqlMetric({cls.__tablename__}"
