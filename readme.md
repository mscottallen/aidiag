# AiDiag - Linux CLI Tool for AI Augmented Diagnostics and Troubleshooting

AiDiag is a Linux CLI tool that uses OpenAI's language models to help diagnose and troubleshoot issues on Linux systems. It is designed to ingest all of the log files in the current directory, uses AI to analyze the logs and then either outputs a diagnosis (-v, --verbose), a list of possible issues (-b, --brief), or starts a conversation with the user to allow the user to interactively work with the AI to figure out a diagnosis (-i, --interactive).

## Installation

*Dependencies*
- Python 3.6+
- pip3

You will also need an API key from OpenAI. To get one, follow the instructions [here](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/#:~:text=Key%20Takeaways%201%20Go%20to%20OpenAI%27s%20Platform%20website,Secret%20Key%22%20to%20generate%20a%20new%20API%20key.).

### To Install via Ansible:

- Download the latest release from [here](https://github.com/mallen7/aidiag.git)
- Run `cd aidiag` and then `ansible-playbook build.ansible.yml`
- In `/usr/local/aidiag/env.sample` add your API keys and rename the file to `.env`

### To Install via manually:

- Execute `cd /opt` and then `git clone https://github.com/mallen7/aidiag.git`
- Copy the `aidiag/` folder to `/usr/local/` (`cp -r aidiag /usr/local/`)
- Copy the `aidiag` file to `/usr/local/bin/` (`cp aidiag /usr/local/bin/`)
- Execute `cd /usr/local/aidiag/` and then `pip3 install -r requirements.txt`
- In `/usr/local/aidiag/env.sample` add your API keys and rename the file to `.env` (`sed -i 's/placeholder/<REPLACE_WITH_APIKEY>/g' /usr/local/aidiag/env.sample` then `mv /usr/local/aidiag/env.sample /usr/local/aidiag/.env`)
- You can now run `aidiag` from anywhere on the system

## Usage
[GIF Here](https://user.fm/files/v2-447c83075813b0d956c12d186fc4e2bb/AiDiag%20Walkthrough.gif)
![alt text](https://user.fm/files/v2-447c83075813b0d956c12d186fc4e2bb/AiDiag%20Walkthrough.gif)