import os
import subprocess
from werkzeug.utils import secure_filename

class ExcelService:
    @staticmethod
    def convert_excel_to_pdf(input_excel_path):
        """
        Converts Excel file to PDF using LibreOffice
        """
        output_pdf_path = os.path.join(
            os.path.dirname(input_excel_path),
            secure_filename(os.path.splitext(os.path.basename(input_excel_path))[0] + '.pdf')
        )
        
        try:
            # Usar LibreOffice para convertir a PDF
            subprocess.run([
                'xvfb-run',
                'libreoffice',
                '--headless',
                '--convert-to', 'pdf:calc_pdf_Export',
                '--outdir', os.path.dirname(output_pdf_path),
                input_excel_path
            ], check=True)
            
            return output_pdf_path
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error converting file: {str(e)}")

    @staticmethod
    def allowed_file(filename):
        """Check if the file extension is allowed"""
        ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'ods'}  # Agregado soporte para OpenDocument
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
