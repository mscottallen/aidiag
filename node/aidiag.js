#!/usr/bin/env node

const fs = require('fs');
const axios = require('axios');
const glob = require('glob');
const readline = require('readline');

const API_URL = "https://api.openai.com/v2/engines/davinci/completions";
const API_KEY = "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";

const path = require('path');
process.env.NODE_PATH = path.join(__dirname, 'node_modules');
require('module').Module._initPaths();

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

async function aggregateLogs() {
    return new Promise((resolve, reject) => {
        const directory = process.cwd();
        glob(directory + '/**/*.{log,out,txt,json}', {}, async (err, files) => {
            if (err) return reject(err);
            
            let concatenatedLogs = '';
            for (let file of files) {
                concatenatedLogs += await fs.promises.readFile(file, 'utf-8');
                concatenatedLogs += '\n';  // Separate content of different files
            }
            
            const tmpFilePath = '/tmp/concatenatedLogs.txt';
            await fs.promises.writeFile(tmpFilePath, concatenatedLogs);
            resolve(tmpFilePath);
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
        const tmpFilePath = await aggregateLogs();
        const logsContent = await fs.promises.readFile(tmpFilePath, 'utf-8');
        
        console.log('Sending logs to ChatGPT for analysis...');
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
