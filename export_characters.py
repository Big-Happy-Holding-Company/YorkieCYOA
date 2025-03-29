
import os
import json
from app import app, db
from models import ImageAnalysis
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def export_character_data():
    """
    Export character data from the image_analysis table to a CSV file.
    Includes only entries with image_type='character' and exports only 
    specified fields.
    """
    output_file = "character_data.csv"
    
    logger.info(f"Starting export of character data to {output_file}")
    
    with app.app_context():
        # Query the database for character entries
        characters = ImageAnalysis.query.filter_by(image_type='character').all()
        
        logger.info(f"Found {len(characters)} character entries")
        
        # Create CSV file with the specified columns
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['id', 'image_url', 'character_name', 'character_traits', 
                          'character_role', 'plot_lines']
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(fieldnames)
            
            # Write data rows
            for char in characters:
                # Convert JSONB fields to strings
                traits = json.dumps(char.character_traits) if char.character_traits else ''
                plots = json.dumps(char.plot_lines) if char.plot_lines else ''
                
                row = [
                    char.id,
                    char.image_url,
                    char.character_name or '',
                    traits,
                    char.character_role or '',
                    plots
                ]
                writer.writerow(row)
        
        logger.info(f"Export completed successfully to {output_file}")
        return output_file

if __name__ == "__main__":
    file_path = export_character_data()
    print(f"Character data exported to {file_path}")
