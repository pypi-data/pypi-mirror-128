# Core
from typing import Dict
import logging
import os
import re
from flyermlops.tracking.tracking_objects import FlightTracker

# Sagemaker
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.tensorflow import TensorFlow
from sagemaker.workflow.steps import TrainingStep
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.retry import (
    StepRetryPolicy,
    StepExceptionTypeEnum,
    SageMakerJobExceptionTypeEnum,
    SageMakerJobStepRetryPolicy,
)

# Flyermlops

from .cli_utils import stdout_msg
from . import flight_utils


# Get logger
logger = logging.getLogger(__name__)

# Set up flight tracker
config = flight_utils.get_config()
flight_tracker = FlightTracker(part_of_flight=True, **config)
flight_tracker.set_tracking_connection()


# Log s3 storage for flight
STORAGE_BUCKET = config.get("storage_location")
FLIGHT_ID = flight_tracker.flight_tracking_id
PROJECT_NAME = config.get("project_name")
S3_FLIGHT_PATH = f"s3://{STORAGE_BUCKET}/projects/{PROJECT_NAME}/{FLIGHT_ID}"
data = {"storage_location": S3_FLIGHT_PATH}
flight_tracker.log_to_registry(data=data, tracking_id=flight_tracker.flight_tracking_id)

# Add to config
config["s3_flight_path"] = S3_FLIGHT_PATH


def retry_policy(max_retry):
    return [
        StepRetryPolicy(
            exception_types=[
                StepExceptionTypeEnum.SERVICE_FAULT,
                StepExceptionTypeEnum.THROTTLING,
            ],
            expire_after_mins=5,
            interval_seconds=10,
            backoff_rate=2.0,
        ),
        SageMakerJobStepRetryPolicy(
            exception_types=[SageMakerJobExceptionTypeEnum.RESOURCE_LIMIT],
            expire_after_mins=120,
            interval_seconds=60,
            backoff_rate=2.0,
        ),
        SageMakerJobStepRetryPolicy(
            failure_reason_types=[
                SageMakerJobExceptionTypeEnum.INTERNAL_ERROR,
                SageMakerJobExceptionTypeEnum.CAPACITY_ERROR,
            ],
            max_attempts=max_retry,
            interval_seconds=30,
            backoff_rate=2.0,
        ),
    ]


def build_leg(leg, resources, vpc_config, sm_role):
    dags = {}

    logging.info(f"Building {leg} DAGs")
    try:
        if resources["ac_type"] == "sklearn":
            processor = SKLearn(
                entry_point=f"{leg}.py",
                source_dir=f"{config['project_name']}/pipeline/{leg}",
                role=sm_role,
                instance_count=resources["number_engines"],
                instance_type=resources["engine"],
                output_path=f"{config['s3_flight_path']}/{leg}",
                framework_version="0.20.0",
                py_version="py3",
                script_mode=True,
                subnets=vpc_config.subnets,
                security_group_ids=vpc_config.security_group_ids,
            )

            dag = TrainingStep(
                name=leg,
                estimator=processor,
                depends_on=resources["dependencies"] or None,
                retry_policies=retry_policy(resources["retry"]),
            )

        elif resources["ac_type"] == "tensorflow":
            processor = TensorFlow(
                entry_point=f"{leg}.py",
                source_dir=f"{config['project_name']}/pipeline/{leg}",
                role=sm_role,
                instance_count=resources["number_engines"],
                instance_type=resources["engine"],
                output_path=f"{config['s3_flight_path']}/{leg}",
                framework_version="2.4",
                py_version="py37",
                script_mode=True,
                subnets=vpc_config.subnets,
                security_group_ids=vpc_config.security_group_ids,
            )

            dag = TrainingStep(
                name=leg,
                estimator=processor,
                depends_on=resources["dependencies"] or None,
                retry_policies=retry_policy(resources["retry"]),
            )

    except Exception as e:
        print(f"Dag build error for: {leg}")
        raise e

    return dag


def get_flight(config: dict, flight_id: str, sm_role: str = None) -> Dict:

    stdout_msg(
        f"Provisioning resources for flight ID {flight_id}!", fg="red", bold=True,
    )

    # Sagemaker session
    sage_sess = flight_utils.get_session(
        config["s3_flight_path"], config.get("region_name")
    )

    # VPC
    if "vpc_config" in config.keys():
        vpc_config = flight_utils.get_vpc_config(config)

    logger.info("Getting flight legs")

    # flight legs
    flight_leg_dags = {}
    flight_legs = config.get("flight_plan")
    for leg, resources in flight_legs.items():
        stdout_msg(f"Building flight leg: {leg}", fg="white")
        flight_leg_dags[leg] = build_leg(leg, resources, vpc_config, sm_role)

    flight_name = flight_utils.clean_text(config["project_name"])[0]
    flight_workflow = Pipeline(name=flight_name, steps=[*flight_leg_dags.values()],)
    return flight_workflow, flight_name
