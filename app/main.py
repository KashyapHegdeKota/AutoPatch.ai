from fastapi import FastAPI, Request, BackgroundTasks
from agents.graph import create_agent_graph
import os

app = FastAPI()
# Initialize the graph once
autopatch_agent = create_agent_graph()

def run_agent_workflow_sync(payload: dict):
    """Synchronous task to run the LangGraph agent."""
    print("⚠️ CI/CD Failure Detected. Starting Synchronous Agent...")
    
    # Extract data from the GitHub Webhook payload
    repo_name = payload["repository"]["full_name"]
    installation_id = payload["installation"]["id"]
    
    # In a real scenario, you'd pull this from the Check Run output
    # For testing, we use a mock error that your Researcher regex can catch
    error_msg = 'File "math_engine.py", line 12, in average\nZeroDivisionError: division by zero'

    initial_state = {
        "repo_name": repo_name,
        "installation_id": installation_id,
        "errorMessage": error_msg,
        "logs": []
    }

    # Direct synchronous call to the graph
    result = autopatch_agent.invoke(initial_state)
    
    print(f"--- 🏁 AGENT FINISHED 🏁 ---")
    print(f"File fixed: {result.get('file_path')}")
    print(f"Logs: {result.get('logs')}")
    print(f"Proposed Fix Snippet: {result.get('proposedFix')[:100]}...")

@app.post("/webhook")
async def handle_github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    
    # Filter for the failed check_run event
    if payload.get("check_run", {}).get("conclusion") == "failure":
        # Using BackgroundTasks runs the function in a separate thread automatically
        background_tasks.add_task(run_agent_workflow_sync, payload)
        return {"status": "sync_agent_started"}

    return {"status": "event_ignored"}