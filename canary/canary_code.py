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
        delta = time.time() - t_prev
        extra_time = delta - _CANARY_WAIT_TIME

        # Log the extra time taken by the event loop to get back after the await
        # If you want, you can turn this into a histogram and show the distribution.
        # maybe you could even put it in your metrics.
        activity.logger.info(f"The canary showed the event loop took {round(extra_time,1)} seconds to get back after its await finished")
        print(f"The canary showed the event loop took {round(extra_time,1)} seconds to get back after its await finished")
        t_prev = time.time()



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
