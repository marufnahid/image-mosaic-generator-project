from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import cv2
from image_preprocessing import load_images, resize_images
from mosaic_creation import create_mosaic

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_rows = int(request.form['num_rows'])
        num_cols = int(request.form['num_cols'])
        target_image = request.files['target_image']
        tiles_dir = request.form['tiles_dir']

        target_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'target_image.jpg')
        target_image.save(target_image_path)

        output_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'output')
        os.makedirs(output_dir, exist_ok=True)

        if tiles_dir:
            image_database = load_images(tiles_dir, output_dir)
        else:
            image_database = load_images('default_tiles', output_dir)

        target_image = cv2.imread(target_image_path)
        target_height, target_width = target_image.shape[:2]
        grid_size = (num_rows, num_cols)
        tile_size = (target_width // num_cols, target_height // num_rows)

        resized_images = resize_images(image_database, tile_size, output_dir)
        mosaic = create_mosaic(target_image, resized_images, grid_size, alpha=0.5, output_dir=output_dir)
        final_mosaic_path = os.path.join(output_dir, 'final_mosaic.jpg')
        cv2.imwrite(final_mosaic_path, mosaic)

        return jsonify({'redirect': url_for('output', filename='final_mosaic.jpg', rows=num_rows, cols=num_cols)})

    return render_template('index.html')

@app.route('/output/<filename>')
def output(filename):
    rows = request.args.get('rows')
    cols = request.args.get('cols')
    return render_template('output.html', filename=filename, rows=rows, cols=cols)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/tile/<int:row>/<int:col>')
def get_tile(row, col):
    tile_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output', f'tile_{row}_{col}.jpg')
    if os.path.exists(tile_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'] + '/output', f'tile_{row}_{col}.jpg')
    return jsonify({'error': 'Tile not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
