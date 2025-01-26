"""
In this video, we'll finish our discussion of the behavior
of the patched function. We'll
show what it does when replaying, and the patch ID
is nowhere in the event history.

- if replaying, and the code has a call to patched,
  - if the patch ID is somewhere in the event history
    - ...
  - if the patch ID is not anywhere in the event history
    - it will return false and not add anything to
      the event history. Furthermore, and this is the
      caveat, it will make all future calls to patched
      with that ID false -- even after it is done replaying
      and is running normal code.


Why is this a caveat?
- in the first video, we said that if not replaying,
  the patched function will always return true, and if
  the marker doesn't exist, it will add it, and if
  the marker already exists, it won't re-add it.

  But what this
  is saying is that this doesn't hold if there was already
  a call to patched with that ID in the replay code, but not
  in the event history.
"""

import asyncio

from temporalio import activity, workflow
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
