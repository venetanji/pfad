import subprocess
import json

base_command = ['gh', 'api', '-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2022-11-28']
forks = []
some_commits = []
zero_commits = []
page = 1
per_page = 50

while True:
    print(f'Getting forks, page {page}')
    gh_command = subprocess.run(
        base_command + [f'/repos/venetanji/pfad/forks?per_page={per_page}&page={page}'],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    gh_forks = json.loads(gh_command.stdout)
    
    if not gh_forks:
        break

    #print(output)
    print(f'Got {len(gh_forks)} forks')

    forks.extend(gh_forks)

    if len(gh_forks) < per_page:
        break
    
    page += 1


print(f'Found a total of {len(forks)} ')
#usernames = [fork['owner']['login'] for fork in forks]

def get_commits(repo):
    commits =  subprocess.run(
        base_command + [f'/repos/{repo}/commits?per_page=100'],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    commits = json.loads(commits.stdout)
    
    commits = [commit for commit
                in commits 
                if not commit['author']
                    or commit['author']['login'] != 'venetanji']

    if len(commits) == 0:
        print(f'\033[91mRepo: {repo} has {len(commits)} commits:\033[0m')
        zero_commits.append(repo)
    else:
        print(f'Repo: {repo} has {len(commits)} commits')
        some_commits.append(repo)

    # for commit in commits:
    #     print(f'Commit {commit["sha"]}\nMessage: {commit["commit"]["message"]}')
    #     print('----\n')
    #print('-----------------------------------')
    #print('\n')

for fork in forks:
    #print(f'Getting commits for {fork["full_name"]}')
    get_commits(fork['full_name'])

print('-----------------------------------')
print('\n')


print(f'\033[92mRepos with some commits: {len(some_commits)}\033[0m')
for repo in some_commits:
    print(repo)

print('-----------------------------------')

print(f'\033[91mRepos with 0 commits: {len(zero_commits)}\033[0m')
for repo in zero_commits:
    print(repo)
