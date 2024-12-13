import subprocess

def git_add_commit_push(commit_message, branch_name="main"):
    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        print("Changes staged successfully.")

        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("Changes committed successfully.")

        # Push changes to the specified branch
        subprocess.run(["git", "push", "origin", branch_name], check=True)
        print(f"Changes pushed to branch '{branch_name}' successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}. Please check if you're in a valid Git repository and if your branch exists.")

# Example usage
if __name__ == "__main__":
    commit_message = input("Enter your commit message: ")
    branch_name = input("Enter the branch name (default: 'main'): ").strip() or "main"
    git_add_commit_push(commit_message, branch_name)
