import subprocess

def git_add_commit_push(commit_message):
    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        print("Changes staged successfully.")

        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("Changes committed successfully.")

        # Push changes to the current branch
        subprocess.run(["git", "push"], check=True)
        print("Changes pushed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}. Please ensure you're in a valid Git repository and connected to a remote repository.")

# Example usage
if __name__ == "__main__":
    commit_message = input("Enter your commit message: ")
    git_add_commit_push(commit_message)
