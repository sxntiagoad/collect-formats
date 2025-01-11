import os
from flask import current_app, request, send_file, jsonify
from werkzeug.utils import secure_filename
from app.api import bp
from app.services.excel_service import ExcelService

@bp.route('/convert', methods=['POST'])
def convert_excel():
    """
    Endpoint to convert Excel files to PDF
    """
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    
    # If user doesn't select file
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and ExcelService.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Ensure upload directory exists
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Save the uploaded file
        input_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        try:
            # Convert to PDF
            pdf_path = ExcelService.convert_excel_to_pdf(input_path)
            
            # Send the PDF file
            return send_file(
                pdf_path,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=os.path.basename(pdf_path)
            )
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
        finally:
            # Clean up temporary files
            if os.path.exists(input_path):
                os.remove(input_path)
            if 'pdf_path' in locals() and os.path.exists(pdf_path):
                os.remove(pdf_path)
    
    return jsonify({'error': 'Invalid file type'}), 400
