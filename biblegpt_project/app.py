from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from biblegpt import get_random_verse, search_verse, generate_bible_style_verse

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/random", methods=['GET'])
def random_verse():
    return jsonify({"verse": get_random_verse()})

@app.route("/api/search", methods=['GET'])
def search():
    keyword = request.args.get("q", default="")
    return jsonify({"verse": search_verse(keyword)})

@app.route("/api/generate", methods=['GET'])
def generate():
    topic = request.args.get("q", default="")
    verse = generate_bible_style_verse(topic)
    return jsonify({"verse": verse})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)