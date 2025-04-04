from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/diff', methods=['POST'])
def diff_pcap():
    # Ensure files are provided
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"error": "Two pcap files are required"}), 400

    # Save uploaded files
    file1 = request.files['file1']
    file2 = request.files['file2']
    file1_path = os.path.join('/tmp', file1.filename)
    file2_path = os.path.join('/tmp', file2.filename)

    # Debugging: Log file paths
    print(f"File 1 path: {file1_path}")
    print(f"File 2 path: {file2_path}")

    try:
        file1.save(file1_path)
        file2.save(file2_path)
    except Exception as e:
        return jsonify({"error": f"Failed to save files: {str(e)}"}), 500

    # Run the pdiff script
    try:
        result = subprocess.run(
            ['python3', '/home/rinas/Desktop/my-projects/pdiff/pdiff.py', '-i', file1_path, '-i', file2_path, '-d'],
            capture_output=True,
            text=True
        )
        output = result.stdout
        error = result.stderr
        if result.returncode != 0:
            return jsonify({"error": error}), 500
        print(f"Backend Response: {output}")  # Debugging: Log the output
        return jsonify({"output": output})
    finally:
        # Clean up temporary files
        if os.path.exists(file1_path):
            os.remove(file1_path)
        if os.path.exists(file2_path):
            os.remove(file2_path)
if __name__ == '__main__':
    app.run(debug=True)