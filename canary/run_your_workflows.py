import asyncio

from temporalio.client import Client

from canary.your_workflows import YourWorkflow


async def main():
    client = await Client.connect("localhost:7233")

    while True:
        # simulate running your workflows

        await client.execute_workflow(
            YourWorkflow.run,
            id="your-workflow",
            task_queue="canary-task-queue",
        )

if __name__ == "__main__":
    asyncio.run(main())
