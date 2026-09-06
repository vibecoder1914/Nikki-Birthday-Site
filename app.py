import os
from flask import Flask, request, render_template_string, jsonify
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Cloudinary credentials
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

# Professional UI Template with Gold Banner, Spaced Layout, Audio & Live Gallery
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fierce at 50! - Event Media Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body { 
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; 
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            
            /* Custom background image with a dark overlay */
            background: linear-gradient(rgba(15, 23, 42, 0.65), rgba(15, 23, 42, 0.75)), 
                        url('/static/bg.png') no-repeat center center fixed;
            background-size: cover;
            
            color: #f8fafc;
            padding: 2rem 1rem 4rem 1rem;
        }

        /* Gold Banner Header */
        .gold-banner {
            width: 100%;
            max-width: 800px;
            text-align: center;
            padding: 1.5rem 1rem;
            margin-top: 2rem;
            margin-bottom: 8rem; /* Creates space so the background photo is visible */
            background: rgba(15, 23, 42, 0.4);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 20px;
            border: 1px solid rgba(212, 175, 55, 0.4);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(212, 175, 55, 0.2);
        }

        .gold-banner h1 {
            font-family: 'Cinzel', serif;
            font-size: clamp(2.2rem, 6vw, 3.8rem);
            font-weight: 700;
            letter-spacing: 2px;
            background: linear-gradient(135deg, #FFE57F 0%, #D4AF37 50%, #AA7C11 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
            text-transform: uppercase;
        }

        .container {
            width: 100%;
            max-width: 800px;
            display: flex;
            flex-direction: column;
            gap: 3rem;
            align-items: center;
        }

        /* Upload Card Container */
        .card { 
            background: rgba(255, 255, 255, 0.08); 
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            width: 100%;
            max-width: 480px; 
            padding: 2.5rem 2rem; 
            border-radius: 24px; 
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            text-align: center;
        }

        .header h2 {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header p { color: #94a3b8; font-size: 0.925rem; margin-bottom: 1.5rem; }

        .drop-zone {
            border: 2px dashed rgba(212, 175, 55, 0.4);
            border-radius: 16px;
            padding: 2rem 1rem;
            background: rgba(255, 255, 255, 0.03);
            cursor: pointer;
            transition: all 0.25s ease;
            margin-bottom: 1.5rem;
        }

        .drop-zone:hover { 
            border-color: #D4AF37; 
            background: rgba(212, 175, 55, 0.1); 
        }
        
        .drop-icon { font-size: 2.2rem; margin-bottom: 0.75rem; display: block; }
        .drop-text { font-size: 0.9rem; color: #cbd5e1; font-weight: 500; }
        .file-input { display: none; }
        .file-info { font-size: 0.85rem; color: #FFE57F; margin-top: 0.5rem; font-weight: 600; }

        .btn-upload { 
            background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%); 
            color: #0f172a; border: none; padding: 0.9rem 1.5rem; 
            border-radius: 12px; font-size: 1rem; font-weight: 700; 
            cursor: pointer; width: 100%; 
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .btn-upload:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
        }

        .audio-container { margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1); }
        .audio-label { font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.5rem; display: block; }
        audio { width: 100%; height: 32px; filter: invert(0.9) hue-rotate(180deg); opacity: 0.8; }
        .loading { display: none; margin-top: 1rem; font-size: 0.9rem; color: #FFE57F; }

        /* Gallery Section */
        .gallery-section { width: 100%; }
        .gallery-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 1rem; text-align: left; color: #f1f5f9; }
        
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 1rem;
            width: 100%;
        }

        .gallery-item {
            position: relative;
            aspect-ratio: 1 / 1;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.12);
            background: rgba(0,0,0,0.3);
        }

        .gallery-item img, .gallery-item video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .gallery-item:hover img, .gallery-item:hover video {
            transform: scale(1.05);
        }
    </style>
</head>
<body>

    <!-- Gold Banner Header -->
    <div class="gold-banner">
        <h1>Fierce at 50!</h1>
    </div>

    <div class="container">
        <!-- Upload Card -->
        <div class="card">
            <div class="header">
                <h2>Capture the Moment ✨</h2>
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

            <div class="audio-container">
                <span class="audio-label">🎵 Event Soundtrack</span>
                <audio controls loop preload="auto">
                    <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
                </audio>
            </div>
        </div>

        <!-- Live Photo/Video Gallery -->
        <div class="gallery-section">
            <h2 class="gallery-title">Live Event Gallery</h2>
            <div class="gallery-grid">
                {% for item in media_items %}
                    <div class="gallery-item">
                        {% if item.resource_type == 'video' %}
                            <video src="{{ item.secure_url }}" controls preload="metadata"></video>
                        {% else %}
                            <a href="{{ item.secure_url }}" target="_blank">
                                <img src="{{ item.secure_url }}" alt="Event Media">
                            </a>
                        {% endif %}
                    </div>
                {% else %}
                    <p style="color: #94a3b8; font-size: 0.9rem;">No photos or videos uploaded yet. Be the first!</p>
                {% endfor %}
            </div>
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
    media_items = []
    try:
        # Fetch up to 12 recent uploads from Cloudinary
        response = cloudinary.api.resources(
            type="upload",
            prefix="event_uploads/",
            max_results=12,
            direction="desc"
        )
        media_items = response.get("resources", [])
    except Exception as e:
        print("Error fetching media from Cloudinary:", e)

    return render_template_string(HTML_TEMPLATE, media_items=media_items)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file attached"}), 400
    
    file = request.files["file"]
    
    cloudinary.uploader.upload(
        file, 
        resource_type="auto", 
        folder="event_uploads"
    )
    
    return """
    <script>
        alert("Upload successful! 🎉");
        window.location.href = "/";
    </script>
    """

if __name__ == "__main__":
    app.run(debug=True)