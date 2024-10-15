import json

def create_json_save(save_data):

    with open("static/projectdata/save.json", 'r') as json_file:
        data = json.load(json_file)

    new_save = True

    for project in data["projects"]:
        if save_data["project"] == project["project"]:
            if save_data["version"] == project["data"]["version"]:
                project["data"]["content"]["code"] = save_data["content"]
                new_save = False

    if new_save:
        project_structure = {
            "project": save_data["project"],
            "data": {
                "version": save_data["version"],
                "content": {
                    "code": save_data["content"]
                }
            }
        }
        data["projects"].append(project_structure)

    # Write the JSON file
    with open("static/projectdata/save.json", 'w') as json_file:
        json.dump(data, json_file, indent=4)

def load_json_save(name, version):

    with open("static/projectdata/save.json", 'r') as json_file:
        data = json.load(json_file)  # Load the JSON content
    
    project_code = ""

    # Iterate through each project and extract the code
    for project in data["projects"]:
        if name == project["project"]:
            if version == project["data"]["version"]:
                project_code = project["data"]["content"]["code"]
        
    return project_code