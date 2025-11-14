from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import os
import uuid
from datetime import datetime
import shutil
from pathlib import Path

app = FastAPI(
    title="PDF Form Filler API",
    description="Upload Excel file to automatically fill PDF form",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
TEMPLATE_DIR = Path("templates")

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
TEMPLATE_DIR.mkdir(exist_ok=True)

# PDF template path
PDF_TEMPLATE = TEMPLATE_DIR / "Letter_of_Representation_Fillable.pdf"

def fill_pdf_form(excel_path: str, pdf_template: str, output_path: str):
    """
    Fill PDF form with data from Excel file.
    """
    try:
        # Read Excel data
        df = pd.read_excel(excel_path)

        if df.empty:
            raise ValueError("Excel file is empty")

        # Get first row of data
        data = df.iloc[0].to_dict()

        # Read PDF template
        reader = PdfReader(pdf_template)
        writer = PdfWriter()

        # Map Excel columns to PDF form fields
        field_mapping = {
            'date': str(data.get('date', '')),
            'recipient_name': str(data.get('recipient_name', '')),
            'recipient_address': str(data.get('recipient_address', '')),
            'case_number': str(data.get('case_number', '')),
            'client_name': str(data.get('client_name', '')),
            'client_name_inline': str(data.get('client_name_inline', '')),
            'attorney_name': str(data.get('attorney_name', '')),
            'bar_number': str(data.get('bar_number', '')),
            'law_firm': str(data.get('law_firm', '')),
            'attorney_address': str(data.get('attorney_address', '')),
            'phone': str(data.get('phone', '')),
            'email': str(data.get('email', ''))
        }

        # Append all pages and update form fields
        writer.append(reader)

        if reader.get_fields() is not None:
            writer.update_page_form_field_values(
                writer.pages[0],
                field_mapping
            )

        # Write filled PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        return True

    except Exception as e:
        raise Exception(f"Error filling PDF: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint"""
    port = os.getenv("PORT", "8003")
    return {
        "status": "healthy",
        "message": "PDF Form Filler API is running",
        "version": "1.0.0",
        "port": port
    }

@app.get("/health")
async def health_check():
    """Health check for monitoring"""
    template_exists = PDF_TEMPLATE.exists()
    return {
        "status": "healthy" if template_exists else "unhealthy",
        "template_available": template_exists,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/fill-pdf")
async def fill_pdf(file: UploadFile = File(...)):
    """
    Upload Excel file and receive filled PDF

    Args:
        file: Excel file (.xlsx) containing form data

    Returns:
        Filled PDF file
    """

    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an Excel file (.xlsx or .xls)"
        )

    # Check if template exists
    if not PDF_TEMPLATE.exists():
        raise HTTPException(
            status_code=500,
            detail="PDF template not found. Please ensure Letter_of_Representation_Fillable.pdf is in the templates directory."
        )

    # Generate unique IDs for files
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save uploaded Excel file
    excel_filename = f"{unique_id}_{file.filename}"
    excel_path = UPLOAD_DIR / excel_filename

    try:
        with open(excel_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Generate output PDF filename
        output_filename = f"filled_pdf_{timestamp}_{unique_id}.pdf"
        output_path = OUTPUT_DIR / output_filename

        # Fill the PDF
        fill_pdf_form(
            str(excel_path),
            str(PDF_TEMPLATE),
            str(output_path)
        )

        # Clean up uploaded Excel file
        excel_path.unlink()

        # Return the filled PDF
        return FileResponse(
            path=output_path,
            media_type='application/pdf',
            filename=f"Letter_of_Representation_Filled_{timestamp}.pdf",
            headers={
                "Content-Disposition": f"attachment; filename=Letter_of_Representation_Filled_{timestamp}.pdf"
            }
        )

    except Exception as e:
        # Clean up files on error
        if excel_path.exists():
            excel_path.unlink()
        if 'output_path' in locals() and output_path.exists():
            output_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )

@app.post("/fill-pdf-batch")
async def fill_pdf_batch(file: UploadFile = File(...)):
    """
    Process Excel file with multiple rows and generate multiple PDFs (future enhancement)
    """
    raise HTTPException(
        status_code=501,
        detail="Batch processing not yet implemented"
    )

@app.delete("/cleanup")
async def cleanup_old_files():
    """
    Clean up old files from uploads and outputs directories
    """
    try:
        deleted_count = 0

        # Clean uploads
        for file in UPLOAD_DIR.iterdir():
            if file.is_file():
                file.unlink()
                deleted_count += 1

        # Clean outputs older than 1 hour
        current_time = datetime.now().timestamp()
        for file in OUTPUT_DIR.iterdir():
            if file.is_file():
                file_age = current_time - file.stat().st_mtime
                if file_age > 3600:  # 1 hour
                    file.unlink()
                    deleted_count += 1

        return {
            "status": "success",
            "files_deleted": deleted_count
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during cleanup: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8003"))
    uvicorn.run(app, host="0.0.0.0", port=port)
