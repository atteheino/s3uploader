all: myenv

server_linux:
	sudo apt-get install -y python3-pip
	sudo apt-get install -y python3-setuptools
	sudo apt-get install -y python3-dev
	sudo -H -u s3upload bash -c 'pip3 install wheel'
	sudo -H -u s3upload bash -c 'pip3 install -r requirements.txt'

myenv:
	#brew install python3
	pip3 install virtualenv
	virtualenv -p python3 myenv
	(. myenv/bin/activate && pip install -r requirements.txt)


