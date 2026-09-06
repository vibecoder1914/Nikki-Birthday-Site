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
            background: linear-gradient(rgba(15, 23, 42, 0.65), rgba(15, 23, 42, 0.75)), 
                        url('/static/bg.png') no-repeat center center fixed;
            background-size: cover;
            color: #f8fafc;
            padding: 2rem 1rem 4rem 1rem;
        }

        .gold-banner {
            width: 100%;
            max-width: 800px;
            text-align: center;
            padding: 1.5rem 1rem;
            margin-top: 2rem;
            margin-bottom: 6rem;
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
            text-transform: uppercase;
        }

        .container {
            width: 100%;
            max-width: 800px;
            display: flex;
            flex-direction: column;
            gap: 2.5rem;
            align-items: center;
        }

        .card { 
            background: rgba(255, 255, 255, 0.08); 
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            width: 100%;
            max-width: 520px; 
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
            color: #ffffff;
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

        .drop-zone:hover { border-color: #D4AF37; background: rgba(212, 175, 55, 0.1); }
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
        }

        /* Active Scrolling Carousel */
        .carousel-container {
            width: 100%;
            overflow: hidden;
            margin-top: 1.5rem;
            border-radius: 16px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 0.75rem;
        }

        .carousel-title {
            font-size: 0.85rem;
            color: #FFE57F;
            font-weight: 600;
            margin-bottom: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .carousel-track {
            display: flex;
            gap: 12px;
            animation: scroll 15s linear infinite;
            width: max-content;
        }

        .carousel-track:hover { animation-play-state: paused; }

        @keyframes scroll {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }

        .carousel-item {
            width: 110px;
            height: 110px;
            flex-shrink: 0;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.2);
            cursor: pointer;
        }

        .carousel-item img, .carousel-item video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        /* See All Link Button */
        .btn-see-all {
            display: inline-block;
            margin-top: 1.5rem;
            color: #D4AF37;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            padding: 0.6rem 1.2rem;
            border: 1px solid rgba(212, 175, 55, 0.4);
            border-radius: 20px;
            background: rgba(212, 175, 55, 0.05);
            transition: all 0.2s ease;
            cursor: pointer;
        }

        .btn-see-all:hover {
            background: rgba(212, 175, 55, 0.2);
            color: #FFE57F;
        }

        .audio-container { margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1); }
        .audio-label { font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.5rem; display: block; }
        audio { width: 100%; height: 32px; filter: invert(0.9) hue-rotate(180deg); opacity: 0.8; }
        .loading { display: none; margin-top: 1rem; font-size: 0.9rem; color: #FFE57F; }

        /* Full Screen Gallery Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(20px);
            z-index: 100;
            overflow-y: auto;
            padding: 3rem 1.5rem;
        }

        .modal-content {
            max-width: 900px;
            margin: 0 auto;
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            border-bottom: 1px solid rgba(212, 175, 55, 0.3);
            padding-bottom: 1rem;
        }

        .modal-header h2 {
            font-family: 'Cinzel', serif;
            color: #D4AF37;
        }

        .close-btn {
            color: #f8fafc;
            font-size: 2rem;
            cursor: pointer;
            line-height: 1;
        }

        .full-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 1.25rem;
        }

        .full-grid-item {
            aspect-ratio: 1 / 1;
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.15);
            background: rgba(0,0,0,0.4);
        }

        .full-grid-item img, .full-grid-item video {
            width: 100%; height: 100%; object-fit: cover;
        }
    </style>
</head>
<body>

    <div class="gold-banner">
        <h1>Fierce at 50!</h1>
    </div>

    <div class="container">
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

            <!-- Active Scrolling Carousel for Last 5 Uploads -->
            {% if recent_5 %}
            <div class="carousel-container">
                <div class="carousel-title">🔥 Recent Uploads</div>
                <div class="carousel-track">
                    <!-- Duplicated array to create a continuous seamless loop -->
                    {% for item in recent_5 + recent_5 %}
                        <div class="carousel-item" onclick="openAllModal()">
                            {% if item.resource_type == 'video' %}
                                <video src="{{ item.secure_url }}" muted autoplay loop></video>
                            {% else %}
                                <img src="{{ item.secure_url }}" alt="Recent Photo">
                            {% endif %}
                        </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            <!-- Link to View All Uploads -->
            <button type="button" class="btn-see-all" onclick="openAllModal()">🖼️ View All Event Media</button>

            <div class="audio-container">
                <span class="audio-label">🎵 Event Soundtrack</span>
                <audio controls loop preload="auto">
                    <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
                </audio>
            </div>
        </div>
    </div>

    <!-- Modal for Viewing All Photos -->
    <div id="allPhotosModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>All Event Photos & Videos</h2>
                <span class="close-btn" onclick="closeAllModal()">&times;</span>
            </div>
            <div class="full-grid">
                {% for item in all_media %}
                    <div class="full-grid-item">
                        {% if item.resource_type == 'video' %}
                            <video src="{{ item.secure_url }}" controls></video>
                        {% else %}
                            <a href="{{ item.secure_url }}" target="_blank">
                                <img src="{{ item.secure_url }}" alt="Event Media">
                            </a>
                        {% endif %}
                    </div>
                {% else %}
                    <p style="color: #94a3b8;">No photos uploaded yet.</p>
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

        function openAllModal() {
            document.getElementById('allPhotosModal').style.display = 'block';
        }

        function closeAllModal() {
            document.getElementById('allPhotosModal').style.display = 'none';
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    all_media = []
    recent_5 = []
    try:
        # Fetch up to 100 uploads from Cloudinary ordered by newest first
        response = cloudinary.api.resources(
            type="upload",
            prefix="event_uploads/",
            max_results=100,
            direction="desc"
        )
        all_media = response.get("resources", [])
        recent_5 = all_media[:5]  # Select the top 5 most recent
    except Exception as e:
        print("Error fetching media from Cloudinary:", e)

    return render_template_string(HTML_TEMPLATE, recent_5=recent_5, all_media=all_media)

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