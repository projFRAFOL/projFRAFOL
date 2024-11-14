var editor = CodeMirror.fromTextArea(
    document.getElementById('editor'),{
    mode: "text/x-java",
    indentWithTabs: true,
    autoRefresh:true,
    smartIndent: true,
    lineNumbers: true,
    lineWrapping: true,
    matchBrackets: true,
    autofocus: true,
    extraKeys: {"Ctrl-Space": "autocomplete"},
    theme: "default"
    }
);

editor.setSize(null, "65vh");

var editor2 = CodeMirror.fromTextArea(
    document.getElementById('dev_suite'),{
    mode: "text/x-java",
    indentWithTabs: true,
    autoRefresh:true,
    smartIndent: true,
    lineNumbers: true,
    lineWrapping: true,
    matchBrackets: true,
    autofocus: true,
    theme: "default"
    }
);

editor2.setSize(null, "65vh");

var editor3 = CodeMirror.fromTextArea(
    document.getElementById('test_class'),{
    mode: "text/x-java",
    indentWithTabs: true,
    autoRefresh:true,
    smartIndent: true,
    lineNumbers: true,
    lineWrapping: true,
    matchBrackets: true,
    autofocus: true,
    theme: "default"
    }
);

editor3.setSize(null, 500);

var outputTerminal = CodeMirror.fromTextArea(
    document.getElementById('console'),{
    mode: "text/shell",
    indentWithTabs: true,
    smartIndent: true,
    lineWrapping: true,
    matchBrackets: true,
    autofocus: true,
    readOnly: true,
    theme: "3024-day"
    }
);

outputTerminal.setSize(null, "20vh");

fetch('static/projectdata/dev_suite.java')
    .then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.text();
    })
    .then(javaCode => {
    // Set the content of the CodeMirror editor
    editor2.setValue(javaCode);
    })
    .catch(error => console.error('Error loading Java file:', error));

fetch('static/projectdata/test_class.java')
    .then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.text();
    })
    .then(javaCode => {
    // Set the content of the CodeMirror editor
    editor3.setValue(javaCode);
    })
    .catch(error => console.error('Error loading Java file:', error));

fetch('static/projectdata/StudentTest.java')
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.text();
})
.then(javaCode => {
    // Set the content of the CodeMirror editor
    editor.setValue(javaCode);
})
.catch(error => console.error('Error loading Java file:', error));