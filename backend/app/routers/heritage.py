from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.ai_service import ai_service
from app.models.heritage import HeritageRecommendationsResponse
# Request model for search
class SearchRequest(BaseModel):
    query: str

router = APIRouter(prefix="/heritage", tags=["heritage"])

@router.post("/search")
async def search_heritage(request: SearchRequest):
    """
    Search for heritage information
    """
    try:
        print(f"🔍 Received search query: {request.query}")
        
        if not request.query or request.query.strip() == "":
            return {"success": False, "error": "Query cannot be empty"}
            
        result = ai_service.search_heritage_info(request.query)
        
        print(f"✅ Search completed for: {request.query}")
        return {"success": True, "result": result}
        
    except Exception as e:
        print(f"❌ Search error: {str(e)}")
        return {"success": False, "error": f"Search failed: {str(e)}"}

@router.post("/upload-image")
async def upload_heritage_image(file: UploadFile = File(...)):
    """
    Upload and analyze a heritage image
    """
    try:
        print(f"🖼️ Received image upload: {file.filename}")
        
        if not file.content_type.startswith('image/'):
            return {"success": False, "error": "Please upload a valid image file"}
        
        image_data = await file.read()
        
        if len(image_data) > 10 * 1024 * 1024:
            return {"success": False, "error": "Image size too large. Please upload images smaller than 10MB"}
            
        result = ai_service.analyze_heritage_image(image_data)
        
        print(f"✅ Image analysis completed: {file.filename}")
        return {"success": True, "result": result}
        
    except Exception as e:
        print(f"❌ Image analysis error: {str(e)}")
        return {"success": False, "error": f"Image analysis failed: {str(e)}"}

@router.get("/recommendations")
async def get_recommendations():
    """
    Get recommended heritage sites to explore
    """
    try:
        recommendations = ai_service.get_heritage_recommendations()
        return HeritageRecommendationsResponse(sites=recommendations)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")

@router.get("/test")
async def test_endpoint():
    """
    Simple test endpoint to verify API is working
    """
    return {"message": "✅ Heritage API is working!", "status": "success"}

@router.get("/config-check")
async def check_config():
    """
    Check API configuration status
    """
    from app.core.config import settings
    from app.services.ai_service import ai_service
    
    config_status = {
        "api_key_configured": bool(settings.OPENROUTER_API_KEY),
        "api_key_length": len(settings.OPENROUTER_API_KEY) if settings.OPENROUTER_API_KEY else 0,
        "base_url": settings.OPENROUTER_BASE_URL,
        "mongodb_configured": bool(settings.MONGODB_USERNAME and settings.MONGODB_PASSWORD),
    }
    
    return {
        "status": "success",
        "config": config_status,
        "message": "API key is configured" if config_status["api_key_configured"] else "⚠️ API key is NOT configured. Please set OPENROUTER_KEY in your .env file"
    }