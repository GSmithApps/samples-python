from temporalio import workflow


@workflow.defn
class ReversalCoordinator:

    def __init__(self, list_of_ids: list):

        self.list_of_ids = list_of_ids
        self.exit = False

    @workflow.run
    async def run(self):

        await condition(self.exit)

    @workflow.signal
    def registerworkflowid(self, workflow_id: str):
        self.list_of_ids.append(workflow_id)

        if continue_as_new_recommended
            continue_as_new(self.list_of_ids)


    @workflow.signal
    def decision_made(self, decision: bool):
        for id in self.list_of_ids:
            handle = get_workflow_handle(id)
            handle.send_signal("decision_made", decision)

        self.exit = True
