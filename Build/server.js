const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const app = express();

app.use(bodyParser.json());

app.post('/tweet-harvest', (req, res) => {

    // Calculate one year ago from today
    const oneYearAgo = new Date();
    oneYearAgo.setFullYear(oneYearAgo.getFullYear() - 1);
    const formattedDate = oneYearAgo.toISOString().split('T')[0]; // Format: YYYY-MM-DD

    const {username} = req.body;
    const token = ""; // Input your Twitter (X) Auth Token here, keep it hidden.
    const filename = `tweet_${username}.csv`;
    const searchKeyword = `(from:${username}) lang:id since:2023-04-05`; // Update the date as you please
    const limit = 150;

    // Command twitter harvest
    const command = `npx --yes tweet-harvest@2.6.1 -o "${filename}" -s "${searchKeyword}" -l ${limit} --token "${token}"`;

    // Execute the command
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error('Error executing command:', error);
            return res.status(500).send('Error executing command');
        }
        console.log('Command executed successfully');
        console.log('Output:', stdout);
        res.send('Twitter harvest completed successfully');
    });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
