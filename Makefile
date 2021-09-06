run:
	python src/main.py -d ./bin/chromedriver ${EMAIL} ${PASSWORD}

install: chrome chromedriver
	apt-get install -y python3-pip
	pip install -r requirements.txt

chrome:
	curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
	apt-get install -y ./google-chrome-stable_current_amd64.deb
	rm google-chrome-stable_current_amd64.deb
	
chromedriver:
	mkdir -p bin
	apt-get install -yqq unzip
	wget -O ./bin/chromedriver.zip https://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
	unzip ./bin/chromedriver.zip chromedriver -d ./bin/
	rm ./bin/chromedriver.zip
