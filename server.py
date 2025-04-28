# ====================
# IMPORTS
# ====================

from flask import Flask, request
from flask_cors import CORS
from bs4 import BeautifulSoup
from short_link import main


# ===================
# initialization
# ===================

app = Flask(__name__)
CORS(app)

# ===================
# ROUTES
# ===================


@app.route("/upload", methods=["POST"])
def upload():
    """Endpoint to receive HTML content and extract bold text."""

    # Check if the request contains JSON data
    if not request.is_json:
        return {"error": "Invalid input format. JSON expected."}, 400

    # getting the HTML content from the request and parsing it
    data = request.get_json()
    html = data.get("html")

    soup = BeautifulSoup(html, "html.parser")

    # extracting the bold text
    bold_texts = []
    for tag in soup.find_all(["b", "strong"]):
        text = tag.get_text(strip=True)
        if text:  # Check if the text is not empty and not already in the list
            bold_texts.append(text)

    # writing the extracted bold text to a file
    open("output.txt", "w").write("\n".join(bold_texts))

    # Call the main function from short_link.py to process the extracted text
    main()

    # Returning success response
    return {"status": "ok"}, 200


# ===================
# RUNNING THE APP
# ===================

if __name__ == "__main__":
    app.run(port=5000)
