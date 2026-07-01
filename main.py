import os
import sys
import io
from app import create_app

# Fix encoding for Windows terminal
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if __name__ == "__main__":
    # Set the environment
    os.environ.setdefault('FLASK_ENV', 'development')
    
    app = create_app('development')
    
    print("\n" + "="*50)
    print("[*] Starting Appointments API")
    print("="*50)
    print("Server running at: http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET    /api/clients")
    print("  POST   /api/clients")
    print("  GET    /api/clients/<id>")
    print("  PUT    /api/clients/<id>")
    print("  DELETE /api/clients/<id>")
    print("\n  GET    /api/services")
    print("  POST   /api/services")
    print("  GET    /api/services/<id>")
    print("  PUT    /api/services/<id>")
    print("  DELETE /api/services/<id>")
    print("\n  GET    /api/appointments")
    print("  POST   /api/appointments")
    print("  GET    /api/appointments/<id>")
    print("  PUT    /api/appointments/<id>")
    print("  DELETE /api/appointments/<id>")
    print("="*50 + "\n")
    
    app.run(host="0.0.0.0", port=5000, debug=True)