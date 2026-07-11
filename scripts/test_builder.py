import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.profile_builder import ProfileBuilder

def test():
    print("Initializing ProfileBuilder...")
    builder = ProfileBuilder(yaml_path="data/profile.yaml")
    
    print("\nBuilding Profile (Validating, expecting graceful fallback due to missing token)...")
    profile = builder.build(validate=False)
    
    print(f"Name: {profile.name}")
    print(f"GitHub Available: {profile.github_available}")
    print(f"Followers: {profile.followers}")
    print(f"Last Updated: {profile.last_updated}")
    
    print("\nTesting Validation (Should fail if environment is incomplete):")
    try:
        builder.build(validate=True)
    except Exception as e:
        print(f"Validation Error caught: {e}")

if __name__ == '__main__':
    test()
