
import os
import json
from app import app, db
from models import ImageAnalysis
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def export_scene_data():
    """
    Export scene data from the image_analysis table to a CSV file.
    Includes only entries with image_type='scene' and exports only 
    specified fields, excluding character-specific columns.
    """
    output_file = "scene_data.csv"
    
    logger.info(f"Starting export of scene data to {output_file}")
    
    with app.app_context():
        # Query the database for scene entries
        scenes = ImageAnalysis.query.filter_by(image_type='scene').all()
        
        logger.info(f"Found {len(scenes)} scene entries")
        
        # Create CSV file with the specified columns
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['image_url', 'image_width', 'image_height', 'image_format', 
                         'image_size_bytes', 'scene_type', 'setting', 
                         'setting_description', 'story_fit', 'dramatic_moments']
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(fieldnames)
            
            # Write data rows
            for scene in scenes:
                # Convert JSONB field to string
                dramatic_moments = json.dumps(scene.dramatic_moments) if scene.dramatic_moments else ''
                
                row = [
                    scene.image_url,
                    scene.image_width,
                    scene.image_height,
                    scene.image_format,
                    scene.image_size_bytes,
                    scene.scene_type or '',
                    scene.setting or '',
                    scene.setting_description or '',
                    scene.story_fit or '',
                    dramatic_moments
                ]
                writer.writerow(row)
        
        logger.info(f"Export completed successfully to {output_file}")
        return output_file

if __name__ == "__main__":
    file_path = export_scene_data()
    print(f"Scene data exported to {file_path}")
