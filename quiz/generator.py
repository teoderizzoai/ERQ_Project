# quiz/generator.py
import json
import random
import logging
import time
import groq
from config.settings import API_KEY
from text_processor import get_context_for_query

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = groq.Groq(api_key=API_KEY)

def select_random_item(items):
    """Select a random item from the database"""
    logger.debug(f"Selecting random item from {len(items) if isinstance(items, list) else 'non-list'} items")
    
    if not isinstance(items, list):
        logger.error(f"Expected list, got {type(items)}")
        raise ValueError("Invalid data structure: expected list of items")
    
    if not items:
        logger.error("No items found in the data")
        raise ValueError("No items found in the data")
    
    # Filter out items without required fields, but be more lenient
    valid_items = []
    for item in items:
        if isinstance(item, dict):
            # Check if item has at least name and either description or quote
            if item.get('name') and (item.get('description') or item.get('quote')):
                # Use quote as description if description is empty
                if not item.get('description') and item.get('quote'):
                    item['description'] = item['quote']
                valid_items.append(item)
    
    if not valid_items:
        logger.error("No valid items found with required fields")
        logger.debug(f"Total items checked: {len(items)}")
        logger.debug("Sample item structure: " + str(items[0] if items else "No items"))
        raise ValueError("No valid items found with required fields")
    
    item = random.choice(valid_items)
    logger.debug(f"Selected item: {item.get('name', 'Unknown')}")
    
    # Create a clean copy with default values for missing fields
    return {
        'name': item.get('name', ''),
        'type': item.get('type', 'Unknown'),
        'description': item.get('description', ''),
        'category': item.get('category', ''),
        'image': item.get('image', ''),
        'location': item.get('location', ''),
        'drops': item.get('drops', []),
        'quote': item.get('quote', '')
    }

def call_groq_api(prompt, max_retries=3, initial_delay=2, max_delay=30, **kwargs):
    """Call the Groq API with improved retry logic for rate limits
    
    Args:
        prompt (str): The prompt to send to the API
        max_retries (int): Maximum number of retry attempts
        initial_delay (int): Initial delay in seconds before retrying
        max_delay (int): Maximum delay between retries
        **kwargs: Additional parameters to pass to the API call
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response
            
        except Exception as e:
            last_error = e
            if "429" in str(e):
                # Calculate delay with exponential backoff, but cap it
                delay = min(initial_delay * (2 ** attempt), max_delay)
                logger.warning(f"Rate limit hit (attempt {attempt + 1}/{max_retries}), retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                # For non-rate-limit errors, wait a bit but don't retry as much
                if attempt < 2:  # Only retry twice for non-rate-limit errors
                    delay = min(initial_delay * (1.5 ** attempt), max_delay)
                    logger.warning(f"API error (attempt {attempt + 1}/3), retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    raise
    
    # If we've exhausted all retries, raise the last error
    raise Exception(f"Failed after {max_retries} retries. Last error: {str(last_error)}")

def extract_relevant_dialogue(question, full_dialogue):
    """Extract relevant parts of NPC dialogue based on the question"""
    try:
        # Clean up the dialogue first
        cleaned_dialogue = ' '.join(
            part.split('] ')[1] if '] ' in part else part 
            for part in full_dialogue.split('Section')
        )
        cleaned_dialogue = ' '.join(
            part.split('] ')[1] if '] ' in part else part 
            for part in cleaned_dialogue.split('[')
        )
        
        # Split into individual lines
        dialogue_lines = [line.strip() for line in cleaned_dialogue.split('.') if line.strip()]
        
        # Process dialogue in chunks of 5 lines
        chunk_size = 5
        relevant_parts = []
        
        for i in range(0, len(dialogue_lines), chunk_size):
            chunk = dialogue_lines[i:i + chunk_size]
            
            prompt = f"""
Given this question about an Elden Ring NPC:
{question}

And this part of the NPC's dialogue:
{' '.join(chunk)}

Extract any sentences from this dialogue chunk that are relevant to answering the question.
Focus on the parts that contain the information needed to answer correctly.
If no part is relevant, respond with "NONE".
Format your response as just the relevant sentences, or "NONE" if none are relevant.
"""
            
            try:
                response = call_groq_api(prompt, max_tokens=150, temperature=0.3)
                if hasattr(response.choices[0].message, 'content'):
                    result = response.choices[0].message.content.strip()
                    if result.lower() != "none":
                        relevant_parts.append(result)
            except Exception as e:
                logger.error(f"Error processing dialogue chunk: {str(e)}")
                continue
        
        # Combine all relevant parts
        if relevant_parts:
            return ' '.join(relevant_parts)
        else:
            # If no relevant parts found, return the first few lines
            return '. '.join(dialogue_lines[:3]) + '.'
            
    except Exception as e:
        logger.error(f"Error extracting relevant dialogue: {str(e)}")
        return '. '.join(dialogue_lines[:3]) + '.'  # Fallback to first few lines if there's an error

def generate_quiz(items):
    """Generate a quiz question about an Elden Ring item"""
    try:
        logger.debug("Starting quiz generation")
        # Log the items we received
        logger.debug(f"Items type: {type(items)}")
        logger.debug(f"Items length: {len(items) if isinstance(items, list) else 'not a list'}")
        if isinstance(items, list) and len(items) > 0:
            logger.debug(f"First item example: {items[0].get('name', 'Unknown')}")
        
        # Select a random item for the quiz
        quiz_item = select_random_item(items)
        logger.debug(f"Selected quiz item: {quiz_item['name']}")
        
        # Get the description, falling back to regular description if quote is empty
        description = quiz_item.get('description', '')
        if quiz_item.get('type', '').lower() == 'npcs' and quiz_item.get('quote'):
            description = quiz_item['quote']
            
        # Get additional context from lore file for question generation
        additional_context = ""
        try:
            additional_context = get_context_for_query(quiz_item['name'])
        except Exception as e:
            logger.warning(f"Failed to get additional context: {e}")
        
        # Generate quiz with retry logic
        max_quiz_attempts = 2  # Limit the number of quiz generation attempts
        for quiz_attempt in range(max_quiz_attempts):
            try:
                prompt = f"""
Generate a multiple-choice quiz question about this Elden Ring item:

Name: {quiz_item['name']}
Description: {description}

Additional Context:
{additional_context}

Create a challenging but fair question about the lore surrounding this item ({quiz_item['name']}).
the description is important.
For example, if the item is a weapon, the question should be about the weapon, the purpose of who wielded it, what was the weapon used for, etc.

You MUST follow these rules EXACTLY:

1. Write the question directly without any prefix
2. ALWAYS provide EXACTLY 4 options labeled A, B, C, and D
3. Each option MUST start with the letter and parenthesis (A), B), C), or D))
4. Each option must be a complete sentence
5. Only one option can be correct
6. All options must sound plausible
7. Each option MUST be on its own line
8. The answer must be just the letter (A, B, C, or D)

Your response MUST follow this EXACT format:

[Question on one line]
A) [First option]
B) [Second option]
C) [Third option]
D) [Fourth option]
Answer: [Letter]

Example:

What insights does the item's description offer?

or (How does the description shape our understanding of the item?)

or (What does the item's description reveal about its purpose or value?)

A) It represents the character's journey of self-discovery
B) It symbolizes the eternal struggle between light and dark
C) It reflects the character's tragic past and lost memories
D) It signifies the character's role as a guardian of ancient knowledge
Answer: D

IMPORTANT: You MUST include ALL FOUR options A, B, C, and D. Do not skip any options. Don't phrase the question as: What is the significance of
"""
                
                response = call_groq_api(prompt, max_tokens=300, temperature=0.7)
                
                if not response or not hasattr(response.choices[0].message, 'content'):
                    raise ValueError("Invalid API response")
                    
                quiz_text = response.choices[0].message.content.strip()
                logger.debug(f"Received quiz text: {quiz_text[:100]}...")
                
                # Parse the quiz
                question, options, correct = parse_quiz(quiz_text)
                
                # Verify we have exactly 4 options
                if len(options) != 4:
                    raise ValueError(f"Expected 4 options, found {len(options)}")
                
                # If we get here, we have a valid quiz
                break
                
            except Exception as e:
                logger.warning(f"Quiz generation attempt {quiz_attempt + 1} failed: {str(e)}")
                if quiz_attempt == max_quiz_attempts - 1:  # Last attempt
                    raise Exception(f"Failed to generate quiz after {max_quiz_attempts} attempts: {str(e)}")
                time.sleep(2)  # Wait a bit before retrying
                continue

        # For NPCs with descriptions, try to extract relevant dialogue
        if quiz_item.get('type', '').lower() == 'npcs' and quiz_item.get('description'):
            try:
                focused_description = extract_relevant_dialogue(question, quiz_item['description'])
            except Exception as e:
                logger.warning(f"Failed to extract relevant dialogue: {e}")
                focused_description = description
        else:
            focused_description = description
        
        return {
            'question': question,
            'options': options,
            'correct': correct,
            'image': quiz_item.get('image', ''),
            'description': description  # Only return the original description without additional context
        }
            
    except Exception as e:
        logger.error(f"Quiz generation failed: {str(e)}")
        logger.error(f"Full error: {repr(e)}")
        raise Exception(f"Quiz generation failed: {str(e)} (type: {type(e).__name__})")

def parse_quiz(quiz_text):
    """Parse the quiz text into question, options, and correct answer"""
    try:
        if not quiz_text:
            raise ValueError("Empty quiz text")
            
        # Clean up the text and split into lines
        lines = [line.strip() for line in quiz_text.splitlines() if line.strip()]
        
        # Extract question
        question = None
        for line in lines:
            if line.lower().startswith("question:"):
                question = line.split(":", 1)[1].strip()
                break
            elif not any(line.startswith(f"{letter})") for letter in "ABCD"):
                question = line.strip()
                # Remove "Here is the quiz question:" if present
                if question.lower().startswith("here is the quiz question:"):
                    question = question.split(":", 1)[1].strip()
                break
        
        if not question:
            raise ValueError("No question found in quiz text")
        
        # Extract options
        options = []
        option_patterns = [f"{letter})" for letter in "ABCD"]
        
        for line in lines:
            for pattern in option_patterns:
                if line.startswith(pattern):
                    option = line[len(pattern):].strip()
                    options.append(option)
                    break
        
        # If we don't have all options, try to find them in any order
        if len(options) < 4:
            remaining_options = set(option_patterns) - {f"{letter})" for letter in "ABCD"[:len(options)]}
            for line in lines:
                for pattern in remaining_options:
                    if line.startswith(pattern):
                        option = line[len(pattern):].strip()
                        options.append(option)
                        remaining_options.remove(pattern)
                        break
        
        if len(options) != 4:
            raise ValueError(f"Expected 4 options, found {len(options)}")
            
        # Extract answer
        correct = None
        for line in lines:
            if line.lower().startswith("answer:"):
                answer_text = line.split(":", 1)[1].strip()
                correct = answer_text[0].upper()
                break
            elif line[0].upper() in "ABCD" and len(line.strip()) == 1:
                correct = line[0].upper()
                break
        
        if not correct or correct not in "ABCD":
            raise ValueError("No valid answer found in quiz text")
            
        return question, options, correct
        
    except Exception as e:
        raise Exception(f"Quiz parsing failed: {str(e)}")

