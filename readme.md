# AiDiag - Linux CLI Tool for AI Augmented Diagnostis and Troubleshooting

AiDiag is a Linux CLI tool that uses AI to help diagnose and troubleshoot issues on Linux systems. It is designed to ingest all of the log files in the current directory it is run in, uses AI to analyze the logs and then either outputs a diagnosis (-v, --verbose), a list of possible issues (-b, --brief), or starts a conversation with the user to allow the user to interactively work with the AI to figure out a diagnosis (-i, --interactive).

## Installation

*Dependencies*
- Python 3.6+
- pip3

### To Install via Ansible:

- Download the latest release from [here](https://github.com/mallen7/aidiag.git)
- Run `cd aidiag` and then `ansible-playbook build.ansible.yml`
- In `/usr/local/aidiag/env.sample` add your API keys and rename the file to `.env`

### To Install via manually:

- Download the latest release from [here](https://github.com/mallen7/aidiag.git)
- Run `cd aidiag` and then `pip3 install -r requirements.txt`
- In `/usr/local/aidiag/env.sample` add your API keys and rename the file to `.env`
- Copy the `aidiag` folder to `/usr/local/`
- Copy the `aidiag` file to `/usr/local/bin/`

## Usage
[GIF Here](https://user.fm/files/v2-447c83075813b0d956c12d186fc4e2bb/AiDiag%20Walkthrough.gif)
![alt text](https://user.fm/files/v2-447c83075813b0d956c12d186fc4e2bb/AiDiag%20Walkthrough.gif)