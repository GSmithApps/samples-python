"""
In your worker initialization, you can add the canary workflow.
"""

from datetime import timedelta
import asyncio
import time

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from canary.your_workflows import YourWorkflow, your_activity

_CANARY_CHECK_RATE = 3


@activity.defn
async def canary_activity() -> None:
    """
    Here's the activity that can probe your worker and see if it's
    still responsive.
    """
    t_prev = time.time()
    while True:
        await asyncio.sleep(_CANARY_CHECK_RATE)
        t_new = time.time()
        delay = t_new - (t_prev + _CANARY_CHECK_RATE)
        t_prev = t_new

        # Log the extra time taken by the event loop to get back after the await
        # If you want, you can turn this into a histogram and show the distribution.
        # maybe you could even put it in your metrics.
        activity.logger.info(
            f"The canary detected {round(delay,4)} seconds of event loop delay."
        )
        print(f"The canary detected {round(delay,4)} seconds of event loop delay.")


@workflow.defn
class CanaryWorkflow:
    """
    Here's the workflow that can probe your worker and see if it's
    still responsive.
    """

    @workflow.run
    async def run(self) -> str:

        return await workflow.execute_activity(
            canary_activity,
            # these timeouts are going to be tricky because if the event loop
            # is indeed blocked, the heartbeats etc may not behave as expected.
            start_to_close_timeout=timedelta(seconds=60 * 100),
        )


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
