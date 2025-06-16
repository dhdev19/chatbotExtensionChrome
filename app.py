from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Set your Gemini API key (ideally load from env variable)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini 2.0 Flash model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_query = data.get("user_query", "")
    page_content = data.get("page_content", "")

    prompt = f"""
You are a helpful assistant. The user is browsing a webpage. Here is the page content:

\"\"\"{page_content[:15000]}\"\"\"  # Truncate for context limits

The user asked:
\"\"\"{user_query}\"\"\"

Provide a helpful response based on the page.
"""

    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG"))
