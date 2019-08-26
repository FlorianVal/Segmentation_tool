FROM python:3

WORKDIR ./workspace

RUN pip install imutils pillow opencv-contrib-python

COPY . ./workspace

CMD [ "python", "./workspace/Segmentator.py" ]
