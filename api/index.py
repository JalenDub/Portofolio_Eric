import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
except Exception as e:
    import traceback
    from flask import Flask
    app = Flask(__name__)
    
    error_msg = f"Failed to initialize app: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return f"<pre>{error_msg}</pre>", 500
