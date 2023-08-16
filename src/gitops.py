import git

'''
Given a repo path and a commit_id checkout the same at repo_dload_path
'''
def clone_checkout_commit(repo_url, repo_dload_path, commit_id):
    repo = git.Repo.clone_from(repo_url, repo_dload_path, no_checkout=True)
    repo.git.checkout(commit_id)
    return


if __name__ == "__main__":
    clone_checkout_commit("https://github.com/eBPFDevSecTools/annotations-search-ui.git","C:\\Users\\08714Q744\\git","43ec66a0ba0c8784bcb817001ae8d8ea019dc85a")