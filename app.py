# This is a simple Flask application that serves a health check endpoint.
from flask import Flask, jsonify

# Create a Flask application instance
app = Flask(__name__)

# Define a health check endpoint
@app.route('/health', methods=['GET'])

# This endpoint returns a JSON response indicating the health status of the application.
def health_check():
    return jsonify({"status": "ok"}), 200

# Define the main entry point of the application
# This block ensures that the application runs only if this script is executed directly.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)