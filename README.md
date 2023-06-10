# FREE-GPT-4 <img src="https://github.com/meetkool/FREE-GPT-4/assets/96396841/8ea50f25-df14-40ed-b71c-1fb2a5b44123" width="40" height="40">


A simple chat system using a Python GUI with tkinter, interacting with a GPT-4 model served via a Docker container.
FREEGPT4 is a python chatbot that allows you to have a self-hosted GPT-4 Unlimited and Free WEB API, via the latest Bing's AI.


## Requirements

1. Python3: The language used for development.
2. tkinter: A standard Python library for creating GUI applications.
3. requests: A Python library for making HTTP requests.
4. Docker: A platform to develop, deploy, and run applications inside containers.

## Installation

### Ubuntu-based Systems

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python3 and pip if they are not installed
sudo apt install python3 python3-pip -y

# Install tkinter if it's not installed (usually it is included with python3)
sudo apt install python3-tk -y

# Install requests python package
pip3 install requests

# Install Docker
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce -y

# Adding current user to docker group (optional)
sudo usermod -aG docker $USER

# Test Docker installation
sudo docker run hello-world

```

Please note that if your system is not Ubuntu-based, the installation commands will differ.

## Running the application
```
python3 chat_system.py
```

This will start the GUI and the Docker container running the GPT-4 model. The user can then interact with the model through the GUI.

## If not docker 
By default, the application is configured to interact with the locally-hosted API. If you wish to use the online API, change the URL in the following line in the code:
```
url = "http://127.0.0.1:4040/?" + urlencode({'text': prompt})
```
to 
```
url = "https://free-gpt-4-api.meet508.tech/?" + urlencode({'text': prompt})
```
Also, comment out the following part of the code that is responsible for starting the local API server:
```
#def start_api_server():
#    cmd = "docker container run  -p 4040:5500 d0ckmg/free-gpt4-web-api"
#    process = subprocess.Popen(cmd, shell=True)
#    time.sleep(5)
#    return process

#api_process = start_api_server()
```

This modification allows the application to interact with the online version of the API. Please ensure you have a stable internet connection if you choose to go this route.
