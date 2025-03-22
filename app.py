from flask import Flask, request, jsonify, Response, render_template
import httpx

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route("/scrape", methods=['GET'])
def scrape():
    url = request.args.get('url')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        if not (url.startswith("http://") or url.startswith("https://")):
            raise ValueError("URL must start with 'http://' or 'https://'")

        response = httpx.get(url, headers=headers)
        response.raise_for_status()

        return Response(response.text, content_type='text/html')

    except httpx.RequestError as e:
        return jsonify({"error": f"Request error: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=False)