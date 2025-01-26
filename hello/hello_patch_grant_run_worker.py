import asyncio

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker

@workflow.defn()
class MyWorkflow:
    @workflow.run
    async def run(self) -> str:

        pass

async def main():

    client = await Client.connect("localhost:7233")

    worker =  Worker(
        client,
        task_queue="hello-patch-task-queue",
        workflows=[MyWorkflow],
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
