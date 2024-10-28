import cv2
import os
from tkinter import Tk, Label, Entry, Button
from image_preprocessing import load_images, resize_images
from best_match import find_best_match
from mosaic_creation import create_mosaic

def create_input_dialog():
    def submit():
        nonlocal num_rows, num_cols
        num_rows = int(rows_entry.get())
        num_cols = int(cols_entry.get())
        root.destroy()

    root = Tk()
    root.title("Grid Input")

    Label(root, text="Number of Rows:").grid(row=0, column=0)
    rows_entry = Entry(root)
    rows_entry.grid(row=0, column=1)

    Label(root, text="Number of Columns:").grid(row=1, column=0)
    cols_entry = Entry(root)
    cols_entry.grid(row=1, column=1)

    Button(root, text="Submit", command=submit).grid(row=2, columnspan=2)

    num_rows, num_cols = 0, 0
    root.mainloop()
    return num_rows, num_cols

def show_original_image(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        tile_height = params['target_height'] // params['num_rows']
        tile_width = params['target_width'] // params['num_cols']
        row = y // tile_height
        col = x // tile_width

        tile_image_path = os.path.join(params['output_dir'], f"tile_{row}_{col}.jpg")
        if os.path.exists(tile_image_path):
            original_image = cv2.imread(tile_image_path)
            if original_image is not None:
                original_height, original_width = original_image.shape[:2]
                scale_factor = min(800 / original_width, 600 / original_height)
                resized_original = cv2.resize(original_image, None, fx=scale_factor, fy=scale_factor)
                cv2.imshow(f"Original Tile {row}, {col}", resized_original)
            else:
                print(f"Failed to load tile image: {tile_image_path}")
        else:
            print(f"Tile image not found: {tile_image_path}")

def main():
    image_dir = "C:\\Users\\Maruf\\Desktop\\Python\\project\\mosaic_tiles"
    output_dir = "C:\\Users\\Maruf\\Desktop\\Python\\project\\output"
    os.makedirs(output_dir, exist_ok=True)

    image_database = load_images(image_dir, output_dir)
    print(f"Number of images loaded: {len(image_database)}")

    target_image_path = "C:\\Users\\Maruf\\Desktop\\Python\\project\\input_image1.jpg"
    target_image = cv2.imread(target_image_path)
    if target_image is None:
        print(f"Failed to load target image: {target_image_path}")
        return

    target_height, target_width = target_image.shape[:2]
    cv2.imwrite(os.path.join(output_dir, "target_image.jpg"), target_image)

    num_rows, num_cols = create_input_dialog()
    grid_size = (num_rows, num_cols)
    tile_size = (target_width // num_cols, target_height // num_rows)

    resized_images = resize_images(image_database, tile_size, output_dir)
    print(f"Number of images resized: {len(resized_images)}")
    print(f"Tile size: {tile_size}")

    mosaic = create_mosaic(target_image, resized_images, grid_size, alpha=0.5, output_dir=output_dir)
    mosaic_height, mosaic_width = mosaic.shape[:2]
    scale_factor = min(800 / mosaic_width, 600 / mosaic_height)
    resized_mosaic = cv2.resize(mosaic, None, fx=scale_factor, fy=scale_factor)
    cv2.imwrite(os.path.join(output_dir, "final_mosaic.jpg"), mosaic)

    cv2.namedWindow("Mosaic", cv2.WINDOW_NORMAL)
    cv2.imshow("Mosaic", resized_mosaic)

    cv2.setMouseCallback("Mosaic", show_original_image, {
        'target_height': target_height,
        'target_width': target_width,
        'num_rows': num_rows,
        'num_cols': num_cols,
        'output_dir': output_dir
    })

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
