
import os
import json
import xml.dom.minidom
import xml.etree.ElementTree as ET
from app import app, db
from models import ImageAnalysis
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def export_character_data():
    """
    Export character data from the image_analysis table to multiple file formats.
    Includes only entries with image_type='character' and exports only 
    specified fields.
    """
    csv_file = "character_data.csv"
    json_file = "character_data.json"
    xml_file = "character_data.xml"
    py_file = "character_data.py"
    
    logger.info(f"Starting export of character data")
    
    with app.app_context():
        # Query the database for character entries
        characters = ImageAnalysis.query.filter_by(image_type='character').all()
        
        logger.info(f"Found {len(characters)} character entries")
        
        # Prepare data structure for all formats
        char_data_list = []
        
        # Export to CSV
        with open(csv_file, 'w', newline='') as csvfile:
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
                
                # Add to the data structure for other formats
                char_dict = {
                    'id': char.id,
                    'image_url': char.image_url,
                    'character_name': char.character_name or '',
                    'character_traits': char.character_traits or [],
                    'character_role': char.character_role or '',
                    'plot_lines': char.plot_lines or [],
                    'image_details': {
                        'width': char.image_width,
                        'height': char.image_height,
                        'format': char.image_format,
                        'size_bytes': char.image_size_bytes
                    }
                }
                char_data_list.append(char_dict)
        
        # Export to JSON
        with open(json_file, 'w') as jsonfile:
            json.dump(char_data_list, jsonfile, indent=2)
        
        # Export to XML
        root = ET.Element("characters")
        for char_dict in char_data_list:
            char_elem = ET.SubElement(root, "character")
            
            # Add simple elements
            ET.SubElement(char_elem, "id").text = str(char_dict['id'])
            ET.SubElement(char_elem, "image_url").text = char_dict['image_url']
            ET.SubElement(char_elem, "character_name").text = char_dict['character_name']
            ET.SubElement(char_elem, "character_role").text = char_dict['character_role']
            
            # Add image details
            img_details = ET.SubElement(char_elem, "image_details")
            ET.SubElement(img_details, "width").text = str(char_dict['image_details']['width'])
            ET.SubElement(img_details, "height").text = str(char_dict['image_details']['height'])
            ET.SubElement(img_details, "format").text = str(char_dict['image_details']['format'])
            ET.SubElement(img_details, "size_bytes").text = str(char_dict['image_details']['size_bytes'])
            
            # Add character traits
            traits_elem = ET.SubElement(char_elem, "character_traits")
            for trait in char_dict['character_traits']:
                ET.SubElement(traits_elem, "trait").text = str(trait)
            
            # Add plot lines
            plots_elem = ET.SubElement(char_elem, "plot_lines")
            for plot in char_dict['plot_lines']:
                ET.SubElement(plots_elem, "plot").text = str(plot)
        
        # Format XML with pretty print
        xml_str = ET.tostring(root, encoding='utf-8')
        dom = xml.dom.minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="  ")
        
        with open(xml_file, 'w') as xmlfile:
            xmlfile.write(pretty_xml)
        
        # Export to Python file
        with open(py_file, 'w') as pyfile:
            pyfile.write("# Character data exported from database\n\n")
            pyfile.write("character_data = [\n")
            
            for char_dict in char_data_list:
                pyfile.write("    {\n")
                pyfile.write(f"        'id': {char_dict['id']},\n")
                pyfile.write(f"        'image_url': '{char_dict['image_url']}',\n")
                pyfile.write(f"        'character_name': '{char_dict['character_name']}',\n")
                pyfile.write(f"        'character_traits': {char_dict['character_traits']},\n")
                pyfile.write(f"        'character_role': '{char_dict['character_role']}',\n")
                pyfile.write(f"        'plot_lines': {char_dict['plot_lines']},\n")
                pyfile.write("        'image_details': {\n")
                pyfile.write(f"            'width': {char_dict['image_details']['width']},\n")
                pyfile.write(f"            'height': {char_dict['image_details']['height']},\n")
                pyfile.write(f"            'format': '{char_dict['image_details']['format']}',\n")
                pyfile.write(f"            'size_bytes': {char_dict['image_details']['size_bytes']}\n")
                pyfile.write("        }\n")
                pyfile.write("    },\n")
            
            pyfile.write("]\n")
        
        logger.info(f"Export completed successfully to multiple formats:")
        logger.info(f"- CSV: {csv_file}")
        logger.info(f"- JSON: {json_file}")
        logger.info(f"- XML: {xml_file}")
        logger.info(f"- Python: {py_file}")
        
        return csv_file

if __name__ == "__main__":
    file_path = export_character_data()
    print(f"Character data exported to multiple formats")
