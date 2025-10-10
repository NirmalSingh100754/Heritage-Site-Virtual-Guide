import requests
import base64
import io
from PIL import Image
from app.core.config import settings

class OpenRouterAIService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        
        # Define prompts for heritage analysis
        self.image_prompt_template = """
        You are an expert historian and heritage guide. Analyze this image of a heritage site and provide detailed information about it.
        
        Please provide information in the following format:
        
        Name: [Official name of the heritage site]
        Location: [City, Country]
        Historical Period: [When it was built]
        Builder/Creator: [Who built/created it]
        Significance: [Why it's important historically/culturally]
        Architectural Style: [Architectural features and style]
        Current Status: [UNESCO status, conservation status, etc.]
        Interesting Facts: [3-5 interesting facts about the site]
        Nearby Attractions: [Other tourist attractions nearby]
        Best Time to Visit: [Ideal time to visit]
        
        If this is not a recognized heritage site, please politely indicate that and ask for a clearer image or more context.
        """
        
        self.text_prompt_template = """
        You are an expert historian and heritage guide. Provide comprehensive information about the following heritage site: {heritage_query}
        
        Please provide information in the following format:
        
        Name: [Official name of the heritage site]
        Location: [City, Country]
        Historical Period: [When it was built]
        Builder/Creator: [Who built/created it]
        Significance: [Why it's important historically/culturally]
        Architectural Style: [Architectural features and style]
        History: [Detailed historical background]
        Current Status: [UNESCO status, conservation status, etc.]
        Interesting Facts: [5-7 interesting facts about the site]
        Visitor Information: [Opening hours, entry fees, best time to visit]
        Nearby Attractions: [Other tourist attractions nearby]
        Travel Tips: [Practical advice for visitors]
        
        If this is not a recognized heritage site, please provide information about similar heritage sites or ask for clarification.
        """
    
    def _call_openrouter(self, messages, model="openai/gpt-3.5-turbo"):
        """Make API call to OpenRouter"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://heritage-virtual-guide.com",  # Required by OpenRouter
            "X-Title": "Heritage Virtual Guide"  # Required by OpenRouter
        }
        
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"OpenRouter API Error: {str(e)}")
            return f"Error calling AI service: {str(e)}"
    
    def analyze_heritage_image(self, image_data):
        """Analyze heritage site from image using OpenRouter with vision models"""
        try:
            # Convert image to base64
            image = Image.open(io.BytesIO(image_data))
            
            # Convert image to base64 string
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.image_prompt_template
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_str}"
                            }
                        }
                    ]
                }
            ]
            
            # Use a vision model - try different models if one fails
            vision_models = [
                "google/gemini-pro-vision",  # Free vision model
                "openai/gpt-4-vision-preview",  # Paid but high quality
                "anthropic/claude-3-sonnet"  # Alternative vision model
            ]
            
            for model in vision_models:
                try:
                    result = self._call_openrouter(messages, model)
                    if result and not result.startswith("Error"):
                        return result
                except Exception as e:
                    print(f"Model {model} failed: {str(e)}")
                    continue
            
            return "Sorry, I couldn't analyze this image. Please try again with a clearer image of a heritage site."
            
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    def search_heritage_info(self, query):
        """Get heritage information from text query using OpenRouter"""
        try:
            formatted_prompt = self.text_prompt_template.format(heritage_query=query)
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful historian and heritage guide expert."
                },
                {
                    "role": "user", 
                    "content": formatted_prompt
                }
            ]
            
            # Try different models for best results
            text_models = [
                "openai/gpt-3.5-turbo",  # Fast and cost-effective
                "anthropic/claude-3-sonnet",  # Good for detailed responses
                "google/gemini-pro",  # Alternative
                "meta-llama/llama-2-13b-chat"  # Open source option
            ]
            
            for model in text_models:
                try:
                    result = self._call_openrouter(messages, model)
                    if result and not result.startswith("Error"):
                        return result
                except Exception as e:
                    print(f"Model {model} failed: {str(e)}")
                    continue
            
            return "Sorry, I couldn't find information about this heritage site. Please try a different search term."
            
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def get_heritage_recommendations(self):
        """Get recommended heritage sites"""
        recommendations = [
            {
                "name": "Taj Mahal",
                "location": "Agra, India",
                "description": "Iconic white marble mausoleum and UNESCO World Heritage Site built by Mughal Emperor Shah Jahan",
                "image_url": "/assets/images/taj-mahal.jpg"
            },
            {
                "name": "Great Pyramid of Giza",
                "location": "Giza, Egypt",
                "description": "Ancient Egyptian pyramid and the oldest of the Seven Wonders of the Ancient World",
                "image_url": "/assets/images/pyramid.jpg"
            },
            {
                "name": "Colosseum",
                "location": "Rome, Italy",
                "description": "Ancient Roman amphitheater and iconic symbol of Imperial Rome",
                "image_url": "/assets/images/colosseum.jpg"
            },
            {
                "name": "Machu Picchu",
                "location": "Cusco, Peru",
                "description": "15th-century Inca citadel high in the Andes Mountains",
                "image_url": "/assets/images/machu-picchu.jpg"
            },
            {
                "name": "Great Wall of China",
                "location": "Beijing, China", 
                "description": "Series of fortifications made of stone, brick, and other materials",
                "image_url": "/assets/images/great-wall.jpg"
            },
            {
                "name": "Petra",
                "location": "Ma'an Governorate, Jordan",
                "description": "Historical and archaeological city famous for its rock-cut architecture",
                "image_url": "/assets/images/petra.jpg"
            }
        ]
        return recommendations

# Global AI service instance
ai_service = OpenRouterAIService()