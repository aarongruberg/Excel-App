import { spawn } from 'node:child_process';

// Add python3 path as environment variable, need to use path that ends in .zip
// Found path by checking with sys.path in python script
const env = { ...process.env, PYTHONPATH: '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.8/lib/python38.zip' };

const pythonProcess = spawn('python', ['./testscript.py'], {env});

const dataToSend = [1, 2, 3, 4, 5]; 

// Send the array as a JSON string
pythonProcess.stdin.write(JSON.stringify(dataToSend));
pythonProcess.stdin.end();

// Handle output from Python process (if needed)
pythonProcess.stdout.on('data', (data) => {
    console.log(`Python output: ${data}`);
  });
