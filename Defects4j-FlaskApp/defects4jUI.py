from flask import Flask, render_template, request, Response, session, jsonify
from flask_cors import CORS
import os
import json
import pathlib
import io
import re
import pandas as pd

app = Flask(__name__)
app.secret_key = "e60OMnoWrQaHjlz"
app.config["SESSION_COOKIE_NAME"] = "4yRw187RKmd31B4"
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

def get_projects_id():
    project_list = list()
    path = os.path.split(os.getcwd())[0] + 'defects4j/framework/projects'
    items = os.listdir(path)

    for item in items:
        if os.path.isdir(path + '/' + item):
            project_list.append(item)

    return project_list

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

def major_parse(df):
        mutant_list = df["Mutant"].tolist()

        path = '/root/' + session["project"] + 'f/tools_output/major/'
        filetype = "*.csv"
        filename = ""
        for file_path in os.listdir(path):
            if file_path.endswith(filetype[1:]):
                filename = file_path

        path_csv = path + '/' + filename

        kill_csv = pd.read_csv(path_csv)

        mutant_nr = kill_csv["MutantNo"].tolist()
        live_mutant = kill_csv["[FAIL | TIME | EXC | LIVE]"].tolist()

        live_mutant_ids = list()

        for item1, item2 in zip(mutant_nr, live_mutant):
            if item2 == 'LIVE':
                live_mutant_ids.append(item1)

        filetype = "*.log"
        filename = ""
        for file_path in os.listdir(path):
            if file_path.endswith(filetype[1:]):
                filename = file_path

        path_log = path + '/' + filename

        with open(path_log) as f:
            f = f.readlines()

        line_list = list()
        operator_list = list()
        original_list = list()
        mutated_list = list()

        for line in f:
            attributes = re.split(":", line)
            if int(attributes[0]) in live_mutant_ids:
                line_list.append(attributes[5])
                operator_list.append(attributes[1])
                original_list.append(attributes[2])
                mutated_list.append(attributes[3])

        sheet_data = list()

        for item1, item2, item3, item4, item5 in zip(mutant_list, line_list, operator_list, original_list,
                                                     mutated_list):
            sheet_data.append((item1, item2, item3, item4, item5))

        return sheet_data

def pit_parse(df):
        mutant_list = df["Mutant"].tolist()

        json_list = df.iloc[:, 1].tolist()

        line_list = list()

        for i, j in enumerate(json_list):
            j = j.replace("\'", "\"")
            content = json.loads(j)
            line_list.insert(i, content["line"])

        operator_list = list()

        for i, j in enumerate(json_list):
            j = j.replace("\'", "\"")
            content = json.loads(j)
            operator_list.insert(i, content["mutator"][47:])

        class_list = list()

        for i, j in enumerate(json_list):
            j = j.replace("\'", "\"")
            content = json.loads(j)
            class_list.insert(i, content["mutated_class"])

        method_list = list()

        for i, j in enumerate(json_list):
            j = j.replace("\'", "\"")
            content = json.loads(j)
            method_list.insert(i, content["mutated_method"])

        sheet_data = list()

        for item1, item2, item3, item4, item5 in zip(mutant_list, line_list, operator_list, class_list, method_list):
            sheet_data.append((item1, item2, item3, item4, item5))

        return sheet_data

def load_csv():
    path = "/root/results.csv"

    df = pd.read_csv(path)
    return df

def get_class_path(project):
    match project:
        case 'Cli-32':
            return "/root/Cli-32f/src/main/java/org/apache/commons/cli/HelpFormatter.java" 
        case 'Gson-15':
            return "/root/Gson-15f/gson/src/main/java/com/google/gson/stream/JsonWriter.java"
        case 'Lang-53':
            return "/root/Lang-53f/src/java/org/apache/commons/lang/time/DateUtils.java"
        case _:
            print("Invalid project selection was found.")

def get_devsuite_path(project):
    match project:
        case 'Cli-32':
            return "/root/Cli-32f/src/test/java/org/apache/commons/cli/HelpFormatterTest.java" 
        case 'Gson-15':
            return "/root/Gson-15f/gson/src/test/java/com/google/gson/stream/JsonWriterTest.java"
        case 'Lang-53':
            return "/root/Lang-53f/src/test/org/apache/commons/lang/time/DateUtilsTest.java"
        case _:
            print("Invalid project selection was found.")

def file_data(path):
    data = str()
    with open(path, encoding='utf-8') as f:
        data = f.read()

    return data

@app.route('/', methods=['POST', 'GET'])
def index():
    session["ids"] = get_projects_id()
    session["projects"] = get_projects_fromjson()

    return render_template('index.html', all_data = [session["ids"], session["projects"]])

@app.route('/checkout_project', methods=['post'])
def checkout_project():
    project = request.form["select_project"]
    version = request.form["version"]

    session["projects"].append(project + '-' + version)
    session["project_name"] = project
    session["project_version"] = version
    session.modified = True

    cmd = ("defects4j checkout -p " + project + " -v" + version + "f -w $HOME/"
                   + project + "-" + version + "f")
    os.system(cmd)

    cmd = ("defects4j compile -w $HOME/" + project + "-" + version + "f")
    os.system(cmd)

    with open("data.json") as fp:
        data = json.load(fp)

        data.append({
            "name": project + "-" + version
        })

        with open("data.json", 'w') as json_file:
            json.dump(data, json_file,
                      indent=4,
                      separators=(',', ': '))

    return render_template('index.html', all_data = [session["ids"], session["projects"]])

@app.route('/load_project', methods=['post'])
def load_project():
    session["project"] = request.form["project"]
    session["tool"] = request.form["select_tool"]
    session.modified = True
    sheet_data = list()

    path = get_class_path(session["project"])
    test_class = file_data(path)

    file = open("static/projectdata/test_class.java", "w")
    file.write(test_class)
    file.close()

    path = get_devsuite_path(session["project"])
    dev_suite = file_data(path)

    file = open("static/projectdata/dev_suite.java", "w")
    file.write(dev_suite)
    file.close()

    match session["tool"]:
            case "pit":
                table_header = ["Mutant", "Line", "Operator", "Class", "Method"]
            case "major":
                table_header = ["Mutant", "Line", "Operator", "Original", "Mutated"]
            case _:
                print("No tool selection was found.")

    return render_template('project.html', all_data = [session["project"], session["tool"]],
                            table_header = table_header, sheet_data = sheet_data)

@app.route('/coverage', methods=['post'])
def coverage():

    cmd = ("defects4j coverage -w $HOME/" + session["project"] + "f")
    os.system(cmd)

    return Response(status=204)

@app.route('/generate', methods=['post'])
def generate():
    extended = ""

    for item in request.form.getlist("mycheckbox"):
        if item == "extend":
            extended = " -t /root/StudentTest.java"
            print("here")
        elif item == "exclude":
            print("here")
    
    #developer = request.form["option2"]

    ##TO-DO Include and Exclude Extended and Dev test cases.

    path = os.path.split(os.getcwd())[0] + 'defects4j/analyzer/analyzer.py'
    cmd = ("python3 " + path + " run $HOME/" + session["project"] + "f --all-dev" + extended + " --tools " + session["tool"])
    os.system(cmd)

    return Response(status=204)

@app.route('/analyze', methods=['post'])
def analyze():
    path = os.path.split(os.getcwd())[0] + 'defects4j/analyzer/reportsanalyzer.py'
    sheet_data = list()

    match session["tool"]:
            case "pit":
                dir_path = "/root/" + session["project"] + "f/tools_output/pit/"
                filetype = "*.xml"
                filename = ""
                for file_path in os.listdir(dir_path):
                    if file_path.endswith(filetype[1:]):
                        filename = file_path
                cmd = ("python3 " + path + " table -p " + session["project_name"] + " -b "
                           + session["project_version"] + " -t " + session["tool"]
                           + " $HOME/" + session["project"] + "f/tools_output/pit/" + filename
                           + " -o " + "$HOME/results.csv")
                os.system(cmd)
            case "major":
                cmd = ("python3 " + path + " table -p " + session["project_name"] + " -b "
                           + session["project_version"] + " -t " + session["tool"]
                           + " $HOME/" + session["project"] + "f/tools_output/major/ -o "
                           + "$HOME/results.csv")
                os.system(cmd)
            case _:
                print("No tool selection was found.")

    df = load_csv()
    table_header = list()

    match session["tool"]:
            case "pit":
                sheet_data = pit_parse(df)
                table_header = ["Mutant", "Line", "Operator", "Class", "Method"]
            case "major":
                sheet_data = major_parse(df)
                table_header = ["Mutant", "Line", "Operator", "Original", "Mutated"]
            case _:
                print("No tool selection was found.")


    return render_template('project.html', all_data = [session["project"], session["tool"]],
                            table_header = table_header, sheet_data = sheet_data)

@app.route('/summary', methods=['post'])
def summary():
    path = os.path.split(os.getcwd())[0] + 'defects4j/analyzer/reportsanalyzer.py'
    filename = ""

    if session["tool"] == "pit":
        dir_path = dir_path = "/root/" + session["project"] + "f/tools_output/pit/"
        filetype = "*.xml"
        for file_path in os.listdir(dir_path):
            if file_path.endswith(filetype[1:]):
                filename = "/" + file_path

    command = ("python3 " + path + " summary -p " + session["project_name"]
                   + " -b " + session["project_version"] + " -t " + session["tool"] + " $HOME/" + session["project"] + "f/tools_output/" + session["tool"] + filename)
    os.system(command)

    return Response(status=204)

@app.route('/save_testsuite', methods=['post'])
def save_testsuite():
    
    data = request.form["junit_editor"]
    path = "/root/StudentTest.java"
    
    file = open(path, "w")
    file.write(data)
    file.close()

    # java_json = json.dumps({'code': data})

    # nodejs_response = requests.post('http://localhost:3000/compile', json= java_json)

    # if nodejs_response.status_code == 200:
    #     return jsonify({'message': nodejs_response.text})
    # else:
    #     return jsonify({'error': 'Failed to communicate with Node.js server'})

    return Response(status=204)

if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=int('8000'), debug=True)