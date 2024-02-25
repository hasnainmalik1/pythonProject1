import os
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

# Get the absolute path to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(script_dir, 'path', 'to', 'save')

# Create the directory if it doesn't exist
os.makedirs(save_path, exist_ok=True)


@app.route('/api/endpoint', methods=['POST'])
def receive_video_data():
    try:
        # Receive video file and parameters from the request
        video_file = request.files['video']
        x = int(request.form['x'])
        y = int(request.form['y'])
        width = int(request.form['width'])
        height = int(request.form['height'])
        # Save or process the video file as needed
        video_file.save(os.path.join(save_path, 'video.jpg'))

        # Crop the region of interest from the saved image
        img = cv2.imread(os.path.join(save_path, 'video.jpg'))
        roi = img[y:y + height, x:x + width]

        # Save the cropped region of interest
        cv2.imwrite(os.path.join(save_path, 'cropped_video.jpg'), roi)

        return jsonify({'message': 'Video data received and processed successfully'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
