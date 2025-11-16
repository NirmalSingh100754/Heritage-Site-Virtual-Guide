# 🏛️ Heritage Virtual Guide

A comprehensive web application that uses AI-powered image recognition and natural language processing to provide detailed information about heritage sites and monuments around the world. Upload an image or search by name to discover fascinating historical details, architectural information, and visitor guides.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-red.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Usage Guide](#-usage-guide)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🔍 **Search Heritage Sites**
- Search by monument name or location
- Get comprehensive historical information
- Learn about architectural styles and significance
- Discover visitor information and travel tips

### 🖼️ **Image Analysis**
- Upload images of heritage sites
- AI-powered image recognition identifies the monument
- Detailed analysis including:
  - Historical period and builder
  - Architectural style
  - Cultural significance
  - Current status (UNESCO, conservation)
  - Interesting facts
  - Nearby attractions
  - Best time to visit

### 🌟 **Featured Sites**
- Browse curated list of famous heritage sites
- Get recommendations for exploration
- Beautiful card-based UI

### 👤 **User Authentication**
- Secure login and signup system
- User session management
- Chat history tracking
- MongoDB integration for user data

### 🎨 **Modern UI/UX**
- Dark theme with elegant styling
- Responsive design
- Smooth animations and transitions
- Progress indicators for AI processing

---

## 🛠️ Tech Stack

### **Backend**
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **OpenRouter AI** - Unified API for multiple AI models (GPT-4, Claude, Gemini)
- **MongoDB** - NoSQL database for user data and sessions
- **Pillow (PIL)** - Image processing library
- **Pydantic** - Data validation using Python type annotations
- **Python-dotenv** - Environment variable management

### **Frontend**
- **Streamlit** - Rapid web app development framework
- **Requests** - HTTP library for API calls
- **Pymongo** - MongoDB driver for Python

### **AI Models Supported**
- OpenAI GPT-4o, GPT-4 Turbo, GPT-4 Vision
- Anthropic Claude 3 (Opus, Sonnet, Haiku)
- Google Gemini Pro Vision

---

## 📁 Project Structure

```
Heritage-Site-Virtual-Guide/
│
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── core/               # Core configuration
│   │   │   └── config.py       # Settings and environment variables
│   │   ├── models/             # Pydantic models
│   │   │   └── heritage.py     # Heritage site data models
│   │   ├── routers/            # API routes
│   │   │   └── heritage.py     # Heritage endpoints
│   │   ├── services/           # Business logic
│   │   │   ├── ai_service.py   # AI integration (OpenRouter)
│   │   │   └── database.py     # MongoDB connection
│   │   └── main.py             # FastAPI application entry point
│   └── requirements.txt        # Backend dependencies
│
├── frontend/                   # Streamlit frontend application
│   ├── components/             # Reusable UI components
│   │   ├── featured_cards.py  # Heritage site cards
│   │   ├── image_upload.py    # Image upload component
│   │   └── search_component.py # Search functionality
│   ├── utils/                  # Utility functions
│   │   ├── api_client.py      # Backend API client
│   │   └── session_state.py    # Session management
│   └── app.py                  # Main Streamlit application
│
├── requirements.txt            # Frontend dependencies
├── README.md                   # This file
└── CHANGES_SUMMARY.md          # Recent changes documentation
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- MongoDB Atlas account (or local MongoDB)
- OpenRouter API key ([Get one here](https://openrouter.ai/))

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Heritage-Site-Virtual-Guide
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Install Frontend Dependencies

```bash
cd ../frontend
pip install -r ../requirements.txt
```

---

## ⚙️ Configuration

### Backend Configuration

Create a `.env` file in the `backend/` directory:

```env
# MongoDB Configuration
MONGODB_USERNAME=your_mongodb_username
MONGODB_PASSWORD=your_mongodb_password
MONGODB_CLUSTER=your_cluster_name.mongodb.net
MONGODB_DATABASE=heritage_db

# OpenRouter AI Configuration
OPENROUTER_KEY=your_openrouter_api_key
```

### Frontend Configuration

The frontend automatically loads environment variables. You can also create a `.env` file in the root directory if needed.

### Getting API Keys

1. **OpenRouter API Key:**
   - Visit [OpenRouter.ai](https://openrouter.ai/)
   - Sign up for an account
   - Navigate to Keys section
   - Create a new API key
   - Copy and paste into `.env` file

2. **MongoDB Atlas:**
   - Visit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a free cluster
   - Create a database user
   - Get connection string
   - Extract username, password, and cluster name

---

## 🏃 Running the Application

### Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`
- Config Check: `http://localhost:8000/api/heritage/config-check`

### Start Frontend Application

Open a new terminal and run:

```bash
cd frontend
streamlit run app.py
```

The application will open at: `http://localhost:8501`

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### 1. **Search Heritage Site**
```http
POST /heritage/search
Content-Type: application/json

{
  "query": "Taj Mahal"
}
```

**Response:**
```json
{
  "success": true,
  "result": "Name: Taj Mahal\nLocation: Agra, India\n..."
}
```

#### 2. **Upload and Analyze Image**
```http
POST /heritage/upload-image
Content-Type: multipart/form-data

file: [image file]
```

**Response:**
```json
{
  "success": true,
  "result": "Name: [Monument Name]\nLocation: [Location]\n..."
}
```

#### 3. **Get Recommendations**
```http
GET /heritage/recommendations
```

**Response:**
```json
{
  "sites": [
    {
      "name": "Taj Mahal",
      "location": "Agra, India",
      "description": "...",
      "image_url": "/assets/images/taj-mahal.jpg"
    }
  ]
}
```

#### 4. **Health Check**
```http
GET /health
```

#### 5. **Config Check**
```http
GET /heritage/config-check
```

---

## 📖 Usage Guide

### For Users

1. **Login/Signup**
   - Create an account or login with existing credentials
   - Your session will be saved

2. **Search Heritage Sites**
   - Go to the "🔍 Search" tab
   - Enter the name of a heritage site
   - Get instant comprehensive information

3. **Upload Image**
   - Go to the "🖼️ Upload Image" tab
   - Upload a clear image of a heritage site
   - Click "Analyze Heritage"
   - Wait for AI analysis (10-20 seconds)
   - View detailed monument information

4. **Browse Featured Sites**
   - Check the "🏠 Home" tab
   - Browse recommended heritage sites
   - Click on cards to learn more

### For Developers

#### Adding New Features

1. **Backend:**
   - Add new routes in `backend/app/routers/`
   - Add business logic in `backend/app/services/`
   - Update models in `backend/app/models/`

2. **Frontend:**
   - Create components in `frontend/components/`
   - Update main app in `frontend/app.py`
   - Add utilities in `frontend/utils/`

#### Testing API

Use the interactive API docs at `http://localhost:8000/docs` or use curl:

```bash
# Test search
curl -X POST "http://localhost:8000/api/heritage/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Colosseum"}'

# Test config
curl "http://localhost:8000/api/heritage/config-check"
```

---

## 🖼️ Screenshots

### Home Page
- Beautiful dark theme interface
- Featured heritage sites cards
- Statistics dashboard

### Search Functionality
- Real-time heritage site search
- Comprehensive information display
- Formatted historical data

### Image Analysis
- Image upload interface
- AI-powered monument recognition
- Detailed analysis results

---

## 🔧 Troubleshooting

### Common Issues

1. **"API key is not configured"**
   - Check if `.env` file exists in `backend/` directory
   - Verify `OPENROUTER_KEY` is set correctly
   - Restart the backend server after adding the key

2. **"Cannot connect to backend server"**
   - Ensure backend is running on port 8000
   - Check if port 8000 is available: `lsof -ti:8000`
   - Kill existing process if needed: `kill -9 <PID>`

3. **"MongoDB connection failed"**
   - Verify MongoDB credentials in `.env`
   - Check if MongoDB Atlas IP whitelist includes your IP
   - Ensure cluster is running

4. **Image analysis fails**
   - Check backend logs for detailed error messages
   - Verify API key has sufficient credits
   - Try a different, clearer image
   - Check `/api/heritage/config-check` endpoint

### Debug Mode

Enable detailed logging by checking backend terminal output. The application logs:
- 🔄 Processing status
- ✅ Success messages
- ❌ Error details
- ⚠️ Warnings

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Update documentation for new features

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **OpenRouter** - For providing unified AI model access
- **FastAPI** - For the excellent web framework
- **Streamlit** - For rapid UI development
- **MongoDB** - For database services
- All the AI model providers (OpenAI, Anthropic, Google)

---

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

## 🎯 Future Enhancements

- [ ] Video analysis support
- [ ] Multi-language support
- [ ] User favorites and bookmarks
- [ ] Social sharing features
- [ ] AR/VR integration
- [ ] Mobile app version
- [ ] Advanced search filters
- [ ] Historical timeline visualization
- [ ] User reviews and ratings
- [ ] Travel planning features

---

**Made with ❤️ for heritage enthusiasts and history lovers**
