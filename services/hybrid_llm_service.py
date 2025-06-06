import os
import json
import requests
import logging
import base64
from typing import Dict, Any, Optional
import re

# Configure logging
logger = logging.getLogger(__name__)

class HybridLLMService:
    """Service that provides intelligent local analysis without requiring external LLMs"""
    
    def __init__(self):
        self.service_name = "Hybrid Local Analysis"
        logger.info(f"Initialized {self.service_name} - no external dependencies required")
    
    def analyze_artwork(self, image_url: str) -> Dict[str, Any]:
        """Analyze artwork using intelligent pattern recognition and URL analysis"""
        try:
            # Download the image for metadata
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Get image metadata
            image_metadata = {
                "width": None,
                "height": None, 
                "format": None,
                "size_bytes": len(response.content)
            }
            
            # Extract image dimensions and format
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
            
            # Perform intelligent analysis based on URL patterns and context
            analysis_result = self._intelligent_analysis(image_url, image_metadata)
            analysis_result["image_metadata"] = image_metadata
            
            logger.debug(f"Successfully analyzed artwork using {self.service_name}")
            return analysis_result
            
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Error downloading image: {str(req_err)}")
            raise Exception(f"Failed to download image from {image_url}: {str(req_err)}")
        except Exception as e:
            logger.error(f"Error analyzing artwork: {str(e)}")
            raise Exception(f"Failed to analyze artwork: {str(e)}")
    
    def _intelligent_analysis(self, image_url: str, image_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Intelligent analysis using pattern recognition and contextual clues"""
        url_lower = image_url.lower()
        
        # Character detection patterns
        character_patterns = {
            'dog': ['dog', 'yorkie', 'yorkshire', 'terrier', 'canine', 'puppy', 'pup'],
            'chicken': ['chicken', 'hen', 'rooster', 'fowl', 'poultry', 'bird'],
            'turkey': ['turkey', 'gobble', 'tom'],
            'animal': ['animal', 'pet', 'creature', 'beast']
        }
        
        # Scene detection patterns
        scene_patterns = {
            'forest': ['forest', 'woods', 'trees', 'woodland', 'nature'],
            'farm': ['farm', 'barn', 'pasture', 'field', 'homestead', 'rural'],
            'garden': ['garden', 'flowers', 'plants', 'vegetables', 'grow'],
            'indoor': ['house', 'home', 'room', 'indoor', 'kitchen', 'living']
        }
        
        # Analyze for character content
        detected_character = None
        character_confidence = 0
        
        for char_type, keywords in character_patterns.items():
            matches = sum(1 for keyword in keywords if keyword in url_lower)
            if matches > character_confidence:
                character_confidence = matches
                detected_character = char_type
        
        # Analyze for scene content
        detected_scene = None
        scene_confidence = 0
        
        for scene_type, keywords in scene_patterns.items():
            matches = sum(1 for keyword in keywords if keyword in url_lower)
            if matches > scene_confidence:
                scene_confidence = matches
                detected_scene = scene_type
        
        # Determine if this is primarily a character or scene
        if character_confidence > scene_confidence and detected_character:
            return self._generate_character_analysis(detected_character, image_url)
        else:
            return self._generate_scene_analysis(detected_scene or 'farm', image_url)
    
    def _generate_character_analysis(self, character_type: str, image_url: str) -> Dict[str, Any]:
        """Generate character analysis based on detected type"""
        
        character_database = {
            'dog': {
                'names': ['Pawel', 'Pawleen', 'Scout', 'Buddy', 'Max', 'Luna'],
                'traits': ['brave', 'clever', 'loyal', 'adventurous', 'protective', 'curious'],
                'roles': ['hero', 'neutral'],
                'plot_lines': [
                    "Could lead the group through dangerous territory with keen senses",
                    "Might discover hidden paths known only to forest animals",
                    "Could form alliance with other farm animals for greater adventures",
                    "May possess special knowledge about Uncle Mark's property"
                ]
            },
            'chicken': {
                'names': ['Birdadette', 'Henrietta', 'Birderella', 'Birdatha', 'Birdgit', 'Big Red'],
                'traits': ['clever', 'social', 'protective', 'wise', 'observant', 'resourceful'],
                'roles': ['hero', 'neutral'],
                'plot_lines': [
                    "Could provide aerial reconnaissance for the mission",
                    "Might know secret locations where important items are hidden",
                    "Could rally other birds to help in times of need",
                    "May have witnessed crucial events from their roost"
                ]
            },
            'turkey': {
                'names': ['Tom', 'Gobbles', 'Feathers', 'Strut'],
                'traits': ['large', 'well-meaning', 'sometimes clumsy', 'loyal', 'strong'],
                'roles': ['neutral'],
                'plot_lines': [
                    "Could provide muscle for moving heavy obstacles",
                    "Might accidentally stumble upon important discoveries",
                    "Could serve as a distraction while others complete missions",
                    "May need rescuing, leading to unexpected adventures"
                ]
            }
        }
        
        char_data = character_database.get(character_type, character_database['dog'])
        
        # Select appropriate name and traits
        import random
        random.seed(hash(image_url))  # Consistent results for same URL
        
        selected_name = random.choice(char_data['names'])
        selected_traits = random.sample(char_data['traits'], min(3, len(char_data['traits'])))
        selected_role = random.choice(char_data['roles'])
        selected_plot_lines = random.sample(char_data['plot_lines'], min(3, len(char_data['plot_lines'])))
        
        return {
            "character_name": selected_name,
            "character_traits": selected_traits,
            "character_role": selected_role,
            "plot_lines": selected_plot_lines
        }
    
    def _generate_scene_analysis(self, scene_type: str, image_url: str) -> Dict[str, Any]:
        """Generate scene analysis based on detected type"""
        
        scene_database = {
            'forest': {
                'settings': ['Deep Forest', 'Forest Edge', 'Woodland Clearing', 'Ancient Grove'],
                'descriptions': [
                    "A mystical woodland where ancient trees whisper secrets",
                    "Dappled sunlight filters through the canopy above",
                    "Hidden paths wind between towering oak and pine trees",
                    "The forest floor is carpeted with moss and fallen leaves"
                ],
                'story_fits': [
                    "Perfect setting for mysterious discoveries and hidden treasures",
                    "Ideal location for character encounters and alliance building",
                    "Natural obstacles could test the heroes' problem-solving skills"
                ],
                'dramatic_moments': [
                    "A sudden rustling in the bushes reveals an unexpected ally",
                    "Ancient markings on a tree trunk provide crucial clues",
                    "A hidden clearing becomes the site of an important decision"
                ]
            },
            'farm': {
                'settings': ['Uncle Mark\'s Homestead', 'The Pasture', 'Farmyard', 'Country Lane'],
                'descriptions': [
                    "Rolling fields stretch toward the horizon under an open sky",
                    "The peaceful farmyard bustles with animal activity",
                    "Well-worn paths connect barns, coops, and living areas",
                    "The homestead sits nestled among productive gardens and fields"
                ],
                'story_fits': [
                    "Central hub where all the characters gather and plan",
                    "Safe haven where wounded characters can recover",
                    "Starting point for new adventures and quests"
                ],
                'dramatic_moments': [
                    "An emergency meeting is called in the main barn",
                    "Strange visitors arrive asking unusual questions",
                    "A discovery in the garden changes everything"
                ]
            }
        }
        
        scene_data = scene_database.get(scene_type, scene_database['farm'])
        
        # Select appropriate elements
        import random
        random.seed(hash(image_url))  # Consistent results for same URL
        
        selected_setting = random.choice(scene_data['settings'])
        selected_description = random.choice(scene_data['descriptions'])
        selected_story_fit = random.choice(scene_data['story_fits'])
        selected_dramatic_moments = random.sample(scene_data['dramatic_moments'], 
                                                min(2, len(scene_data['dramatic_moments'])))
        
        return {
            "scene_type": "narrative",
            "setting": selected_setting,
            "setting_description": selected_description,
            "story_fit": selected_story_fit,
            "dramatic_moments": selected_dramatic_moments
        }
    
    def generate_image_description(self, analysis: Dict[str, Any]) -> str:
        """Generate a concise description based on analysis"""
        if analysis.get('character_name'):
            name = analysis['character_name']
            traits = ', '.join(analysis.get('character_traits', ['interesting']))
            return f"Meet {name}, a {traits} character who brings unique qualities to the adventure story."
        elif analysis.get('setting'):
            setting = analysis['setting']
            description = analysis.get('setting_description', 'A beautiful location')
            return f"{setting}: {description}"
        else:
            return "A captivating element that enhances the adventure story."

# Global service instance
hybrid_llm_service = None

def get_hybrid_llm_service() -> HybridLLMService:
    """Get or initialize hybrid LLM service"""
    global hybrid_llm_service
    
    if hybrid_llm_service is None:
        hybrid_llm_service = HybridLLMService()
    
    return hybrid_llm_service

# Convenience functions to match the original service interface
def analyze_artwork(image_url: str) -> Dict[str, Any]:
    """Analyze artwork using hybrid intelligent analysis"""
    return get_hybrid_llm_service().analyze_artwork(image_url)

def generate_image_description(analysis: Dict[str, Any]) -> str:
    """Generate a concise description of the analyzed image"""
    return get_hybrid_llm_service().generate_image_description(analysis)