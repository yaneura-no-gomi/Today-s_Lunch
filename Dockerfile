FROM python:latest

RUN apt-get update 
RUN apt-get -y install \
    tesseract-ocr \
    tesseract-ocr-jpn \
    git
RUN apt-get clean

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# RUN pip install --upgrade pip; \
#     pip install \
#     pillow \
#     pytesseract \
#     pyocr \
#     requests \
#     beautifulsoup4 \
#     pandas \
#     slackbot

WORKDIR /worker
RUN git clone https://github.com/yaneura-no-gomi/Today-s_Lunch.git todayslunch

# ENTRYPOINT ["/usr/bin/tail", "-f", "/dev/null"]
CMD python /worker/todayslunch/slackbot/run.py