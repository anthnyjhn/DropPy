cd to the parent directory of wifi_file_server.py

// INstall venv in system
sudo apt install python3-venv -y

// create Virtual environment for the project only
python3 -m venv venv

// activate project
source venv/bin/activate

// install all dependencies
pip install flask qrcode[pil] terminaltables netifaces
