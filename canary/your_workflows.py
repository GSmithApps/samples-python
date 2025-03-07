"""
This simulates your code.

You can actually use your own code, but if you want
to use this code as a playground, you can change
the amount of time in the time.sleep() call in
your_activity().
"""

import asyncio
import time
import random
from datetime import timedelta

from temporalio.client import Client
from temporalio import activity, workflow


@activity.defn
async def your_activity() -> None:
    """
    Here's the activity that's in your codebase.

    You can experiment with this one to see how it behaves.
    """

    t0 = time.time()

    # this simulates a long-running activity. this is the piece that we don't
    # know if your code has it or not. This is what we're using the canary for.
    #
    # to illustrate the difference, comment out time.sleep() and uncomment
    # the asyncio.sleep() call.
    # the canary will detect very little delay.
    r = random.random()
    time.sleep(0.5 + r)
    # await asyncio.sleep(.5 + r)

    print(f"Your activity finished after {round(time.time() - t0,1)} seconds")


@workflow.defn
class YourWorkflow:
    @workflow.run
    async def run(self) -> str:

        return await workflow.execute_activity(
            your_activity,
            start_to_close_timeout=timedelta(seconds=60 * 100),
        )


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
