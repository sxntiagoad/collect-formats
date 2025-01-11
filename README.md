# Excel to PDF Converter API

This API service converts Excel files to PDF format using Flask and Windows COM automation.

## Features

- Excel to PDF conversion via REST API
- Secure file handling
- Configurable page setup and margins
- GitHub Actions integration for CI/CD

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:
```
SECRET_KEY=your-secret-key
```

4. Run the application:
```bash
python run.py
```

## API Usage

### Convert Excel to PDF

**Endpoint:** `POST /api/convert`

**Request:**
- Content-Type: multipart/form-data
- Body: file (Excel file .xlsx or .xls)

**Response:**
- PDF file download
- Error message in case of failure

## Deployment

The application is configured to deploy automatically via GitHub Actions to Azure Web Apps when pushing to the main branch.

To set up deployment:

1. Create an Azure Web App
2. Add the following secrets to your GitHub repository:
   - `AZURE_WEBAPP_NAME`: Your Azure Web App name
   - `AZURE_WEBAPP_PUBLISH_PROFILE`: Your Azure publish profile

## Development

The project follows a clean architecture pattern:
- `app/`: Main application package
  - `api/`: API routes and endpoints
  - `services/`: Business logic and services
- `config.py`: Application configuration
- `run.py`: Application entry point
