import json
import re
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def clean_dialogue(text):
    """Clean up dialogue text by removing section markers, names, and formatting"""
    if not text:
        return ""
        
    # Split into sections first
    sections = text.split('Section')
    cleaned_sections = []
    
    for section in sections:
        # Skip empty sections
        if not section.strip():
            continue
            
        # Remove section numbers and IDs
        section = re.sub(r'\d+', '', section)
        section = re.sub(r'\[\d+\]', '', section)
        section = re.sub(r'\[\d+\s+', '', section)
        
        # Remove section names (e.g., "Introduction:", "Quest:", etc.)
        section = re.sub(r'[A-Za-z\s]+:', '', section)
        
        # Remove any remaining brackets and their contents
        section = re.sub(r'\[.*?\]', '', section)
        
        # Remove any remaining special characters used for formatting
        section = re.sub(r'[<>]', '', section)
        
        # Clean up whitespace
        section = ' '.join(section.split())
        
        # Remove any remaining numbers at the start of lines
        section = re.sub(r'^\d+\s*', '', section, flags=re.MULTILINE)
        
        if section.strip():
            cleaned_sections.append(section.strip())
    
    # Join all cleaned sections with a period
    result = '. '.join(cleaned_sections)
    
    # Final cleanup
    result = re.sub(r'\.+', '.', result)  # Replace multiple periods with one
    result = re.sub(r'\s+', ' ', result)  # Replace multiple spaces with one
    
    return result.strip()

def process_db():
    """Process the DB.json file to clean NPC dialogues"""
    try:
        # Load the database
        logger.debug("Loading DB.json")
        with open('data/DB.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Process only NPC items
        npc_items = [item for item in data if item.get('type', '').lower() == 'npcs']
        logger.debug(f"Found {len(npc_items)} NPC items")
        
        # Clean dialogues for each NPC
        for item in npc_items:
            if 'description' in item:
                original = item['description']
                cleaned = clean_dialogue(original)
                item['description'] = cleaned
                logger.debug(f"Cleaned dialogue for {item['name']}")
                logger.debug(f"Original: {original[:100]}...")
                logger.debug(f"Cleaned: {cleaned[:100]}...")
        
        # Save the cleaned data
        logger.debug("Saving cleaned data")
        with open('data/DB_cleaned.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        logger.info("Successfully cleaned and saved NPC dialogues")
        
    except Exception as e:
        logger.error(f"Error processing database: {str(e)}")
        raise

if __name__ == "__main__":
    process_db() 