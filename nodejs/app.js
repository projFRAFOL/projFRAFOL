const express = require('express');
const cors = require('cors');
const fs = require('fs');
const { exec } = require('child_process');

const app = express();
const port = 3000;

var corsOptions = {
  origin: 'http://localhost:8000'
}

app.use(express.json(), cors(corsOptions));

app.post('/compile', (req, res) => {
  const javaCode = req.body.code;

  const filePath = 'StudentTest.java';

  // Write Java code to the file
  fs.writeFile(filePath, javaCode, (err) => {
      if (err) {
          console.error('Error writing Java file:', err);
          return;
      }
      console.log('Java file created successfully!');
  });

  // Execute Java compiler
  exec(`javac StudentTest.java`, (error, stdout, stderr) => {
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
