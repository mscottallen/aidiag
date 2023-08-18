const fs = require('fs');
const axios = require('axios');
const glob = require('glob');
const readline = require('readline');

const API_URL = "https://api.openai.com/v2/engines/davinci/completions";
const API_KEY = "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";

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

async function aggregateLogs(directory) {
    return new Promise((resolve, reject) => {
        glob(directory + '/**/*.{log,out,txt,json}', {}, (err, files) => {
            if (err) return reject(err);

            let content = '';
            files.forEach(file => {
                content += fs.readFileSync(file, 'utf-8') + '\n';
            });
            resolve(content);
        });
    });
}

async function sendToChatGPT(content) {
    const response = await axios.post(API_URL, {
        prompt: content,
        max_tokens: 150  // Adjust as needed
    }, {
        headers: {
            'Authorization': `Bearer ${API_KEY}`,
            'Content-Type': 'application/json'
        }
    });
    return response.data.choices[0].text.trim();
}

async function main() {
    try {
        const logsContent = await aggregateLogs('.');
        console.log(await sendToChatGPT(logsContent));

        rl.on('line', async (userInput) => {
            if (userInput.toLowerCase() === 'exit' || userInput.toLowerCase() === 'quit') {
                rl.close();
                return;
            }
            const response = await sendToChatGPT(userInput);
            console.log(`ChatGPT: ${response}`);
        });
    } catch (error) {
        console.error("Error:", error);
    }
}

main();
