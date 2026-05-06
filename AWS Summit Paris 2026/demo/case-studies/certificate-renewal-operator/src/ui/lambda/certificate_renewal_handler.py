from typing import Protocol, runtime_checkable

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext


def handle(event: dict, context: LambdaContext):
    pass
