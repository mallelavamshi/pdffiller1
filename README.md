# PDF Form Filler API 📝

A production-ready FastAPI application that automatically fills PDF forms with data from Excel files. Includes complete CI/CD pipeline with Docker, GitHub, and Jenkins.

![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python)

## 🚀 Features

- ✅ **Automatic PDF Form Filling** - Upload Excel, get filled PDF
- ✅ **RESTful API** - Easy integration with any application
- ✅ **Docker Support** - Containerized deployment
- ✅ **CI/CD Pipeline** - Automated deployment with Jenkins
- ✅ **Health Monitoring** - Built-in health check endpoints
- ✅ **Auto Cleanup** - Automatic file management
- ✅ **API Documentation** - Interactive Swagger UI

## 📋 Requirements

- Python 3.11+
- Docker & Docker Compose
- Ubuntu Server (for deployment)
- Jenkins (for CI/CD)

## 🏗️ Project Structure

```
pdf-filler-api/
├── main.py                 # FastAPI application
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── Jenkinsfile            # CI/CD pipeline
├── requirements.txt       # Python dependencies
├── DEPLOYMENT_GUIDE.md    # Complete deployment guide
└── templates/             # PDF templates directory
    └── Letter_of_Representation_Fillable.pdf
```

## 🔧 Quick Start

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/pdf-filler-api.git
cd pdf-filler-api
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Add PDF template:**
```bash
mkdir -p templates
cp Letter_of_Representation_Fillable.pdf templates/
```

5. **Run application:**
```bash
uvicorn main:app --reload
```

6. **Access API:**
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Docker Deployment

1. **Build and run with Docker Compose:**
```bash
docker-compose up -d
```

2. **Check logs:**
```bash
docker-compose logs -f
```

3. **Stop application:**
```bash
docker-compose down
```

## 📡 API Endpoints

### `GET /`
Health check endpoint
```bash
curl http://localhost:8000/
```

### `GET /health`
Detailed health status
```bash
curl http://localhost:8000/health
```

### `POST /fill-pdf`
Upload Excel file and receive filled PDF
```bash
curl -X POST "http://localhost:8000/fill-pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_data.xlsx" \
  --output filled_pdf.pdf
```

### `DELETE /cleanup`
Clean up old temporary files
```bash
curl -X DELETE http://localhost:8000/cleanup
```

## 📊 Excel File Format

Your Excel file should contain these columns:

| Column | Description | Example |
|--------|-------------|---------|
| date | Document date | November 14, 2025 |
| recipient_name | Recipient's name | Honorable Judge Sarah Mitchell |
| recipient_address | Recipient's address | Denton County Criminal Court... |
| case_number | Case number | F-2025-12345-C |
| client_name | Client's full name | Robert James Anderson |
| client_name_inline | Client name (inline) | Robert James Anderson |
| attorney_name | Attorney's name | Michael T. Harrison |
| bar_number | Bar number | 24567890 |
| law_firm | Law firm name | Harrison & Associates Law Firm |
| attorney_address | Attorney's address | 2301 S Stemmons Fwy... |
| phone | Phone number | (940) 555-1234 |
| email | Email address | mharrison@harrisonlawfirm.com |

## 🚢 Production Deployment

For complete deployment instructions including:
- Ubuntu server setup
- Docker configuration
- Jenkins CI/CD pipeline
- GitHub integration
- SSL/HTTPS setup
- Monitoring & maintenance

**See:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 🔐 Environment Variables

Create a `.env` file for configuration (optional):

```env
# Application
APP_NAME=pdf-filler-api
APP_VERSION=1.0.0

# Server
HOST=0.0.0.0
PORT=8000

# Paths
TEMPLATE_DIR=templates
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
```

## 🧪 Testing

### Test with cURL:
```bash
# Health check
curl http://localhost:8000/health

# Upload and fill PDF
curl -X POST "http://localhost:8000/fill-pdf" \
  -F "file=@Letter_of_Representation_Sample_Data.xlsx" \
  -o filled_output.pdf
```

### Test with Python:
```python
import requests

# Upload file
url = "http://localhost:8000/fill-pdf"
files = {"file": open("Letter_of_Representation_Sample_Data.xlsx", "rb")}
response = requests.post(url, files=files)

# Save filled PDF
with open("filled_output.pdf", "wb") as f:
    f.write(response.content)
```

### Test with JavaScript:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/fill-pdf', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'filled_pdf.pdf';
    a.click();
});
```

## 🐛 Troubleshooting

### Issue: "PDF template not found"
```bash
# Ensure template exists
ls -la templates/Letter_of_Representation_Fillable.pdf

# Copy template if missing
cp Letter_of_Representation_Fillable.pdf templates/
```

### Issue: "Invalid file type"
- Only `.xlsx` and `.xls` files are accepted
- Ensure your file has the correct extension

### Issue: Port already in use
```bash
# Change port in docker-compose.yml or use different port
docker-compose down
# Edit docker-compose.yml to use different port
docker-compose up -d
```

## 📈 Performance

- Average processing time: < 2 seconds
- Supports concurrent requests
- Automatic cleanup of temporary files
- Docker health checks every 30 seconds

## 🔒 Security Considerations

1. **File Validation**: Only Excel files accepted
2. **Temporary Files**: Automatically cleaned up
3. **CORS**: Configured for production use
4. **Docker**: Isolated container environment
5. **Health Checks**: Monitor application status

## 🛠️ Development

### Project Dependencies:
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pandas**: Excel file processing
- **PyPDF2**: PDF manipulation
- **python-multipart**: File upload handling

### Adding Features:

1. **Batch Processing**: Process multiple rows
2. **Authentication**: Add API key validation
3. **Database**: Store processing history
4. **Webhooks**: Notify when processing complete

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **API Docs**: http://YOUR_SERVER:8000/docs

## 🎯 Roadmap

- [ ] Batch processing support
- [ ] Multiple PDF templates
- [ ] API authentication
- [ ] Processing history dashboard
- [ ] Email notifications
- [ ] S3/Cloud storage integration

## 👏 Acknowledgments

- FastAPI framework
- Docker community
- Jenkins project

---

**Made with ❤️ using FastAPI**

*Last Updated: November 2025*
