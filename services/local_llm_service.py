import os
import json
import requests
import logging
import base64
from typing import Dict, Any, Optional
import ollama
import subprocess
import time

# Configure logging
logger = logging.getLogger(__name__)

class LocalLLMService:
    """Service for interacting with local LLM models via Ollama"""
    
    def __init__(self, model_name: str = "phi3:mini"):
        self.model_name = model_name
        self.client = None
        self.ollama_available = False
        self._setup_ollama()
    
    def _setup_ollama(self):
        """Setup Ollama service and client"""
        try:
            # Try to start Ollama service
            self._start_ollama_service()
            
            # Initialize client
            self.client = ollama.Client()
            
            # Test connection and setup model
            self._ensure_model_available()
            self.ollama_available = True
            logger.info("Ollama service initialized successfully")
            
        except Exception as e:
            logger.warning(f"Could not initialize Ollama: {str(e)}")
            logger.info("Will use fallback text-based analysis")
            self.ollama_available = False
    
    def _start_ollama_service(self):
        """Start Ollama service if not running"""
        try:
            # Check if Ollama is already running
            result = subprocess.run(['pgrep', '-f', 'ollama serve'], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:  # Not running
                logger.info("Starting Ollama service...")
                # Start Ollama in background
                subprocess.Popen(['ollama', 'serve'], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
                # Wait for service to start
                time.sleep(3)
                
        except Exception as e:
            logger.warning(f"Could not start Ollama service: {str(e)}")
            raise
    
    def _ensure_model_available(self):
        """Ensure the model is downloaded and available"""
        try:
            # Check if model is already available
            models = self.client.list()
            model_names = [model['name'] for model in models['models']]
            
            if self.model_name not in model_names:
                logger.info(f"Downloading {self.model_name} model...")
                self.client.pull(self.model_name)
                logger.info(f"Model {self.model_name} downloaded successfully")
            else:
                logger.info(f"Model {self.model_name} is available")
                
        except Exception as e:
            logger.error(f"Error checking/downloading model: {str(e)}")
            raise Exception(f"Failed to setup model {self.model_name}: {str(e)}")
    
    def analyze_artwork(self, image_url: str) -> Dict[str, Any]:
        """Analyze artwork using local LLM or fallback to rule-based analysis"""
        try:
            # Download the image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Get image metadata
            image_metadata = {
                "width": None,
                "height": None, 
                "format": None,
                "size_bytes": len(response.content)
            }
            
            # Try to get image dimensions and format
            try:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(response.content))
                image_metadata.update({
                    "width": img.width,
                    "height": img.height,
                    "format": img.format.lower() if img.format else "unknown"
                })
            except Exception as img_err:
                logger.warning(f"Could not extract image metadata: {str(img_err)}")
            
            # Use local LLM if available, otherwise use rule-based analysis
            if self.ollama_available and self.client:
                return self._analyze_with_llm(image_url, image_metadata)
            else:
                return self._analyze_with_fallback(image_url, image_metadata)
            
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Error downloading image: {str(req_err)}")
            raise Exception(f"Failed to download image from {image_url}: {str(req_err)}")
        except Exception as e:
            logger.error(f"Error analyzing artwork: {str(e)}")
            raise Exception(f"Failed to analyze artwork: {str(e)}")
    
    def _analyze_with_llm(self, image_url: str, image_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze using local LLM"""
        try:
            system_prompt = """You are an expert analyzer of images for a "Choose Your Own Adventure" story universe.

The universe is centered around Uncle Mark's forest farm where two Yorkshire Terriers are the main characters:
- Pawel (male) - fearless, clever, impulsive
- Pawleen (female) - fearless, clever, thoughtful

Key characters in this universe:
1. HEROES:
   - The Yorkies (Pawel and Pawleen) - masters of the forest homestead and pasture
   - Chickens - clever birds with personality (30+ of them)
     - Big Red (the rooster, not very smart)
     - Main hens (clever): Birdadette, Henrietta, Birderella, Birdatha, Birdgit

2. NEUTRAL:
   - Turkeys - big, white, not very smart, always getting stuck

Analyze this image and determine if it shows a CHARACTER or a SCENE. Then provide detailed analysis.

For CHARACTERS, provide:
- character_name: string
- character_traits: array of strings
- character_role: "hero", "villain", or "neutral"
- plot_lines: array of story suggestions

For SCENES, provide:
- scene_type: string (e.g., "narrative", "choice", "action")  
- setting: string
- setting_description: string
- story_fit: string
- dramatic_moments: array of strings

Respond in JSON format with the appropriate keys based on the image type. Use snake_case for all field names."""

            user_prompt = f"Please analyze this image for our Choose Your Own Adventure story:\n\nImage URL: {image_url}\nImage size: {image_metadata['size_bytes']} bytes"
            
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                format='json'
            )
            
            content = response['message']['content']
            result = json.loads(content)
            result["image_metadata"] = image_metadata
            
            logger.debug("Successfully analyzed artwork with local LLM")
            return result
            
        except Exception as e:
            logger.warning(f"LLM analysis failed: {str(e)}, falling back to rule-based analysis")
            return self._analyze_with_fallback(image_url, image_metadata)
    
    def _analyze_with_fallback(self, image_url: str, image_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback rule-based analysis when LLM is not available"""
        logger.info("Using rule-based analysis (LLM not available)")
        
        # Simple heuristics based on filename/URL patterns
        url_lower = image_url.lower()
        
        # Check for character-related keywords
        character_keywords = ['dog', 'yorkie', 'terrier', 'chicken', 'rooster', 'hen', 'turkey', 'animal', 'pet']
        scene_keywords = ['forest', 'farm', 'barn', 'field', 'pasture', 'garden', 'landscape', 'scene']
        
        is_character = any(keyword in url_lower for keyword in character_keywords)
        is_scene = any(keyword in url_lower for keyword in scene_keywords)
        
        if is_character and not is_scene:
            # Generate character analysis
            return {
                "character_name": "Unknown Character",
                "character_traits": ["mysterious", "intriguing", "story-worthy"],
                "character_role": "neutral",
                "plot_lines": [
                    "This character could become an ally in the adventure",
                    "They might have important information for Pawel and Pawleen",
                    "Their unique abilities could help solve problems"
                ],
                "image_metadata": image_metadata
            }
        else:
            # Generate scene analysis
            return {
                "scene_type": "narrative",
                "setting": "Uncle Mark's farm",
                "setting_description": "A beautiful location that fits perfectly into the adventure story",
                "story_fit": "This setting provides an excellent backdrop for character interactions and plot development",
                "dramatic_moments": [
                    "Characters could discover something important here",
                    "This location might be where key decisions are made",
                    "The environment could present challenges or opportunities"
                ],
                "image_metadata": image_metadata
            }
    
    def generate_story(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate story content using local LLM or fallback"""
        if self.ollama_available and self.client:
            return self._generate_story_with_llm(prompt, **kwargs)
        else:
            return self._generate_story_fallback(prompt, **kwargs)
    
    def _generate_story_with_llm(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate story using local LLM"""
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a creative storyteller specializing in Choose Your Own Adventure stories. Generate engaging, interactive narratives with meaningful choices.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                format='json'
            )
            
            content = response['message']['content']
            result = json.loads(content)
            
            logger.debug("Successfully generated story with local LLM")
            return result
            
        except Exception as e:
            logger.warning(f"LLM story generation failed: {str(e)}, using fallback")
            return self._generate_story_fallback(prompt, **kwargs)
    
    def _generate_story_fallback(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Fallback story generation when LLM is not available"""
        logger.info("Using fallback story generation (LLM not available)")
        
        return {
            "narrative": "Pawel and Pawleen found themselves at an interesting crossroads in their adventure. The Yorkshire Terriers exchanged knowing glances, their keen instincts telling them that an important decision lay ahead. The forest around them seemed to hold its breath, waiting to see which path they would choose.",
            "choices": [
                {"text": "Explore the mysterious path ahead", "consequence_hint": "Discover new adventures"},
                {"text": "Investigate the interesting sounds nearby", "consequence_hint": "Meet new characters"},
                {"text": "Return and gather more information", "consequence_hint": "Prepare for challenges"}
            ],
            "setting_details": "A peaceful forest clearing with multiple paths",
            "character_focus": "Pawel and Pawleen",
            "tension_level": "medium"
        }
    
    def generate_image_description(self, analysis: Dict[str, Any]) -> str:
        """Generate a concise description of the analyzed image"""
        if self.ollama_available and self.client:
            return self._generate_description_with_llm(analysis)
        else:
            return self._generate_description_fallback(analysis)
    
    def _generate_description_with_llm(self, analysis: Dict[str, Any]) -> str:
        """Generate description using local LLM"""
        try:
            prompt = f"Based on this image analysis, write a concise, engaging description:\n{json.dumps(analysis, indent=2)}"
            
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a skilled writer. Create concise, vivid descriptions based on image analysis data.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            return response['message']['content'].strip()
            
        except Exception as e:
            logger.warning(f"LLM description generation failed: {str(e)}, using fallback")
            return self._generate_description_fallback(analysis)
    
    def _generate_description_fallback(self, analysis: Dict[str, Any]) -> str:
        """Fallback description generation"""
        if analysis.get('character_name'):
            return f"An intriguing character named {analysis['character_name']} who could play an important role in the adventure."
        elif analysis.get('setting'):
            return f"A beautiful {analysis['setting']} that provides the perfect backdrop for storytelling."
        else:
            return "A captivating scene from the adventure story."

# Global service instance
local_llm_service = None

def get_local_llm_service() -> LocalLLMService:
    """Get or initialize local LLM service"""
    global local_llm_service
    
    if local_llm_service is None:
        local_llm_service = LocalLLMService()
    
    return local_llm_service

# Convenience functions to match the OpenAI service interface
def analyze_artwork(image_url: str) -> Dict[str, Any]:
    """Analyze artwork using local LLM"""
    return get_local_llm_service().analyze_artwork(image_url)

def generate_image_description(analysis: Dict[str, Any]) -> str:
    """Generate a concise description of the analyzed image"""
    return get_local_llm_service().generate_image_description(analysis)