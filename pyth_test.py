import os
import glob
import cv2
from hough_test import Window


def main():
    video_path = "/mnt/nas/datasets/crit_air_detection/"
    data_path = "/home/florian/Desktop/Crit_air_data/raw/"
    mask_path = "/home/florian/Desktop/Crit_air_data/mask/"
    if os.listdir(data_path) is []:
        get_raw_images_from_videos(video_path, data_path)
    create_mask(data_path, mask_path)


def create_mask(path_to_img, path_to_mask):
    files = []
    image_size = (800, 600)
    file_index = 0
    if os.path.isfile(path_to_img):
        im = cv2.imread(path_to_img)
    else:
        for r, d, f in os.walk(path_to_img):
            f.sort()
            for file in f:
                if '.jpg' or '.png' in file:
                    files.append(os.path.join(r, file))
        im = cv2.imread(files[0])
    im = cv2.resize(im, image_size)
    windows = []
    windows.append(Window(im, "Color", "color", files[0].split("/")[-1]))
    # windows.append(Window(im, "Circle Hough", "circle_hough"))
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("c"):
            break
        try:
            if key == ord("n"):
                print("n!")
                file_index += 1
                save_masks(windows, path_to_mask)
                im = cv2.imread(files[file_index])
                im = cv2.resize(im, image_size)
                for window in windows:
                    window.set_img(im, files[file_index].split("/")[-1])
            if key == ord("b"):
                file_index -= 1
                im = cv2.imread(files[file_index])
                im = cv2.resize(im, image_size)
                for window in windows:
                    window.set_img(im, files[file_index].split("/")[-1])
        except IndexError:
            print("no more images")
            file_index = 0
    cv2.destroyAllWindows()


def save_masks(windows, path_to_mask):
    for window in windows:
        print(os.path.join(path_to_mask, window.image_name))
        cv2.imwrite(os.path.join(path_to_mask, window.image_name), window.get_mask())


def get_raw_images_from_videos(video_path, image_folder_path):
    files = os.listdir(video_path)
    for file in files:
        if ".MOV" in file:
            print("Entering :", file)
            capture = cv2.VideoCapture(os.path.join(video_path, file))
            ret = True
            number_of_frame = 0
            frame_saved = 0
            while ret:
                ret, img = capture.read()
                number_of_frame += 1
                print(number_of_frame)
                if number_of_frame % 20 == 0:
                    number_of_frame = 0
                    cv2.imwrite((image_folder_path + file + "_" + str(frame_saved) + ".png"), img)
                    frame_saved += 1
                    print("img saved ")


if __name__ == '__main__':
    main()
