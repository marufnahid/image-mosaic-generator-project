import cv2
import numpy as np

def average_color(image):
    avg_color = cv2.mean(image)[:3]
    print(f"Average color: {avg_color}")
    return avg_color

def extract_texture_features(image):
    gabor_kernels = []
    for theta in np.arange(0, np.pi, np.pi / 4):
        kernel = cv2.getGaborKernel((21, 21), 3, theta, 10, 0.5, 0, ktype=cv2.CV_32F)
        gabor_kernels.append(kernel)

    features = []
    for kernel in gabor_kernels:
        filtered = cv2.filter2D(image, cv2.CV_8UC3, kernel)
        features.append(filtered)
    print(f"Extracted texture features: {len(features)}")
    return features
