"""
In your worker initialization, you can add the canary workflow.
"""

import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from canary.canary_code import CanaryWorkflow, canary_activity
from canary.your_workflows import YourWorkflow, your_activity



async def main():
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="canary-task-queue",
        workflows=[CanaryWorkflow, YourWorkflow],
        activities=[canary_activity, your_activity],
    ):

        # add this to your code
        await client.execute_workflow(
            CanaryWorkflow.run,
            id="canary",
            task_queue="canary-task-queue",
        )

if __name__ == "__main__":
    asyncio.run(main())
