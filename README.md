# Segmentation_tool
This Python program aims to test many classic methods of computer vision in order to resolve simple problems or to create more easily a dataset to train a machine learning algorithm

# Run

To run it you need to have Docker installed and run : 

```
docker build . -t segm_tool
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix segm_tool
```

## Implemented features:
- Canny edge detection
- Morphological transform
- WIP
