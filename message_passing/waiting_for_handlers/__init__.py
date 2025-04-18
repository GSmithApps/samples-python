from dataclasses import dataclass
from enum import IntEnum

TASK_QUEUE = "my-task-queue"
WORKFLOW_ID = "my-workflow-id"


class WorkflowExitType(IntEnum):
    SUCCESS = 0
    FAILURE = 1
    CANCELLATION = 2


@dataclass
class WorkflowInput:
    exit_type: WorkflowExitType


@dataclass
class WorkflowResult:
    data: str
