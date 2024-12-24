from flask import Flask

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]

@app.route("/store", methods=["GET"])
def get_store():
    return {"stores": stores}  # Visit http://127.0.0.1:5001/store

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Use a different port