import operator
from typing import TypedDict, Annotated, List

class AgentState(TypedDict):
    repo_name: str
    installation_id: int
    errorMessage: str
    sourceCode: str
    file_path: str
    proposedFix: str
    # Pass the function reference, NOT the function call
    logs: Annotated[List[str], operator.add]