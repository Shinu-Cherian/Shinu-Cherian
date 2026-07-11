import sys
import os

# Add the parent directory to Python path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.github_api import GitHubClient

def test():
    print("Initializing Client...")
    client = GitHubClient()
    
    print("\nFetching Profile (expecting graceful failure if no token):")
    res = client.get_profile()
    
    if res.success:
        print(f"Success! Username: {res.data.username}")
    else:
        print(f"Graceful Failure Expected: {res.error}")

if __name__ == '__main__':
    test()
