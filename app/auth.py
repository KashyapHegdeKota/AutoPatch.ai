from github import Github, GithubIntegration
import os

def get_installation_token(installation_id):
    try:
        # 1. Read the private key
        with open(os.getenv("GITHUB_PRIVATE_KEY_PATH"), "r") as f:
            private_key = f.read()

        # 2. Initialize the Integration
        integration = GithubIntegration(
            os.getenv("GITHUB_APP_ID"),
            private_key,
        )

        # 3. Get the access token for this specific repo installation
        # This is where 'None' usually comes from if the ID is wrong
        access_token = integration.get_access_token(installation_id)
        
        return Github(access_token.token)
    
    except Exception as e:
        print(f"❌ GITHUB AUTH FAILED: {str(e)}")
        return None