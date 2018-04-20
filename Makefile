all: myenv

pip_linux:
	sudo apt-get install -y python3-pip

myenv:
	#brew install python3
	pip3 install virtualenv
	virtualenv -p python3 myenv
	(. myenv/bin/activate && pip install -r requirements.txt)


