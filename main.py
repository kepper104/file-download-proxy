from flask import Flask, request, send_file
import requests
from io import BytesIO

app = Flask(__name__)


@app.route('/download_image', methods=['GET'])
def download_image():
    # Get the 'url' parameter from the request
    image_url = request.args.get('url')

    if not image_url:
        return "Missing 'url' parameter", 400

    try:
        # Send a GET request to the image URL
        response = requests.get(image_url)

        # Check if the request was successful
        if response.status_code != 200:
            return f"Failed to download image. Status code: {response.status_code}", 400

        # Create a BytesIO stream from the image data
        img_data = BytesIO(response.content)

        # Return the image back to the client
        return send_file(img_data, mimetype='image/jpeg')  # Adjust mimetype if necessary

    except Exception as e:
        return f"Error occurred: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
