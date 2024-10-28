import numpy as np
import cv2
from image_analysis import average_color, extract_texture_features

def color_difference(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))

def texture_similarity(texture1, texture2):
    return np.mean([np.linalg.norm(t1 - t2) for t1, t2 in zip(texture1, texture2)])

def find_best_match(target_segment, tile_images, weights=(0.5, 0.5)):
    target_avg_color = average_color(target_segment)
    target_texture = extract_texture_features(cv2.cvtColor(target_segment, cv2.COLOR_BGR2GRAY))

    min_score = float('inf')
    best_match = None

    for index, tile in enumerate(tile_images):
        tile_avg_color = average_color(tile)
        tile_texture = extract_texture_features(cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY))

        color_diff = color_difference(target_avg_color, tile_avg_color)
        texture_sim = texture_similarity(target_texture, tile_texture)

        score = weights[0] * color_diff + weights[1] * texture_sim
        print(f"Tile {index}: Color diff: {color_diff}, Texture sim: {texture_sim}, Score: {score}")

        if score < min_score:
            min_score = score
            best_match = tile

    print(f"Best match score: {min_score}")
    return best_match
