import asyncio
from dataclasses import dataclass
from typing import List, Set

from temporalio import activity


@dataclass
class AssignNodesToJobInput:
    nodes: List[str]
    job_name: str


@dataclass
class ClusterState:
    node_ids: List[str]


@activity.defn
async def start_cluster() -> ClusterState:
    return ClusterState(node_ids=[f"node-{i}" for i in range(25)])


@activity.defn
async def assign_nodes_to_job(input: AssignNodesToJobInput) -> None:
    print(f"Assigning nodes {input.nodes} to job {input.job_name}")
    await asyncio.sleep(0.1)


@dataclass
class UnassignNodesForJobInput:
    nodes: List[str]
    job_name: str


@activity.defn
async def unassign_nodes_for_job(input: UnassignNodesForJobInput) -> None:
    print(f"Deallocating nodes {input.nodes} from job {input.job_name}")
    await asyncio.sleep(0.1)


@dataclass
class FindBadNodesInput:
    nodes_to_check: Set[str]


@activity.defn
async def find_bad_nodes(input: FindBadNodesInput) -> Set[str]:
    await asyncio.sleep(0.1)
    bad_nodes = set([id for id in input.nodes_to_check if hash(id) % 5 == 0])
    if bad_nodes:
        print(f"Found bad nodes: {bad_nodes}")
    else:
        print("No new bad nodes found.")
    return bad_nodes
