# Video/Photo Upload Microservice

## API Endpoints

### Upload File

- **URL**: `/upload`
- **Method**: `POST`
- **Request**:
  - Headers: `Content-Type: multipart/form-data`
  - Body: `file` (required, file to upload)
- **Response**:
  - 200: `{"message": "File uploaded successfully"}`
  - 400: `{"error": "Error message"}`

### Get Parental Consent

- **URL**: `/consent`
- **Method**: `POST`
- **Request**:
  - Headers: `Content-Type: application/json`
  - Body: `{"parental_consent": "consent_text"}`
- **Response**:
  - 200: `{"message": "Consent recorded successfully"}`
  - 400: `{"error": "Error message"}`

## Security Measures

- Files are encrypted before uploading to Google Cloud Storage.
- Parental consent records are securely stored in a PostgreSQL database.

## Deployment Instructions

- Step-by-step deployment instructions on Google Cloud Platform (see below).

## Testing

- Instructions for running unit tests (coming soon).
