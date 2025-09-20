from flask import Flask, render_template, request, redirect, flash
import requests
import os

# -----------------------------
# Flask app (frontend)
# -----------------------------
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")  # Secure via env var in production

# API configs (set in Render dashboard)
MODEL_API_URL = os.getenv("MODEL_API_URL", "http://10.212.239.250:8000/api/process_claim")
WEBGIS_API_URL = os.getenv("WEBGIS_API_URL", "http://10.212.239.250:5001/api/claims")
MODEL_API_KEY = os.getenv("MODEL_API_KEY", "YOUR_SECRET_API_KEY_HERE")
WEBGIS_API_KEY = os.getenv("WEBGIS_API_KEY", "SIH2025_SECRET_123")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            flash("No file uploaded", "error")
            return render_template("index.html", result=result)

        # Validate file size
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)
        if size == 0 or size > 200 * 1024:
            flash("File size must be between 1KB and 200KB", "error")
            return render_template("index.html", result=result)

        try:
            # Step 1: Send file to Model API
            files = {"file": (file.filename, file.read(), file.content_type)}
            headers = {"x-api-key": MODEL_API_KEY}
            response = requests.post(MODEL_API_URL, headers=headers, files=files, timeout=30)

            if response.status_code != 200:
                flash(f"Model API request failed: {response.text}", "error")
                return render_template("index.html", result=result)

            result = response.json()

            # Step 2: Forward AI result to Map API
            try:
                map_response = requests.post(
                    WEBGIS_API_URL,
                    headers={"x-api-key": WEBGIS_API_KEY, "Content-Type": "application/json"},
                    json=result.get("result"),
                    timeout=30
                )
                if map_response.status_code != 200:
                    flash(f"Map API request failed: {map_response.text}", "error")
                else:
                    print("Map API response:", map_response.json())
            except Exception as e:
                flash(f"Failed to send to Map API: {str(e)}", "error")

            # Step 3: Redirect to Map UI
            return redirect("http://10.212.239.250:5001/")

        except requests.exceptions.RequestException as e:
            flash(f"Failed to connect to Model API: {str(e)}", "error")

    return render_template("index.html", result=result)

# -----------------------------
# Run Flask frontend
# -----------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Render provides $PORT
    app.run(host="0.0.0.0", port=port, debug=False)


