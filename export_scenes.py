
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

def export_scene_data():
    """
    Export scene data from the image_analysis table to multiple file formats.
    Includes only entries with image_type='scene' and exports only 
    specified fields, excluding character-specific columns.
    """
    csv_file = "scene_data.csv"
    json_file = "scene_data.json"
    xml_file = "scene_data.xml"
    py_file = "scene_data.py"
    
    logger.info(f"Starting export of scene data")
    
    with app.app_context():
        # Query the database for scene entries
        scenes = ImageAnalysis.query.filter_by(image_type='scene').all()
        
        logger.info(f"Found {len(scenes)} scene entries")
        
        # Prepare data structure for all formats
        scene_data_list = []
        
        # Create CSV file with the specified columns
        with open(csv_file, 'w', newline='') as csvfile:
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
                
                # Add to the data structure for other formats
                scene_dict = {
                    'id': scene.id,
                    'image_url': scene.image_url,
                    'image_details': {
                        'width': scene.image_width,
                        'height': scene.image_height,
                        'format': scene.image_format,
                        'size_bytes': scene.image_size_bytes
                    },
                    'scene_type': scene.scene_type or '',
                    'setting': scene.setting or '',
                    'setting_description': scene.setting_description or '',
                    'story_fit': scene.story_fit or '',
                    'dramatic_moments': scene.dramatic_moments or []
                }
                scene_data_list.append(scene_dict)
        
        # Export to JSON
        with open(json_file, 'w') as jsonfile:
            json.dump(scene_data_list, jsonfile, indent=2)
        
        # Export to XML
        root = ET.Element("scenes")
        for scene_dict in scene_data_list:
            scene_elem = ET.SubElement(root, "scene")
            
            # Add simple elements
            ET.SubElement(scene_elem, "id").text = str(scene_dict['id'])
            ET.SubElement(scene_elem, "image_url").text = scene_dict['image_url']
            ET.SubElement(scene_elem, "scene_type").text = scene_dict['scene_type']
            ET.SubElement(scene_elem, "setting").text = scene_dict['setting']
            ET.SubElement(scene_elem, "setting_description").text = scene_dict['setting_description']
            ET.SubElement(scene_elem, "story_fit").text = scene_dict['story_fit']
            
            # Add image details
            img_details = ET.SubElement(scene_elem, "image_details")
            ET.SubElement(img_details, "width").text = str(scene_dict['image_details']['width'])
            ET.SubElement(img_details, "height").text = str(scene_dict['image_details']['height'])
            ET.SubElement(img_details, "format").text = str(scene_dict['image_details']['format'])
            ET.SubElement(img_details, "size_bytes").text = str(scene_dict['image_details']['size_bytes'])
            
            # Add dramatic moments
            moments_elem = ET.SubElement(scene_elem, "dramatic_moments")
            for moment in scene_dict['dramatic_moments']:
                ET.SubElement(moments_elem, "moment").text = str(moment)
        
        # Format XML with pretty print
        xml_str = ET.tostring(root, encoding='utf-8')
        dom = xml.dom.minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="  ")
        
        with open(xml_file, 'w') as xmlfile:
            xmlfile.write(pretty_xml)
        
        # Export to Python file
        with open(py_file, 'w') as pyfile:
            pyfile.write("# Scene data exported from database\n\n")
            pyfile.write("scene_data = [\n")
            
            for scene_dict in scene_data_list:
                pyfile.write("    {\n")
                pyfile.write(f"        'id': {scene_dict['id']},\n")
                pyfile.write(f"        'image_url': '{scene_dict['image_url']}',\n")
                pyfile.write(f"        'scene_type': '{scene_dict['scene_type']}',\n")
                pyfile.write(f"        'setting': '{scene_dict['setting']}',\n")
                pyfile.write(f"        'setting_description': '''{scene_dict['setting_description']}''',\n")
                pyfile.write(f"        'story_fit': '{scene_dict['story_fit']}',\n")
                pyfile.write(f"        'dramatic_moments': {scene_dict['dramatic_moments']},\n")
                pyfile.write("        'image_details': {\n")
                pyfile.write(f"            'width': {scene_dict['image_details']['width']},\n")
                pyfile.write(f"            'height': {scene_dict['image_details']['height']},\n")
                pyfile.write(f"            'format': '{scene_dict['image_details']['format']}',\n")
                pyfile.write(f"            'size_bytes': {scene_dict['image_details']['size_bytes']}\n")
                pyfile.write("        }\n")
                pyfile.write("    },\n")
            
            pyfile.write("]\n")
        
        logger.info(f"Export completed successfully to multiple formats:")
        logger.info(f"- CSV: {csv_file}")
        logger.info(f"- JSON: {json_file}")
        logger.info(f"- XML: {xml_file}")
        logger.info(f"- Python: {py_file}")
        
        return csv_file, json_file, xml_file, py_file

if __name__ == "__main__":
    file_paths = export_scene_data()
    print(f"Scene data exported to multiple formats")
