# data/loader.py
import json
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_items(file_path):
    """Load items from DB.json"""
    try:
        # Convert to absolute path and normalize
        file_path = os.path.abspath(file_path)
        logger.debug(f"Attempting to load items from: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"Data file not found at: {file_path}")
            logger.error(f"Current working directory: {os.getcwd()}")
            raise FileNotFoundError(f"Data file not found at: {file_path}")
            
        # Check file size
        file_size = os.path.getsize(file_path)
        logger.debug(f"File size: {file_size} bytes")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.debug(f"Raw data type: {type(data)}")
            
            if not isinstance(data, list):
                logger.error(f"Invalid data format: expected list, got {type(data)}")
                raise ValueError("Invalid data format: expected list of items")
            
            # Log total number of items
            logger.debug(f"Total items in file: {len(data)}")
            
            # Filter out items without descriptions, but be more lenient
            items = []
            for item in data:
                if isinstance(item, dict):
                    # Check if item has at least name and description
                    if item.get('name') and (item.get('description') or item.get('quote')):
                        # Use quote as description if description is empty
                        if not item.get('description') and item.get('quote'):
                            item['description'] = item['quote']
                        items.append(item)
            
            logger.debug(f"Loaded {len(items)} valid items")
            
            if not items:
                logger.warning("No valid items found in the data file")
                logger.debug("Sample item structure: " + str(data[0] if data else "No items"))
            else:
                logger.debug(f"First item: {json.dumps(items[0], indent=2)}")
            
            return items
            
    except FileNotFoundError as e:
        logger.error(f"Data file not found: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error loading items: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        raise

def get_similar_items(item_name, top_k=5):
    """This function is deprecated and will be removed"""
    return []