FROM python:latest
WORKDIR /app
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -yqq unzip python3-pip

RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
	apt-get install -yqq ./google-chrome-stable_current_amd64.deb && \
	rm google-chrome-stable_current_amd64.deb

RUN mkdir -p bin && \
	wget -O ./bin/chromedriver.zip https://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

RUN unzip ./bin/chromedriver.zip chromedriver -d ./bin/ && \
	rm ./bin/chromedriver.zip

RUN pip install -r requirements.txt

COPY src ./src

RUN useradd --user-group --system --create-home --no-log-init yad2
USER yad2

ENV EMAIL="", PASSWORD=""

CMD ["python", "src/main.py", "-d", "./bin/chromedriver", "${EMAIL}", "${PASSWORD}"]