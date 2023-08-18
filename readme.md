## This utility is used to take avantage of OpenAI's language models when diagnosing server problems.
### It does this by concatenating the server logs to a temporary file, feeding the file into the model, then returning the most likely causes of the error. 

### Dependencies:
- Node.js
- npm
- Python
- Ansible

Run `node npm_dep.js` from the project directory to install the dependencies. Then `node aidiag.js` will work even though we'll be calling it by using the environment variable `aidiag`. 

### Usage:

Run aidiag in the folder with the log files you want analyzed. It will be ingested by OpenAI and open an interactive prompt to converse with the model and get the most likely causes of the error.