from flask import Flask, request, send_file, Response
import requests
from io import BytesIO
from config import secret_key
app = Flask(__name__)


@app.route('/download_image', methods=['GET'])
def download_image():
    if not request.args.get('password'):
        return "Missing 'password' parameter", 400

    if request.args.get('password') != secret_key:
        return "Invalid password", 401

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


@app.route('/url', methods=['GET'])
def url_proxy():
    if not request.args.get('password'):
        return "Missing 'password' parameter", 400

    if request.args.get('password') != secret_key:
        return "Invalid password", 401

    # Get the 'url' parameter from the request
    target_url = request.args.get('url')

    if not target_url:
        return "Missing 'url' parameter", 400

    try:
        # Send a GET request to the target URL
        response = requests.get(target_url)

        # If the request was successful, return the content (assuming it's XML)
        if response.status_code == 200:
            return Response(response.content, content_type='application/xml')

        # Handle error if URL request fails
        return f"Failed to fetch URL. Status code: {response.status_code}", 400

    except Exception as e:
        return f"Error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5823, debug=True)
