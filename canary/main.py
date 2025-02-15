import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from probing.probing_code import ProbingWorkflow, probing_activity
from probing.your_workflows import YourWorkflow, your_activity



async def main():
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="probing-task-queue",
        workflows=[ProbingWorkflow, YourWorkflow],
        activities=[probing_activity, your_activity],
    ):

        # add this to your code
        await client.start_workflow(
            ProbingWorkflow.run,
            id="probing",
            task_queue="probing-task-queue",
        )

        while True:
            # simulate running your workflows

            await client.execute_workflow(
                YourWorkflow.run,
                id="your-workflow",
                task_queue="probing-task-queue",
            )

if __name__ == "__main__":
    asyncio.run(main())
