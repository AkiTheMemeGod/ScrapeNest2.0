from flask import Flask, request, jsonify, Response, render_template
import httpx

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route("/scrape", methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    try:
        if not (url.startswith("http://") or url.startswith("https://")):
            raise ValueError("URL must start with 'http://' or 'https://'")

        response = httpx.get(url)
        response.raise_for_status()

        return Response(response.text, content_type='text/html')

    except httpx.RequestError as e:
        return jsonify({"error": f"Request error: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=False)