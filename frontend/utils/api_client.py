import requests
import json
from typing import Optional
import streamlit as st

class HeritageAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_prefix = "/api"
        
    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[dict] = None, files: Optional[dict] = None) -> Optional[dict]:
        """Generic method to make API requests"""
        url = f"{self.base_url}{self.api_prefix}{endpoint}"
        
        try:
            headers = {"Content-Type": "application/json"}
            
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                if files:
                    # For file uploads, don't use JSON headers
                    response = requests.post(url, files=files, data=data)
                else:
                    # For JSON data, use json parameter
                    response = requests.post(url, json=data, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError:
            st.error("🚫 Cannot connect to backend server. Make sure the FastAPI server is running on http://localhost:8000")
            return None
        except requests.exceptions.HTTPError as e:
            error_detail = ""
            try:
                error_response = e.response.json()
                error_detail = error_response.get('detail', e.response.text)
            except:
                error_detail = e.response.text
                
            st.error(f"❌ HTTP Error {e.response.status_code}: {error_detail}")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"❌ API request failed: {str(e)}")
            return None
        except Exception as e:
            st.error(f"💥 Unexpected error: {str(e)}")
            return None
    
    def analyze_image(self, image_bytes: bytes, user_id: Optional[str] = None) -> Optional[str]:
        """Analyze heritage image"""
        endpoint = "/heritage/upload-image"
        files = {"file": ("heritage_image.jpg", image_bytes, "image/jpeg")}
        data = {"user_id": user_id} if user_id else {}
        
        response = self._make_request(endpoint, "POST", data=data, files=files)
        return response.get("result") if response and response.get("success") else None
    
    def analyze_text(self, query: str, user_id: Optional[str] = None) -> Optional[str]:
        """Analyze heritage text query - FIXED VERSION"""
        endpoint = "/heritage/search"
        
        # Simple JSON data
        data = {
            "query": query
        }
            
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