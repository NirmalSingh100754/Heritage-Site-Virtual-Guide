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
        if not self.api_key:
            print("❌ OPENROUTER_API_KEY is not set!")
            return None
        
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
            print(f"🔄 Calling OpenRouter API with model: {model}")
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"✅ Successfully got response from {model}")
            return content
        except requests.exceptions.HTTPError as e:
            error_detail = ""
            try:
                error_response = e.response.json()
                error_detail = error_response.get('error', {}).get('message', str(e))
            except:
                error_detail = e.response.text
            print(f"❌ HTTP Error for {model}: {error_detail}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error for {model}: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected Error for {model}: {str(e)}")
            return None
    
    def analyze_heritage_image(self, image_data):
        """Analyze heritage site from image using OpenRouter with vision models"""
        try:
            # Check API key first
            if not self.api_key:
                return "Error: OPENROUTER_API_KEY is not configured. Please set it in your environment variables."
            
            # Convert image to base64
            try:
                image = Image.open(io.BytesIO(image_data))
                # Convert to RGB if necessary (some images might be RGBA)
                if image.mode in ('RGBA', 'LA', 'P'):
                    image = image.convert('RGB')
            except Exception as e:
                return f"Error processing image: {str(e)}. Please ensure you uploaded a valid image file."
            
            # Convert image to base64 string
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG", quality=85)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Standard OpenAI vision format (works for GPT-4 vision models)
            messages_standard = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": self.image_prompt_template.strip()
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
            # Updated to use more reliable vision models available on OpenRouter
            vision_models = [
                ("openai/gpt-4o", messages_standard),  # GPT-4 Omni with vision support
                ("openai/gpt-4-turbo", messages_standard),  # GPT-4 Turbo with vision
                ("openai/gpt-4-vision-preview", messages_standard),  # GPT-4 Vision Preview
                ("anthropic/claude-3-opus", messages_standard),  # Claude 3 Opus
                ("anthropic/claude-3-sonnet", messages_standard),  # Claude 3 Sonnet
                ("anthropic/claude-3-haiku", messages_standard),  # Claude 3 Haiku (faster)
                ("google/gemini-pro-vision", messages_standard),  # Free vision model
            ]
            
            last_error = None
            for model, messages in vision_models:
                try:
                    print(f"🔄 Trying vision model: {model}")
                    result = self._call_openrouter(messages, model)
                    if result and result.strip() and not result.startswith("Error"):
                        print(f"✅ Successfully analyzed image using {model}")
                        return result
                    else:
                        print(f"⚠️ Model {model} returned empty or error result")
                except Exception as e:
                    last_error = str(e)
                    print(f"❌ Model {model} failed with exception: {last_error}")
                    continue
            
            # If all models failed, return a helpful error message
            error_msg = "Sorry, I couldn't analyze this image. "
            if not self.api_key:
                error_msg += "API key is not configured. Please check your environment variables."
            elif last_error:
                error_msg += f"All vision models failed. Last error: {last_error}. Please check your API key and try again."
            else:
                error_msg += "All vision models failed. Please check your API key configuration and try again with a clearer image."
            
            print(f"❌ All vision models failed. Last error: {last_error}")
            return error_msg
            
        except Exception as e:
            error_msg = f"Error analyzing image: {str(e)}"
            print(f"❌ Exception in analyze_heritage_image: {error_msg}")
            return error_msg
    
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
            
            last_error = None
            for model in text_models:
                try:
                    result = self._call_openrouter(messages, model)
                    if result and result.strip():
                        return result
                except Exception as e:
                    last_error = str(e)
                    print(f"❌ Model {model} failed: {last_error}")
                    continue
            
            error_msg = "Sorry, I couldn't find information about this heritage site. "
            if not self.api_key:
                error_msg += "API key is not configured."
            elif last_error:
                error_msg += f"Error: {last_error}"
            else:
                error_msg += "Please try a different search term."
            
            return error_msg
            
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