import express from "express";
import bodyParser from "body-parser";
import multer from "multer";
import { spawn } from 'node:child_process';

const app = express();
const port = 3000;

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, 'uploads/')
    },
    filename: function (req, file, cb) {
      cb(null, file.originalname)
    }
  })    
  
const upload = multer({storage});

app.use(express.static("public"));



app.get('/', (req, res) => {
    res.render("index.ejs");
});

app.post('/api/uploads', upload.array('avatar', 2), (req, res) => {
    console.log("files uploaded: " + req.files[0].originalname, req.files[1].originalname);

    //Set child process for Python, testing with Zeitgeist's daily-sales.py script
    const childPython = spawn('python', ['./daily-sales.py', JSON.stringify(req.files[0].originalname), JSON.stringify(req.files[1].originalname)]);

    childPython.stdout.on('data', (data) => {
        console.log('stdout: ', data.toString());
    });

    //res.send("uploaded successfully, results file is in downloads folder...");
    //res.download("./daily-sales-summary-2023-02-07-2023-02-08.csv");
    res.render("download.ejs");
});

//route for downloading results csv file
app.get('/download/results', (req, res) => {
    res.download("./daily-sales-summary-2023-02-07-2023-02-08.csv");
});

app.listen(port, () => {
    console.log('listening on port ' + port);
});
