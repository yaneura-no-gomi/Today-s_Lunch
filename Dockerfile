FROM python:latest

RUN apt-get update
RUN apt-get -y install \
    tesseract-ocr \
    tesseract-ocr-jpn
RUN apt-get clean

RUN pip install --upgrade pip; \
    pip install \
    pillow \
    pytesseract \
    pyocr \
    requests \
    beautifulsoup4 \
    pandas \
    slackbot \
    slacker

CMD /usr/bin/tail -f /dev/null

WORKDIR work
COPY . .
RUN pip install -r requirements.txt
CMD python slackbot/run.py