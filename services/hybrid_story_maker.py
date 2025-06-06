import os
import json
import logging
import random
from typing import Dict, List, Tuple, Optional, Any

# Configure logging
logger = logging.getLogger(__name__)

def get_story_options() -> Dict[str, List[Tuple[str, str]]]:
    """Return available story options for UI display"""
    return {
        "conflicts": [
            ("mystery", "A mysterious disappearance or strange occurrence"),
            ("rescue", "Someone or something needs to be rescued"),
            ("adventure", "An exciting journey or quest"),
            ("friendship", "Building bonds and working together"),
            ("rivalry", "Competition between characters"),
            ("survival", "Overcoming dangerous situations"),
            ("discovery", "Finding something new or important"),
            ("protection", "Defending home or loved ones")
        ],
        "settings": [
            ("forest", "Deep in the enchanted forest"),
            ("farm", "Around Uncle Mark's homestead"),
            ("pasture", "In the open grazing fields"),
            ("chicken_coop", "Near the bustling chicken community"),
            ("creek", "By the babbling forest creek"),
            ("barn", "Inside the old wooden barn"),
            ("garden", "Among the vegetable patches"),
            ("meadow", "In the sunny wildflower meadow")
        ],
        "narrative_styles": [
            ("playful", "Light-hearted and fun"),
            ("mysterious", "Suspenseful and intriguing"),
            ("heroic", "Bold and courageous"),
            ("cozy", "Warm and comfortable"),
            ("adventurous", "Thrilling and exciting"),
            ("educational", "Learning through experience"),
            ("humorous", "Funny and entertaining"),
            ("dramatic", "Intense and emotional")
        ],
        "moods": [
            ("cheerful", "Happy and optimistic"),
            ("suspenseful", "Tense and exciting"),
            ("peaceful", "Calm and serene"),
            ("energetic", "Active and lively"),
            ("mysterious", "Dark and intriguing"),
            ("heartwarming", "Touching and emotional"),
            ("comedic", "Funny and amusing"),
            ("inspiring", "Uplifting and motivating")
        ]
    }

class HybridStoryMaker:
    """Intelligent story generation without external dependencies"""
    
    def __init__(self):
        self.story_templates = self._load_story_templates()
        self.character_database = self._load_character_database()
        logger.info("Initialized Hybrid Story Maker with intelligent narrative generation")
    
    def _load_story_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Load story templates organized by conflict and mood combinations"""
        return {
            "mystery_suspenseful": {
                "openings": [
                    "The morning mist clung to Uncle Mark's farm as {characters} noticed something peculiar. Strange tracks led from the chicken coop toward the dark forest, and several of the hens were acting unusually nervous.",
                    "A series of unexplained sounds had been echoing through the barn at night. {characters} decided it was time to investigate what was causing the mysterious disturbances.",
                    "When the morning feed time arrived, {characters} discovered that something important had vanished without a trace. The only clue was an unusual scent lingering in the air."
                ],
                "developments": [
                    "Following the trail deeper into their investigation, {characters} realized this mystery was more complex than they initially thought.",
                    "As they pieced together the clues, {characters} began to understand that someone—or something—needed their help urgently.",
                    "The evidence pointed toward the old section of the farm that hadn't been explored in years."
                ]
            },
            "rescue_heroic": {
                "openings": [
                    "A distress call echoed across Uncle Mark's property as {characters} sprang into action. One of their friends was in serious trouble and needed immediate assistance.",
                    "The peaceful morning was shattered when {characters} realized that someone dear to them had gone missing during the night storm.",
                    "Racing against time, {characters} learned that a fellow farm resident had become trapped and was depending on them for rescue."
                ],
                "developments": [
                    "The rescue mission proved more challenging than expected, requiring {characters} to use all their skills and courage.",
                    "Working together, {characters} devised a clever plan that played to each of their unique strengths.",
                    "Time was running out, and {characters} had to make a critical decision about the best way to help."
                ]
            },
            "adventure_energetic": {
                "openings": [
                    "The day promised excitement as {characters} set off to explore parts of Uncle Mark's vast property they'd never seen before.",
                    "An old map discovered in the barn sparked {characters}' imagination and led them on an unexpected quest.",
                    "When strange new visitors arrived at the farm, {characters} found themselves embarking on an adventure beyond their wildest dreams."
                ],
                "developments": [
                    "Each step of their journey revealed new wonders and unexpected challenges for {characters} to overcome.",
                    "The adventure tested not only their bravery but also their friendship as {characters} faced difficult choices.",
                    "As they ventured further from home, {characters} discovered abilities they never knew they possessed."
                ]
            },
            "friendship_heartwarming": {
                "openings": [
                    "A misunderstanding between old friends prompted {characters} to step in and help heal the rift in their community.",
                    "When a new animal arrived at Uncle Mark's farm, {characters} took it upon themselves to make the newcomer feel welcome.",
                    "The annual farm gathering was approaching, and {characters} wanted to organize something special to bring everyone together."
                ],
                "developments": [
                    "Through their efforts, {characters} learned valuable lessons about understanding and forgiveness.",
                    "The bonds of friendship grew stronger as {characters} worked side by side toward their common goal.",
                    "Each character contributed their unique talents, showing how diversity makes their group stronger."
                ]
            }
        }
    
    def _load_character_database(self) -> Dict[str, Dict[str, Any]]:
        """Load character information and personality traits"""
        return {
            "Pawel": {
                "species": "Yorkshire Terrier",
                "traits": ["fearless", "clever", "impulsive", "protective"],
                "motivations": ["protecting the farm", "seeking adventure", "solving problems quickly"],
                "dialogue_style": "direct and action-oriented"
            },
            "Pawleen": {
                "species": "Yorkshire Terrier", 
                "traits": ["fearless", "clever", "thoughtful", "strategic"],
                "motivations": ["keeping everyone safe", "making wise decisions", "building consensus"],
                "dialogue_style": "measured and considerate"
            },
            "Big Red": {
                "species": "Rooster",
                "traits": ["well-meaning", "not very smart", "loud", "proud"],
                "motivations": ["protecting the hens", "proving his worth", "being helpful"],
                "dialogue_style": "enthusiastic but sometimes confused"
            },
            "Birdadette": {
                "species": "Hen",
                "traits": ["clever", "observant", "social", "wise"],
                "motivations": ["gathering information", "helping friends", "maintaining harmony"],
                "dialogue_style": "insightful and diplomatic"
            },
            "Henrietta": {
                "species": "Hen",
                "traits": ["clever", "organized", "practical", "efficient"],
                "motivations": ["solving logistical problems", "keeping things running smoothly"],
                "dialogue_style": "practical and solution-focused"
            }
        }
    
    def generate_story(self, 
                      conflict: str,
                      setting: str, 
                      narrative_style: str,
                      mood: str,
                      character_info: Optional[Dict[str, Any]] = None,
                      custom_conflict: Optional[str] = None,
                      custom_setting: Optional[str] = None,
                      custom_narrative: Optional[str] = None,
                      custom_mood: Optional[str] = None,
                      previous_choice: Optional[str] = None,
                      story_context: Optional[str] = None,
                      additional_characters: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Generate an intelligent story based on parameters and character information"""
        
        try:
            # Use custom parameters if provided
            final_conflict = custom_conflict if custom_conflict else conflict
            final_setting = custom_setting if custom_setting else setting
            final_narrative = custom_narrative if custom_narrative else narrative_style
            final_mood = custom_mood if custom_mood else mood
            
            # Set up random seed for consistent results based on parameters
            seed_string = f"{final_conflict}_{final_setting}_{final_narrative}_{final_mood}"
            random.seed(hash(seed_string))
            
            # Determine main characters for the story
            main_characters = self._select_characters(character_info, additional_characters)
            
            # Generate the narrative
            if previous_choice and story_context:
                narrative = self._generate_continuation(
                    final_conflict, final_setting, final_narrative, final_mood,
                    main_characters, previous_choice, story_context
                )
            else:
                narrative = self._generate_opening(
                    final_conflict, final_setting, final_narrative, final_mood, main_characters
                )
            
            # Generate meaningful choices
            choices = self._generate_choices(final_conflict, final_mood, main_characters)
            
            # Determine tension level
            tension_level = self._calculate_tension_level(final_conflict, final_mood)
            
            result = {
                "narrative": narrative,
                "choices": choices,
                "setting_details": self._generate_setting_details(final_setting),
                "character_focus": ", ".join([char["name"] for char in main_characters]),
                "tension_level": tension_level
            }
            
            logger.info(f"Generated story with conflict: {final_conflict}, setting: {final_setting}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            return self._generate_fallback_story(conflict, setting)
    
    def _select_characters(self, character_info: Optional[Dict[str, Any]], 
                          additional_characters: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Select main characters for the story"""
        characters = []
        
        # Always include Pawel and Pawleen as main characters
        characters.extend([
            {"name": "Pawel", "data": self.character_database["Pawel"]},
            {"name": "Pawleen", "data": self.character_database["Pawleen"]}
        ])
        
        # Add specified character if provided
        if character_info and character_info.get('character_name'):
            char_name = character_info['character_name']
            if char_name in self.character_database:
                characters.append({"name": char_name, "data": self.character_database[char_name]})
            else:
                # Create character from provided info
                characters.append({
                    "name": char_name,
                    "data": {
                        "traits": character_info.get('character_traits', ['mysterious']),
                        "motivations": ["helping the main characters"],
                        "dialogue_style": "helpful and supportive"
                    }
                })
        
        # Add additional characters if provided
        if additional_characters:
            for char in additional_characters:
                if char.get('character_name'):
                    characters.append({
                        "name": char['character_name'],
                        "data": {
                            "traits": char.get('character_traits', ['friendly']),
                            "motivations": ["contributing to the group"],
                            "dialogue_style": "cooperative"
                        }
                    })
        
        # Add one supporting character from the database
        supporting_chars = ["Big Red", "Birdadette", "Henrietta"]
        available_chars = [name for name in supporting_chars 
                          if name not in [char["name"] for char in characters]]
        if available_chars:
            selected = random.choice(available_chars)
            characters.append({"name": selected, "data": self.character_database[selected]})
        
        return characters
    
    def _generate_opening(self, conflict: str, setting: str, narrative_style: str, 
                         mood: str, characters: List[Dict[str, Any]]) -> str:
        """Generate an opening narrative"""
        
        # Create character list for template
        char_names = [char["name"] for char in characters[:3]]  # Use first 3 characters
        character_string = ", ".join(char_names[:-1]) + f" and {char_names[-1]}" if len(char_names) > 1 else char_names[0]
        
        # Find appropriate template
        template_key = f"{conflict}_{mood}"
        templates = self.story_templates.get(template_key, self.story_templates["adventure_energetic"])
        
        # Select opening and development
        opening = random.choice(templates["openings"])
        development = random.choice(templates["developments"])
        
        # Format with characters
        opening = opening.format(characters=character_string)
        development = development.format(characters=character_string)
        
        # Add setting-specific details
        setting_detail = self._get_setting_flavor(setting)
        
        return f"{opening}\n\n{development} {setting_detail}"
    
    def _generate_continuation(self, conflict: str, setting: str, narrative_style: str,
                              mood: str, characters: List[Dict[str, Any]], 
                              previous_choice: str, story_context: str) -> str:
        """Generate a continuation based on previous choice"""
        
        char_names = [char["name"] for char in characters[:2]]
        character_string = " and ".join(char_names)
        
        continuations = {
            "mystery": f"Following their decision to {previous_choice.lower()}, {character_string} discovered new clues that deepened the mystery. The investigation was leading them toward an unexpected revelation.",
            "rescue": f"After choosing to {previous_choice.lower()}, {character_string} found themselves closer to their goal but facing new obstacles in their rescue mission.",
            "adventure": f"Their choice to {previous_choice.lower()} led {character_string} down an exciting new path filled with possibilities they hadn't considered before.",
            "friendship": f"By deciding to {previous_choice.lower()}, {character_string} took an important step toward strengthening the bonds within their community."
        }
        
        base_continuation = continuations.get(conflict, continuations["adventure"])
        
        # Add specific consequence based on choice content
        if "investigate" in previous_choice.lower():
            consequence = " Their careful examination revealed details that others had missed."
        elif "help" in previous_choice.lower():
            consequence = " Their willingness to assist opened new opportunities for cooperation."
        elif "explore" in previous_choice.lower():
            consequence = " The new territory held surprises that would change their perspective."
        else:
            consequence = " The outcome of their decision would shape what happened next."
        
        return base_continuation + consequence
    
    def _generate_choices(self, conflict: str, mood: str, characters: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate three meaningful choices based on story context"""
        
        choice_templates = {
            "mystery": [
                {"text": "Investigate the most obvious clue first", "consequence_hint": "Direct approach might reveal key information"},
                {"text": "Search for hidden evidence others missed", "consequence_hint": "Thorough investigation could uncover secrets"},
                {"text": "Ask the other animals what they observed", "consequence_hint": "Community knowledge might provide insights"}
            ],
            "rescue": [
                {"text": "Take the quickest but riskiest route", "consequence_hint": "Speed might save the day but danger awaits"},
                {"text": "Gather supplies and helpers first", "consequence_hint": "Preparation increases chances of success"},
                {"text": "Scout the area to understand the situation", "consequence_hint": "Information gathering reduces unknown risks"}
            ],
            "adventure": [
                {"text": "Follow the most intriguing path ahead", "consequence_hint": "Curiosity leads to exciting discoveries"},
                {"text": "Stick together and proceed cautiously", "consequence_hint": "Teamwork ensures everyone stays safe"},
                {"text": "Split up to cover more ground quickly", "consequence_hint": "Efficiency might reveal multiple opportunities"}
            ],
            "friendship": [
                {"text": "Address the conflict directly and honestly", "consequence_hint": "Open communication can heal relationships"},
                {"text": "Find a compromise that works for everyone", "consequence_hint": "Diplomatic solutions build stronger bonds"},
                {"text": "Organize a group activity to bring everyone together", "consequence_hint": "Shared experiences create lasting connections"}
            ]
        }
        
        base_choices = choice_templates.get(conflict, choice_templates["adventure"])
        
        # Customize choices based on available characters
        if any(char["name"] in ["Big Red", "Birdadette", "Henrietta"] for char in characters):
            # Modify one choice to leverage chicken abilities
            base_choices[1]["text"] = base_choices[1]["text"].replace("first", "with aerial reconnaissance")
            base_choices[1]["consequence_hint"] = "Bird's eye view provides strategic advantages"
        
        return base_choices
    
    def _generate_setting_details(self, setting: str) -> str:
        """Generate detailed setting description"""
        setting_details = {
            "forest": "Ancient trees tower overhead, their branches creating a natural cathedral. Dappled sunlight filters through the leaves, illuminating patches of wildflowers and moss-covered fallen logs.",
            "farm": "The familiar sights and sounds of Uncle Mark's homestead surround the characters - the gentle lowing of cattle, the rustle of grain in the breeze, and the warm smell of hay.",
            "pasture": "Rolling green fields stretch to the horizon, dotted with shade trees and crisscrossed by old stone walls that have stood for generations.",
            "chicken_coop": "The bustling center of poultry activity, where wise hens share gossip and important information while going about their daily routines.",
            "creek": "Clear water babbles over smooth stones, creating a peaceful soundtrack while cattails sway gently in the breeze along the banks.",
            "barn": "The massive structure provides shelter and storage, its high rafters home to swallows and its corners filled with the tools of farm life.",
            "garden": "Neat rows of vegetables and herbs create a patchwork of green, while bees buzz among the flowering plants and butterflies dance in the warm air.",
            "meadow": "Wildflowers carpet the open space in brilliant colors, while butterflies and bees go about their work in the peaceful countryside setting."
        }
        
        return setting_details.get(setting, setting_details["farm"])
    
    def _get_setting_flavor(self, setting: str) -> str:
        """Get setting-specific narrative flavor"""
        flavors = {
            "forest": "The deep woods seemed to hold their breath, waiting to see what would unfold.",
            "farm": "The familiar surroundings of home provided comfort even in uncertain times.",
            "pasture": "The open fields offered room to think and plan their next move.",
            "chicken_coop": "The social hub of the farm buzzed with activity and shared information.",
            "creek": "The gentle sound of flowing water provided a peaceful backdrop for important decisions.",
            "barn": "The shelter of the great barn offered protection while they considered their options.",
            "garden": "Among the growing plants, new ideas seemed to take root naturally.",
            "meadow": "The open space invited careful consideration of all possibilities."
        }
        
        return flavors.get(setting, flavors["farm"])
    
    def _calculate_tension_level(self, conflict: str, mood: str) -> str:
        """Calculate appropriate tension level"""
        high_tension = ["mystery", "rescue", "survival"]
        medium_tension = ["adventure", "rivalry", "discovery"]
        low_tension = ["friendship", "protection"]
        
        suspenseful_moods = ["suspenseful", "mysterious"]
        calm_moods = ["peaceful", "cheerful", "heartwarming"]
        
        if conflict in high_tension or mood in suspenseful_moods:
            return "high"
        elif conflict in medium_tension and mood not in calm_moods:
            return "medium"
        else:
            return "low"
    
    def _generate_fallback_story(self, conflict: str, setting: str) -> Dict[str, Any]:
        """Generate a simple fallback story structure"""
        return {
            "narrative": "Pawel and Pawleen found themselves facing an interesting situation that would test their cleverness and teamwork. The Yorkshire Terriers knew that whatever challenges lay ahead, they could handle them together with wisdom and courage.",
            "choices": [
                {"text": "Approach the situation with careful planning", "consequence_hint": "Thoughtful preparation leads to success"},
                {"text": "Trust their instincts and take action", "consequence_hint": "Quick thinking opens new possibilities"},
                {"text": "Seek advice from their friends first", "consequence_hint": "Community wisdom provides valuable guidance"}
            ],
            "setting_details": self._generate_setting_details(setting),
            "character_focus": "Pawel and Pawleen",
            "tension_level": "medium"
        }

# Create global instance
hybrid_story_maker = HybridStoryMaker()

def generate_story(conflict: str, setting: str, narrative_style: str, mood: str,
                  character_info: Optional[Dict[str, Any]] = None,
                  custom_conflict: Optional[str] = None,
                  custom_setting: Optional[str] = None,
                  custom_narrative: Optional[str] = None,
                  custom_mood: Optional[str] = None,
                  previous_choice: Optional[str] = None,
                  story_context: Optional[str] = None,
                  additional_characters: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Generate a story using the hybrid story maker"""
    return hybrid_story_maker.generate_story(
        conflict, setting, narrative_style, mood,
        character_info, custom_conflict, custom_setting, custom_narrative, custom_mood,
        previous_choice, story_context, additional_characters
    )