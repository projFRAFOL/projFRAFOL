const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const app = express();
const port = 3000;

var corsOptions = {
  origin: 'http://localhost:8000'
}

app.use(express.json(), cors(corsOptions));

app.post('/checkout', (req, res) => {
  const project = req.body.project;
  const version = req.body.version;

  let cmd = ("defects4j checkout -p " + project + " -v" + version + "f -w $HOME/"
                   + project + "-" + version + "f")

  exec(cmd, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      res.status(500).json({ error: error.message });
      return;
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      res.status(400).json({ error: stderr });
      return;
    }
    console.log(`stdout: ${stdout}`);
    res.json({ message: 'Checkout successful' });
  });
});

app.post('/compile', (req, res) => {
  const javaCode = req.body.code;
  const cppath = req.body.cppath;
  const project = req.body.project;
  const filePath = `/root/${project}f/${req.body.stPath}/StudentTest.java`;
  console.log('FILEPATH: ' + filePath)

  // Write Java code to the file
  fs.writeFile(filePath, javaCode, (err) => {
    if (err) {
        console.error('Error writing Java file:', err);
        return;
    }
    console.log('Java file created successfully!');
  });

  const env = {
    ...process.env, // include existing environment variables
    'test.classes.dir': req.body.stPath,
    'classes.dir': req.body.clPath
  };

  // Execute Java compiler
  exec(`javac -cp "${cppath}" ${filePath}`, { env }, (error, stdout, stderr) => {
    if (error) {
      console.error(`Compilation error: ${error.message}`);
      console.log()
      res.status(500).json({ error: error.message });
      return;
    }
    if (stderr) {
      console.error(`Compilation error: ${stderr}`);
      res.status(400).json({ error: stderr });
      return;
    }
    console.log(`Compilation successful: ${stdout}`);
    res.json({ message: 'Compilation successful' });
  });
  
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
