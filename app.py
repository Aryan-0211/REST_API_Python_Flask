from flask import Flask
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

app = Flask(__name__)

# Application configuration
app.config["PROPAGATE_EXCEPTIONS"] = True  
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"  # Prefix for OpenAPI docs
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"  # Swagger UI path
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Initialize the API
api = Api(app)

# Register blueprints
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)

# Application entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
