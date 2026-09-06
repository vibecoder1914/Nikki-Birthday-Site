import os
from flask import Flask, request, render_template_string, jsonify
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

app = Flask(__name__)

# Configure Cloudinary credentials
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

# Mobile-friendly upload interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Event Upload</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; text-align: center; padding: 2rem; background: #f4f4f9; }
        .card { background: white; max-width: 400px; margin: 0 auto; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
        input[type="file"] { margin: 1.5rem 0; display: block; width: 100%; }
        button { background: #007AFF; color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; width: 100%; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Share Your Event Photos & Videos 📸</h2>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*,video/*" required>
            <button type="submit">Upload Media</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file attached"}), 400
    
    file = request.files["file"]
    
    # Upload photo/video to Cloudinary folder "event_uploads"
    upload_result = cloudinary.uploader.upload(
        file, 
        resource_type="auto", 
        folder="event_uploads"
    )
    
    return f"""
    <div style="font-family: sans-serif; text-align: center; padding: 2rem;">
        <h2>Success! File uploaded safely. 🎉</h2>
        <p><a href="{upload_result['secure_url']}" target="_blank">View Uploaded File</a></p>
        <a href="/">Upload Another File</a>
    </div>
    """

if __name__ == "__main__":
    app.run(debug=True)