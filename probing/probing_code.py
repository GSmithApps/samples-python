"""
You could add this to your code
"""

from datetime import timedelta

import asyncio
import time
from temporalio import activity
from temporalio import workflow


@activity.defn
async def probing_activity() -> None:
    """
    Here's the activity that can probe your worker and see if it's
    still responsive.
    """
    t_prev = time.time()
    while True:
        wait_length = 1
        await asyncio.sleep(wait_length)
        delta = time.time() - t_prev
        extra_time = delta - wait_length
        activity.logger.info(f"probing showed the event loop took {round(extra_time,1)} extra seconds")
        print(f"probing showed the event loop took {round(extra_time,1)} extra seconds")
        t_prev = time.time()



@workflow.defn
class ProbingWorkflow:
    """
    Here's the workflow that can probe your worker and see if it's
    still responsive.
    """

    @workflow.run
    async def run(self) -> str:

        return await workflow.execute_activity(
            probing_activity,

            # these timeouts are going to be tricky because if the event loop
            # is indeed blocked, the heartbeats etc may not behave as expected.
            start_to_close_timeout=timedelta(seconds=60 * 100),
        )
