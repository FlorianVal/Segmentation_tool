FROM python:3

WORKDIR ./workspace

RUN pip install imutils pillow opencv-contrib-python

ENV DISPLAY=192.168.1.5:0.0
COPY . ./workspace

CMD [ "python", "./workspace/Segmentator.py" ]