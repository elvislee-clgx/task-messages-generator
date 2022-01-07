from git import Repo
import sys

def git_push(git_repo_path, env, pipeline_title):
    try:
        repo = Repo(git_repo_path)
        repo.git.add(update=True)
        repo.index.commit("Add task message \"{pipeline_title}\" in {env} ".format(env=env.upper(), pipeline_title=pipeline_title))

        origin = repo.remote(name='origin')
        origin.push()
        print('A new task message [{pipeline_title}] in {env} is created successfully!'.format(env=env.upper(),pipeline_title=pipeline_title))

    except:
        print('Some errors occurred while pushing the code')
