import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from DataBase.database import db, init_db
from Routes.transaction_route import transaction_bp
from Routes.category_route import category_bp
from Routes.budget_route import budget_bp
from Routes.analytics_route import analytics_bp


def create_app(test_config=None):
    """
    Application factory for the Flask backend.
    Enables safe importing, test fixtures, and modular routing.
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config)
    if test_config:
        app.config.update(test_config)

    # Enable CORS for local Streamlit frontend communication
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize Database and default categories
    init_db(app)

    # Register Blueprints
    app.register_blueprint(transaction_bp, url_prefix="/api/transactions")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(budget_bp, url_prefix="/api/budgets")
    app.register_blueprint(analytics_bp, url_prefix="/api")

    # Health Check Endpoints
    @app.route("/health", methods=["GET"])
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "Student Expense Tracker & Analyzer API",
            "version": "1.0.0",
            "database": "connected"
        }), 200

    # Global Error Handlers
    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            "success": False,
            "message": "The requested API endpoint was not found.",
            "error": str(e)
        }), 404

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return jsonify({
            "success": False,
            "message": "Internal server error occurred.",
            "error": "A server-side error occurred. Please check server logs."
        }), 500

    return app


# Application instance for WSGI / direct execution
app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV", "development").lower() == "development"
    print(f"[SERVER] Starting Student Expense Tracker Flask API on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=False)
