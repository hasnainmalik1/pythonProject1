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
        video_file = request.files['video']
        # Save or process the video file as needed
        video_file.save(os.path.join(save_path, 'video.jpg'))

        # Convert the saved image back to a video
        images = []
        for filename in os.listdir(save_path):
            if filename.endswith(".jpg"):
                img = cv2.imread(os.path.join(save_path, filename))
                height, width, layers = img.shape
                size = (width, height)
                images.append(img)

        out = cv2.VideoWriter(os.path.join(save_path, 'output_video.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), 1, size)
        for image in images:
            out.write(image)
        out.release()

        return jsonify({'message': 'Video data received and converted successfully'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

