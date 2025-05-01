import streamlit as st
from pathlib import Path
import logging
from quiz.generator import generate_quiz
from data.loader import load_items
from config.settings import DATA_FILE

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_session_state():
    """Initialize session state variables"""
    if 'app_state' not in st.session_state:
        st.session_state.app_state = 'main_menu'
        st.session_state.current_quiz = None
        st.session_state.score = 0
        st.session_state.submitted = False
        st.session_state.selected_answer = None
        st.session_state.selected_type = None
        
        # Initialize high score
        if not hasattr(st.session_state, 'high_score'):
            try:
                with open('high_score.txt', 'r') as f:
                    st.session_state.high_score = int(f.read().strip())
            except:
                st.session_state.high_score = 0
        
        # Load items
        logger.debug(f"Loading items from: {DATA_FILE}")
        try:
            items = load_items(DATA_FILE)
            logger.debug(f"Loaded items type: {type(items)}")
            logger.debug(f"Loaded items length: {len(items) if isinstance(items, list) else 'not a list'}")
            if items and isinstance(items, list):
                logger.debug(f"Successfully loaded {len(items)} items")
                # Store items as a list in session state
                st.session_state.items = list(items)  # Ensure it's a list
                # Get unique item types
                st.session_state.item_types = sorted(list(set(item['type'] for item in items if 'type' in item)))
                logger.debug(f"Available item types: {st.session_state.item_types}")
            else:
                logger.error("Failed to load items or items is not a list")
                st.session_state.items = []
                st.session_state.item_types = []
        except Exception as e:
            logger.error(f"Error loading items: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            st.session_state.items = []
            st.session_state.item_types = []

def update_high_score(score):
    """Update the high score if the current score is higher"""
    if score > st.session_state.high_score:
        st.session_state.high_score = score
        try:
            with open('high_score.txt', 'w') as f:
                f.write(str(score))
        except Exception as e:
            logger.error(f"Error saving high score: {e}")

def reset_high_score():
    """Reset the high score to 0"""
    st.session_state.high_score = 0
    try:
        with open('high_score.txt', 'w') as f:
            f.write('0')
    except Exception as e:
        logger.error(f"Error resetting high score: {e}")

def start_quiz():
    """Start a new quiz"""
    st.session_state.app_state = 'type_selection'
    st.session_state.score = 0
    st.session_state.current_quiz = None
    st.session_state.submitted = False
    st.session_state.selected_answer = None

def back_to_menu():
    """Return to main menu"""
    st.session_state.app_state = 'main_menu'
    st.session_state.current_quiz = None
    st.session_state.submitted = False
    st.session_state.selected_answer = None

def next_question():
    """Load next question"""
    st.session_state.current_quiz = None
    st.session_state.submitted = False
    st.session_state.selected_answer = None

def show_type_selection():
    """Display the item type selection state"""
    st.markdown(
        '<div style="text-align: center;">'
        '<h2>Select Item Type</h2>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Create a grid of buttons using columns
    col1, col2 = st.columns(2)
    
    # Add "Random" button first
    with col1:
        if st.button("Random", key="random_type", use_container_width=True):
            st.session_state.selected_type = None
            st.session_state.app_state = 'question'
            st.rerun()
    
    # Add "Back" button
    with col2:
        if st.button("Back to Menu", key="back_to_menu", use_container_width=True):
            st.session_state.app_state = 'main_menu'
            st.rerun()
    
    st.write("")  # Add some spacing
    
    # Create buttons for each item type
    for i in range(0, len(st.session_state.item_types), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(st.session_state.item_types[i], key=f"type_{i}", use_container_width=True):
                st.session_state.selected_type = st.session_state.item_types[i]
                st.session_state.app_state = 'question'
                st.rerun()
        
        # Add second button if it exists
        if i + 1 < len(st.session_state.item_types):
            with col2:
                if st.button(st.session_state.item_types[i + 1], key=f"type_{i+1}", use_container_width=True):
                    st.session_state.selected_type = st.session_state.item_types[i + 1]
                    st.session_state.app_state = 'question'
                    st.rerun()

def show_main_menu():
    """Display the main menu state"""
    # Show banner
    try:
        banner_path = Path("images/banner.png").absolute()
        logger.debug(f"Attempting to load banner from: {banner_path}")
        if banner_path.exists():
            logger.debug("Banner file exists, loading image")
            st.image(str(banner_path), width='100%')
        else:
            logger.warning(f"Banner not found at path: {banner_path}")
    except Exception as e:
        logger.error(f"Could not load banner image: {e}")
        logger.error(f"Current working directory: {Path.cwd()}")
    
    # Add some spacing
    st.write("")
    
    # Show high score
    st.markdown(
        '<div style="text-align: center;">'
        f'<h2>High Score: {st.session_state.high_score}</h2>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Add spacing between high score and buttons
    st.write("")
    st.write("")
    
    # Create columns for buttons with more space
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Center the buttons and add margin
        st.markdown(
            '<style>div.stButton > button { width: 100%; margin: 10px 0; }</style>',
            unsafe_allow_html=True
        )
        
        # Start Quiz button
        if st.button("Start Quiz", key="start_quiz", on_click=start_quiz):
            pass
        
        # Reset High Score button
        if st.button("Reset High Score", key="reset_score", on_click=reset_high_score):
            pass

def show_question():
    """Display the question state"""
    # Generate new quiz if needed
    if st.session_state.current_quiz is None:
        logger.debug("No current quiz, generating new one")
        
        # Get items from session state and ensure it's a list
        items = st.session_state.get('items', [])
        if not isinstance(items, list):
            logger.error(f"Items is not a list: {type(items)}")
            st.error("Invalid items data. Please refresh the page.")
            return
            
        # Filter items by type if selected
        if st.session_state.selected_type:
            logger.debug(f"Filtering items by type: {st.session_state.selected_type}")
            filtered_items = []
            for item in items:
                if isinstance(item, dict) and item.get('type') == st.session_state.selected_type:
                    filtered_items.append(item)
            items = filtered_items
            logger.debug(f"Found {len(items)} items of type {st.session_state.selected_type}")
            
        if not items:
            logger.error(f"No items available for type: {st.session_state.selected_type}")
            st.error(f"No items available for type: {st.session_state.selected_type}")
            st.session_state.app_state = 'type_selection'
            return
            
        try:
            logger.debug("Attempting to generate quiz")
            st.session_state.current_quiz = generate_quiz(items)
            logger.debug("Quiz generated successfully")
        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}")
            st.error("Failed to generate quiz. Please try again.")
            return
    
    quiz = st.session_state.current_quiz
    logger.debug(f"Current quiz: {quiz}")
    
    # Display stats at the top
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div style="text-align: center; padding: 10px; background-color: #262730; border-radius: 5px;">'
            f'<div style="font-size: 1.2em; color: #FFFFFF;">Score</div>'
            f'<div style="font-size: 1.5em; color: #4CAF50;">{st.session_state.score}</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div style="text-align: center; padding: 10px; background-color: #262730; border-radius: 5px;">'
            f'<div style="font-size: 1.2em; color: #FFFFFF;">High Score</div>'
            f'<div style="font-size: 1.5em; color: #FFC107;">{st.session_state.high_score}</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col3:
        category = st.session_state.selected_type or "Random"
        st.markdown(
            f'<div style="text-align: center; padding: 10px; background-color: #262730; border-radius: 5px;">'
            f'<div style="font-size: 1.2em; color: #FFFFFF;">Category</div>'
            f'<div style="font-size: 1.5em; color: #2196F3;">{category}</div>'
            '</div>',
            unsafe_allow_html=True
        )
    
    # Add some spacing after the stats
    st.write("")
    
    # Question text
    logger.debug(f"Displaying question: {quiz['question']}")
    st.markdown(f"### {quiz['question']}")
    
    # Handle answer submission
    if not st.session_state.submitted:
        logger.debug("Displaying answer options")
        # Radio buttons for options
        answer = st.radio("Choose your answer:", quiz['options'], key="answer_radio", label_visibility="collapsed")
        st.session_state.selected_answer = answer
        logger.debug(f"Selected answer: {answer}")
        
        # Show initial image
        if quiz.get('image'):
            st.image(quiz['image'], width=400)
        
        # Submit button
        if st.button("Submit Answer", key="submit"):
            logger.debug("Submit button clicked")
            st.session_state.submitted = True
            st.rerun()  # Force a rerun to remove radio buttons
            
    # Show results after submission
    if st.session_state.submitted:
        logger.debug("Showing results after submission")
        
        # Get selected answer info
        selected_idx = quiz['options'].index(st.session_state.selected_answer)
        selected_letter = chr(ord('A') + selected_idx)
        logger.debug(f"Selected letter: {selected_letter}, Correct answer: {quiz['correct']}")
        
        is_wrong_answer = selected_letter != quiz['correct']
        
        # Display colored options first
        for i, option in enumerate(quiz['options']):
            letter = chr(ord('A') + i)
            if letter == quiz['correct']:
                st.markdown(f'<div style="color: #4CAF50; padding: 5px;">✓ {option}</div>', 
                          unsafe_allow_html=True)
            elif is_wrong_answer and option == st.session_state.selected_answer:
                st.markdown(f'<div style="color: #F44336; padding: 5px;">✗ {option}</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="color: #9E9E9E; padding: 5px;">○ {option}</div>', 
                          unsafe_allow_html=True)
        
        # Display item image or you_died image
        if quiz.get('image'):
            logger.debug(f"Processing image: {quiz.get('image')}")
            if is_wrong_answer:
                # Show you_died image for wrong answers
                try:
                    you_died_path = Path("images/you_died.png").absolute()
                    logger.debug(f"Looking for you_died image at: {you_died_path}")
                    if you_died_path.exists():
                        logger.debug("You died image found, displaying")
                        st.image(str(you_died_path), width='100%')
                    else:
                        logger.warning(f"You died image not found at path: {you_died_path}")
                except Exception as e:
                    logger.error(f"Could not load you_died.png: {e}")
                    logger.error(f"Current working directory: {Path.cwd()}")
            else:
                # Show item image
                logger.debug("Showing item image")
                st.image(quiz['image'], width=400)
        
        # Show description
        if quiz.get('description'):
            st.info(f'"{quiz["description"]}"')
        
        # Show navigation buttons based on answer at the bottom
        if not is_wrong_answer:
            st.success("Correct! 🎉")
            st.button("Next Question", key="next", on_click=next_question)
            # Update score and high score
            st.session_state.score += 1
            update_high_score(st.session_state.score)
        else:
            st.button("Back to Menu", key="menu", on_click=back_to_menu)

def main():
    # Initialize session state
    init_session_state()
    
    # Set page config
    st.set_page_config(
        page_title="Elden Ring Quiz",
        page_icon="🎮",
        layout="centered"
    )
    
    # Show appropriate state
    if st.session_state.app_state == 'main_menu':
        show_main_menu()
    elif st.session_state.app_state == 'type_selection':
        show_type_selection()
    else:
        show_question()

if __name__ == "__main__":
    main() 