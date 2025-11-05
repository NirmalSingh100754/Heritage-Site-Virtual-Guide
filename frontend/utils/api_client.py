import requests
import json
from typing import Optional
import streamlit as st

class HeritageAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_prefix = "/api"
        
    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[dict] = None, files: Optional[dict] = None) -> Optional[dict]:
        """Generic method to make API requests with enhanced error handling"""
        url = f"{self.base_url}{self.api_prefix}{endpoint}"
        
        try:
            headers = {"Content-Type": "application/json"}
            
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                if files:
                    # For file uploads, don't use JSON headers
                    headers = {}  # Remove JSON headers for file uploads
                    response = requests.post(url, files=files, data=data, timeout=30)
                else:
                    # For JSON data, use json parameter
                    response = requests.post(url, json=data, headers=headers, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError:
            st.error("🚫 Cannot connect to backend server. Please make sure:")
            st.info("1. Backend server is running on http://localhost:8000")
            st.info("2. No firewall is blocking the connection")
            st.info("3. Both servers are in the same network")
            return None
            
        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out. The AI service might be slow. Please try again.")
            return None
            
        except requests.exceptions.HTTPError as e:
            error_detail = ""
            try:
                error_response = e.response.json()
                error_detail = error_response.get('detail', e.response.text)
                if 'error' in error_response:
                    error_detail = error_response['error']
            except:
                error_detail = e.response.text
                
            if e.response.status_code == 422:
                st.error("❌ Invalid request format. Please check your input.")
            elif e.response.status_code == 429:
                st.error("🚦 Too many requests. Please wait a moment and try again.")
            elif e.response.status_code == 500:
                st.error("🔧 Server error. Our team has been notified.")
            else:
                st.error(f"❌ HTTP Error {e.response.status_code}: {error_detail}")
            return None
            
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Network error: {str(e)}")
            return None
            
        except Exception as e:
            st.error(f"💥 Unexpected error: {str(e)}")
            return None
    
    def analyze_image(self, image_bytes: bytes, user_id: Optional[str] = None) -> Optional[str]:
        """Analyze heritage image with progress tracking"""
        endpoint = "/heritage/upload-image"
        files = {"file": ("heritage_image.jpg", image_bytes, "image/jpeg")}
        data = {"user_id": user_id} if user_id else {}
        
        # Show progress for image analysis (can take longer)
        with st.spinner("🔄 AI is analyzing your image. This may take 10-20 seconds..."):
            response = self._make_request(endpoint, "POST", data=data, files=files)
        
        return response.get("result") if response and response.get("success") else None
    
    def analyze_text(self, query: str, user_id: Optional[str] = None) -> Optional[str]:
        """Analyze heritage text query with progress tracking"""
        endpoint = "/heritage/search"
        
        data = {"query": query}
            
        with st.spinner("🔍 Searching heritage database..."):
            response = self._make_request(endpoint, "POST", data=data)
        
        return response.get("result") if response and response.get("success") else None
    
    def get_recommendations(self) -> Optional[list]:
        """Get heritage recommendations"""
        endpoint = "/heritage/recommendations"
        response = self._make_request(endpoint, "GET")
        return response.get("sites") if response else None
    
    def test_connection(self) -> bool:
        """Test backend connection"""
        endpoint = "/heritage/test"
        response = self._make_request(endpoint, "GET")
        return response is not None and response.get("status") == "success"
    
    def health_check(self) -> bool:
        """Check if backend is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False

# Global API client instance
api_client = HeritageAPIClient()