from git import Repo
import sys

# Use the path to your local .git folder
PATH_OF_GIT_REPO = sys.argv[1]

COMMIT_MESSAGE = 'test the 12th commit'

def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)

        origin = repo.remote(name='origin')
        origin.push()
        print('A new commit "{}" is pushed successfully!'.format(COMMIT_MESSAGE))

    except:
        print('Some error occurred while pushing the code')

git_push()