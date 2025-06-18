from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    upload_folder = app.config['UPLOAD_FOLDER']
    plot_folder = app.config['PLOT_FOLDER']
    
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(plot_folder, exist_ok=True)
    
    print(f"Upload folder created at: {os.path.abspath(upload_folder)}")
    print(f"Plot folder created at: {os.path.abspath(plot_folder)}")
    print("Server starting on http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)