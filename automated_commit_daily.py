import base64
from github import Github
from github import InputGitTreeElement
import os
import datetime
import schedule
import time


def download_data_and_commit():
    os.system("python3 get_data.py 1")

    REPO_NAME = "OneFourthLabs/COVID-Viz"
    user = "XXXX"
    password = "XXXX"

    g = Github(user, password)
    repo = g.get_repo(REPO_NAME, lazy=False)
    file_list = [
        "india_states.csv",
        "india_states_daily.csv"
    ]

    file_names = [
        "india_states.csv",
        "india_states_daily.csv"
    ]
    commit_message = 'Update files ' + \
        str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
    master_ref = repo.get_git_ref('heads/master')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    element_list = list()
    for i, entry in enumerate(file_list):
        with open(entry) as input_file:
            data = input_file.read()
        if entry.endswith('.png'):
            data = base64.b64encode(data)
        element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
        element_list.append(element)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)


schedule.every().day.at("06:00").do(download_data_and_commit)

while True:
    schedule.run_pending()
    time.sleep(1)

