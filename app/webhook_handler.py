from fastapi import FastAPI, Request, HTTPException
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        payload = await request.json()
        check_run = payload.get("check_run", {})
        conclusion = check_run.get("conclusion")

        if conclusion == "failure":
            repo_name = payload["repository"]["full_name"]
            install_id = payload["installation"]["id"]
            run_url = check_run.get("html_url", "N/A")

            print("🚨 FAILURE DETECTED IN AN INSTALLED REPOSITORY! 🚨")
            print(f"Repository: {repo_name}")
            print(f"Installation ID: {install_id}")
            print(f"Check Run URL: {run_url}")
            print("Next steps: Waking up the LangGrapgh worker to handle the failure...")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)