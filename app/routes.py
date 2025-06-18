from flask import Blueprint, request, jsonify, send_file, current_app
from . import db
from .models import UploadedFile, AnalysisResult
from .utils import allowed_file, process_file, clean_data, generate_stats, generate_plot
import os
import pandas as pd
import uuid
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type"}), 415
    
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{file.filename}"
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        new_file = UploadedFile(
            filename=file.filename,
            filepath=filepath,
            uploaded_at=datetime.utcnow()
        )
        db.session.add(new_file)
        db.session.commit()
        
        df = process_file(filepath)
        if df.empty:
            return jsonify({"error": "Empty or invalid file"}), 400
            
        return jsonify({
            "message": "File uploaded successfully",
            "file_id": new_file.id
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/data/stats', methods=['GET'])
def get_stats():
    file_id = request.args.get('file_id')
    if not file_id:
        return jsonify({"error": "Missing file_id parameter"}), 400
    
    try:
        file = UploadedFile.query.get(file_id)
        if not file:
            return jsonify({"error": "File not found"}), 404
        
        existing_analysis = AnalysisResult.query.filter_by(
            file_id=file_id, 
            analysis_type='stats'
        ).first()
        
        if existing_analysis:
            return jsonify(existing_analysis.result)
        
        df = process_file(file.filepath)
        stats = generate_stats(df)
        
        new_analysis = AnalysisResult(
            file_id=file_id,
            analysis_type='stats',
            result=stats
        )
        db.session.add(new_analysis)
        db.session.commit()
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/data/clean', methods=['GET'])
def clean_data_endpoint():
    file_id = request.args.get('file_id')
    if not file_id:
        return jsonify({"error": "Missing file_id parameter"}), 400
    
    try:
        file = UploadedFile.query.get(file_id)
        if not file:
            return jsonify({"error": "File not found"}), 404
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        df = process_file(file.filepath)
        cleaned_df = clean_data(df)
        
        new_filename = f"cleaned_{file.filename}"
        new_filepath = os.path.join(upload_folder, new_filename)
        
        if file.filepath.endswith('.csv'):
            cleaned_df.to_csv(new_filepath, index=False)
        else:
            cleaned_df.to_excel(new_filepath, index=False)
        
        file.cleaned = True
        db.session.commit()
        
        return jsonify({
            "message": "Data cleaned successfully",
            "cleaned_file_path": new_filepath
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/data/plot', methods=['GET'])
def get_plot():
    file_id = request.args.get('file_id')
    column = request.args.get('column')
    
    if not file_id or not column:
        return jsonify({"error": "Missing parameters"}), 400
    
    try:
        file = UploadedFile.query.get(file_id)
        if not file:
            return jsonify({"error": "File not found"}), 404
        
        existing_analysis = AnalysisResult.query.filter_by(
            file_id=file_id, 
            analysis_type='plot'
        ).first()
        
        if existing_analysis and existing_analysis.result.get('column') == column:
            plot_path = existing_analysis.result.get('plot_path')
            if os.path.exists(plot_path):
                return send_file(plot_path, mimetype='image/png')
        
        plot_folder = current_app.config['PLOT_FOLDER']
        os.makedirs(plot_folder, exist_ok=True)
        
        df = process_file(file.filepath)
        plot_path = generate_plot(df, column, plot_folder)
        
        new_analysis = AnalysisResult(
            file_id=file_id,
            analysis_type='plot',
            result={
                "column": column,
                "plot_path": plot_path
            }
        )
        db.session.add(new_analysis)
        db.session.commit()
        
        return send_file(plot_path, mimetype='image/png')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500