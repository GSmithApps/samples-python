import asyncio
import sys
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, exceptions, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from hello.hello_patch_grant_run_worker import MyWorkflow


async def main():

    # Uncomment the lines below to see logging output
    # import logging
    # logging.basicConfig(level=logging.INFO)

    client = await Client.connect("localhost:7233")

    await client.execute_workflow(
        MyWorkflow.run,  # type: ignore
        id="hello-patch-workflow-id",
        task_queue="hello-patch-task-queue",
    )


if __name__ == "__main__":
    asyncio.run(main())
