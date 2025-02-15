"""
You could add this to your code
"""

from datetime import timedelta

import asyncio
import time
from temporalio import activity
from temporalio import workflow


_CANARY_WAIT_TIME = 3


@activity.defn
async def canary_activity() -> None:
    """
    Here's the activity that can probe your worker and see if it's
    still responsive.
    """
    t_prev = time.time()
    while True:
        await asyncio.sleep(_CANARY_WAIT_TIME)
        t_new = time.time()
        delay = t_new - (t_prev + _CANARY_WAIT_TIME)
        t_prev = t_new

        # Log the extra time taken by the event loop to get back after the await
        # If you want, you can turn this into a histogram and show the distribution.
        # maybe you could even put it in your metrics.
        activity.logger.info(f"The canary detected {round(delay,3)} seconds of event loop delay.")
        print(f"The canary detected {round(delay,3)} seconds of event loop delay.")


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
