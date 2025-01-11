import os
import win32com.client
from werkzeug.utils import secure_filename

class ExcelService:
    @staticmethod
    def convert_excel_to_pdf(input_excel_path):
        """
        Converts Excel file to PDF
        """
        output_pdf_path = os.path.join(
            os.path.dirname(input_excel_path),
            secure_filename(os.path.splitext(os.path.basename(input_excel_path))[0] + '.pdf')
        )
        
        # Configurar Excel usando win32com
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        
        try:
            # Abrir el archivo Excel
            wb = excel.Workbooks.Open(input_excel_path)
            ws = wb.ActiveSheet
            
            # Configurar área de impresión y ajustes
            ws.PageSetup.Zoom = False
            ws.PageSetup.FitToPagesWide = 1
            ws.PageSetup.FitToPagesTall = False
            ws.PageSetup.PrintArea = "A1:U85"
            ws.PageSetup.Orientation = 1  # xlPortrait
            ws.PageSetup.CenterHorizontally = True
            
            # Configurar márgenes (en puntos)
            ws.PageSetup.LeftMargin = excel.InchesToPoints(0.7)
            ws.PageSetup.RightMargin = excel.InchesToPoints(0.7)
            ws.PageSetup.TopMargin = excel.InchesToPoints(0.75)
            ws.PageSetup.BottomMargin = excel.InchesToPoints(0.75)
            
            # Exportar a PDF
            wb.ExportAsFixedFormat(0, output_pdf_path)
            
            return output_pdf_path
            
        finally:
            # Cerrar Excel
            wb.Close(False)
            excel.Quit()

    @staticmethod
    def allowed_file(filename):
        """Check if the file extension is allowed"""
        ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
