import os
from flask import Flask, request, render_template_string, jsonify
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Cloudinary credentials
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

# Professional UI Template with Audio & Modern Layout
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Event Media Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body { 
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; 
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
            color: #f8fafc;
            padding: 1.5rem;
            position: relative;
            overflow-x: hidden;
        }

        /* Subtle animated background light accents */
        body::before {
            content: '';
            position: absolute;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(99,102,241,0.35) 0%, rgba(0,0,0,0) 70%);
            top: 10%;
            left: 15%;
            z-index: 0;
            border-radius: 50%;
            filter: blur(40px);
        }

        .card { 
            position: relative;
            z-index: 1;
            background: rgba(255, 255, 255, 0.07); 
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            width: 100%;
            max-width: 440px; 
            padding: 2.5rem 2rem; 
            border-radius: 24px; 
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            text-align: center;
        }

        .header h1 {
            font-size: 1.65rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header p {
            color: #94a3b8;
            font-size: 0.925rem;
            margin-bottom: 2rem;
        }

        /* Drag & drop file area */
        .drop-zone {
            border: 2px dashed rgba(255, 255, 255, 0.25);
            border-radius: 16px;
            padding: 2rem 1rem;
            background: rgba(255, 255, 255, 0.03);
            cursor: pointer;
            transition: all 0.25s ease;
            margin-bottom: 1.5rem;
        }

        .drop-zone:hover, .drop-zone.dragover {
            border-color: #818cf8;
            background: rgba(99, 102, 241, 0.1);
        }

        .drop-icon {
            font-size: 2.2rem;
            margin-bottom: 0.75rem;
            display: block;
        }

        .drop-text {
            font-size: 0.9rem;
            color: #cbd5e1;
            font-weight: 500;
        }

        .file-input { display: none; }

        .file-info {
            font-size: 0.85rem;
            color: #38bdf8;
            margin-top: 0.5rem;
            font-weight: 600;
            word-break: break-all;
        }

        /* Primary action button */
        .btn-upload { 
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); 
            color: white; 
            border: none; 
            padding: 0.9rem 1.5rem; 
            border-radius: 12px; 
            font-size: 1rem; 
            font-weight: 600; 
            cursor: pointer; 
            width: 100%; 
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .btn-upload:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
        }

        /* Audio Player Styling */
        .audio-container {
            margin-top: 2rem;
            padding-top: 1.25rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }

        .audio-label {
            font-size: 0.8rem;
            color: #94a3b8;
            margin-bottom: 0.5rem;
            display: block;
        }

        audio {
            width: 100%;
            height: 36px;
            filter: invert(0.9) hue-rotate(180deg);
            opacity: 0.8;
        }

        /* Loading Overlay */
        .loading {
            display: none;
            margin-top: 1rem;
            font-size: 0.9rem;
            color: #a5b4fc;
        }
    </style>
</head>
<body>

    <div class="card">
        <div class="header">
            <h1>Capture the Moment ✨</h1>
            <p>Upload your event photos and videos below</p>
        </div>

        <form action="/upload" method="POST" enctype="multipart/form-data" id="uploadForm">
            <div class="drop-zone" onclick="document.getElementById('fileInput').click()">
                <span class="drop-icon">📸</span>
                <span class="drop-text" id="dropText">Tap or drag photos/videos here</span>
                <div class="file-info" id="fileName"></div>
            </div>
            
            <input type="file" name="file" id="fileInput" class="file-input" accept="image/*,video/*" required onchange="showFileName(this)">
            <button type="submit" class="btn-upload" id="submitBtn">Upload Media</button>
        </form>

        <div class="loading" id="loadingText">⏳ Uploading your media... Please hold on.</div>

        <!-- Optional Background Audio Player -->
        <div class="audio-container">
            <span class="audio-label">🎵 Event Soundtrack</span>
            <audio controls loop preload="auto">
                <!-- Replace src link below with your hosted audio/MP3 link -->
                <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
                Your browser does not support audio playback.
            </audio>
        </div>
    </div>

    <script>
        function showFileName(input) {
            const fileNameDiv = document.getElementById('fileName');
            const dropText = document.getElementById('dropText');
            if (input.files && input.files[0]) {
                fileNameDiv.textContent = "Selected: " + input.files[0].name;
                dropText.textContent = "Change selected file";
            }
        }

        document.getElementById('uploadForm').onsubmit = function() {
            document.getElementById('submitBtn').style.opacity = '0.5';
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('loadingText').style.display = 'block';
        };
    </script>
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
    
    upload_result = cloudinary.uploader.upload(
        file, 
        resource_type="auto", 
        folder="event_uploads"
    )
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
                color: #f8fafc;
                text-align: center;
                padding: 1.5rem;
            }}
            .card {{
                background: rgba(255, 255, 255, 0.07);
                backdrop-filter: blur(16px);
                padding: 2.5rem;
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                max-width: 400px;
                width: 100%;
            }}
            a {{ color: #818cf8; text-decoration: none; font-weight: 600; display: inline-block; margin-top: 1rem; }}
            .btn {{ background: #4f46e5; color: white; padding: 0.75rem 1.25rem; border-radius: 10px; margin-top: 1.5rem; display: block; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Success! File Uploaded 🎉</h2>
            <p style="margin-top: 0.5rem; color: #94a3b8;">Thank you for sharing your memory.</p>
            <a href="{upload_result['secure_url']}" target="_blank">View Your Upload</a>
            <a href="/" class="btn">Upload Another Media File</a>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)