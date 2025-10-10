import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # MongoDB Configuration
    MONGODB_USERNAME: str = os.getenv("MONGODB_USERNAME")
    MONGODB_PASSWORD: str = os.getenv("MONGODB_PASSWORD")
    MONGODB_CLUSTER: str = os.getenv("MONGODB_CLUSTER")
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "heritage_db")
    
    # AI Configuration - Using OpenRouter instead of Gemini
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_KEY")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # App Configuration
    PROJECT_NAME: str = "Heritage Virtual Guide API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    @property
    def MONGODB_URI(self):
        from urllib.parse import quote_plus
        username = quote_plus(self.MONGODB_USERNAME)
        password = quote_plus(self.MONGODB_PASSWORD)
        return f"mongodb+srv://{username}:{password}@{self.MONGODB_CLUSTER}/{self.MONGODB_DATABASE}?retryWrites=true&w=majority&appName=ClusterHeritage"

settings = Settings()