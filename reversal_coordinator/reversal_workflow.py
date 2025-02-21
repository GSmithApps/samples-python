from temporalio import workflow, activity


@workflow.defn
class ReversalWorkflow:

    def __init__(self, merchant):
        self.merchant = merchant
        self.decision_received = False
        self.decision_should_continue_reversal = False

    @workflow.run
    async def run(self):

        if rate_limited():
            reversal_coordinator_handle = get_or_make_reversal_coordinator()

            register_with_handler(reversal_coordinator_handle)

            await condition(self.decision_received)

            if self.decision_should_continue_reversal:
                # continue reversal
                pass
            else:
                # complete
                pass

    @activity.defn
    def get_or_make_reversal_coordinator(self):

        while True:
            try:
                workflow_handle = get_workflow_handle("reversal-coordinator-" + self.merchant)
                return workflow_handle
            except WorkflowExecutionNotFound:
                try:
                    workflow_handle = start_child_workflow(
                        ReversalCoordinator.run,
                        arg=[],
                        id="reversal-coordinator-" + self.merchant,
                        task_queue="reversal-coordinator-task-queue",
                        parent_close_policy='abandon'
                    )
                    return workflow_handle
                except WorkflowExecutionAlreadyStarted:
                    continue

    @activity.defn
    def register_with_handler(self, handle):
        handle.signal("registerworkflowid", workflow.id)

    @workflow.signal
    def decision_made(self, decision_result: bool):
        self.decision_received = True
        self.decision_should_continue_reversal = decision_result
