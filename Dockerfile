FROM python:3

WORKDIR ./workspace

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install imutils pillow opencv-contrib-python

COPY . ./workspace

CMD [ "python", "./workspace/Segmentator.py" ]
