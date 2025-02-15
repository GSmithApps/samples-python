"""
This simulates your code.

You can actually use your own code, but if you want
to use this code as a playground, you can change
the amount of time in the time.sleep() call in
your_activity().
"""

import asyncio
import time
from temporalio import activity

from datetime import timedelta

from temporalio import workflow

@activity.defn
async def your_activity() -> None:
    """
    Here's the activity that's in your codebase.

    You can experiment with this one to see how it behaves.
    """

    t0 = time.time()

    # this simulates a long-running activity. this is the piece that we don't
    # know if your code has it or not. This is what we're probing for.
    time.sleep(2)

    activity.logger.info(f"your activity has finished after: {round(time.time() - t0,0)} seconds")
    print(f"your activity has finished after: {round(time.time() - t0,0)} seconds")



@workflow.defn
class YourWorkflow:
    @workflow.run
    async def run(self) -> str:

        return await workflow.execute_activity(
            your_activity,
            start_to_close_timeout=timedelta(seconds=60 * 100),
        )

