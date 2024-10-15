import os
import io
import pathlib
import json
import pandas as pd

def get_projects_id():
    project_list = list()
    path = os.path.split(os.getcwd())[0] + 'defects4j/framework/projects'
    items = os.listdir(path)

    for item in items:
        if os.path.isdir(path + '/' + item):
            project_list.append(item)

    return project_list

def get_project_versions(project):
    path = os.path.split(os.getcwd())[0] + 'defects4j/framework/projects/' + project + '/active-bugs.csv'
    df = pd.read_csv(path)
    return df['bug.id'].tolist()

def get_projects_fromjson():
    path = pathlib.Path().resolve() / "data.json"
    project_list = list()

    if os.path.isfile(path) and os.access(path, os.R_OK):
        # checks if file exists
        print("File exists and is readable")
        f = open('data.json')
        data = json.load(f)

        for i in data:
            if "name" in i:
                project_list.append(i['name'])

        f.close()
    else:
        print("Either file is missing or is not readable, creating file...")
        with io.open(os.path.join(pathlib.Path().resolve(), 'data.json'), 'w') as db_file:
            db_file.write(json.dumps([]))

    return project_list