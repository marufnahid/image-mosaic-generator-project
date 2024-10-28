import os
import cv2

def load_images(directory, output_dir):
    images = []
    for index, filename in enumerate(os.listdir(directory)):
        img_path = os.path.join(directory, filename)
        img = cv2.imread(img_path)
        if img is not None:
            images.append(img)
            cv2.imwrite(os.path.join(output_dir, f"loaded_image_{index}.jpg"), img)
            print(f"Loaded and saved image: {filename}")
    return images

def resize_images(images, size, output_dir):
    resized_images = []
    for index, img in enumerate(images):
        resized_img = cv2.resize(img, size)
        resized_images.append(resized_img)
        cv2.imwrite(os.path.join(output_dir, f"resized_image_{index}.jpg"), resized_img)
        print(f"Resized image to: {size}")
    return resized_images
