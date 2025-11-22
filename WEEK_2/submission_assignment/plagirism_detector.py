import heapq
import os
from collections import defaultdict
import string
import re

"""
Plagiarism Detection System Implementation
Uses A* Search Algorithm for Optimal Text Alignment
CS367 - Artificial Intelligence Lab Assignment

State Space Definition:
    - Current position in source document
    - Current position in target document  
    - Type of operation performed to reach this state
"""

# Global variables for document storage
source_document = []
target_document = []


def load_document_content(filepath):
    """
    Reads text content from a file with error handling
    Returns file content as string
    """
    script_directory = os.path.dirname(os.path.abspath(__file__))
    complete_filepath = os.path.join(script_directory, filepath)
    
    try:
        with open(complete_filepath, "r", encoding='utf-8') as file_handle:
            text_content = file_handle.read()
        return text_content
    except FileNotFoundError:
        print(f"Warning: File not found at {complete_filepath}")
        print("Using default sample text for demonstration...")
        
        # Provide sample content based on filename
        if "doc1" in filepath:
            return "Artificial intelligence is transforming modern technology. Machine learning algorithms learn from data patterns. Deep learning networks process complex information efficiently."
        else:
            return "Artificial intelligence is revolutionizing modern technology. Machine learning algorithms discover data patterns. Deep learning networks handle complex information effectively."


def tokenize_into_sentences(text_input):
    """
    Splits input text into individual sentences using regex patterns
    Returns list of normalized sentences
    """
    normalized_text = text_input.lower().strip()
    # Enhanced sentence splitting pattern
    sentence_list = re.split(r'(?<=[.!?])\s+(?=[A-Z]|\w)', normalized_text)
    # Filter empty strings and clean whitespace
    return [sent.strip() for sent in sentence_list if sent.strip()]


def clean_sentence_text(sentence_input):
    """
    Removes punctuation and normalizes sentence text
    Replaces newlines with spaces and removes special characters
    """
    translation_table = str.maketrans("\n\r\t", "   ", string.punctuation)
    cleaned_text = sentence_input.translate(translation_table)
    # Remove extra whitespaces
    return re.sub(r'\s+', ' ', cleaned_text).strip()


def prepare_document_data(file_location):
    """
    Complete document preprocessing pipeline
    1. Load file content
    2. Extract sentences  
    3. Clean and normalize text
    """
    # Step 1: Load document content
    raw_content = load_document_content(file_location)
    
    # Step 2: Split into sentences
    sentence_array = tokenize_into_sentences(raw_content)
    
    # Step 3: Clean each sentence
    print(f"Raw sentences: {sentence_array}")
    processed_sentences = [clean_sentence_text(sent) for sent in sentence_array]
    
    return processed_sentences


class SearchNode:
    """
    Node class for A* search algorithm
    Stores state information and cost calculations
    """
    def __init__(self, current_state, parent_node=None, path_cost=0, heuristic_cost=0, weight_g=1, weight_h=1):
        self.current_state = current_state
        self.parent_node = parent_node
        self.path_cost = path_cost  # g(n) - actual cost from start
        self.heuristic_cost = heuristic_cost  # h(n) - estimated cost to goal
        self.total_cost = weight_g * path_cost + weight_h * heuristic_cost  # f(n) = g(n) + h(n)

    def __lt__(self, other_node):
        """Comparison operator for priority queue"""
        return self.total_cost < other_node.total_cost


def calculate_character_difference(source_idx=None, target_idx=None):
    """
    Computes character-level differences between sentences
    
    Algorithm:
    1. Count character frequencies in both sentences
    2. Calculate mismatched characters
    3. Add length difference penalty if source is longer
    """
    source_sentence = source_document[source_idx] if source_idx is not None else ""
    target_sentence = target_document[target_idx] if target_idx is not None else ""

    # Convert to character arrays
    source_chars = list(source_sentence)
    target_chars = list(target_sentence)

    # Character frequency counting
    target_char_count = defaultdict(int)
    source_char_freq = defaultdict(int)

    # Build frequency map for source sentence
    for character in source_chars:
        source_char_freq[character] += 1

    # Calculate differences
    mismatch_penalty = 0
    if len(source_chars) > len(target_chars):
        mismatch_penalty += len(source_chars) - len(target_chars)

    # Count unmatched characters in target
    for character in target_chars:
        if source_char_freq[character] == 0:
            target_char_count[character] += 1
            mismatch_penalty += 1
        else:
            source_char_freq[character] -= 1

    return mismatch_penalty


def estimate_remaining_cost(current_state, goal_state):
    """
    Heuristic function for A* search
    Estimates minimum cost to reach goal from current state
    """
    current_source_pos, current_target_pos, _ = list(current_state)
    goal_source_len, goal_target_len, _ = list(goal_state)

    remaining_cost = 0

    # Process all remaining positions
    while current_source_pos <= goal_source_len or current_target_pos <= goal_target_len:
        if current_source_pos <= goal_source_len and current_target_pos <= goal_target_len:
            remaining_cost += calculate_character_difference(current_source_pos, current_target_pos)
        elif current_source_pos <= goal_source_len and current_target_pos > goal_target_len:
            remaining_cost += calculate_character_difference(current_source_pos, None)
        elif current_source_pos > goal_source_len and current_target_pos <= goal_target_len:
            remaining_cost += calculate_character_difference(None, current_target_pos)

        current_target_pos += 1
        current_source_pos += 1

    return remaining_cost


def compute_levenshtein_distance(string1, string2):
    """
    Dynamic programming implementation of edit distance
    Calculates minimum operations needed to transform string1 to string2
    """
    # Handle edge cases
    first_string = string1
    second_string = string2

    # Get string lengths
    length1 = len(first_string)
    length2 = len(second_string)

    # Create DP matrix
    distance_matrix = [[0] * (length2 + 1) for _ in range(length1 + 1)]

    # Initialize base cases
    for row in range(1, length1 + 1):
        distance_matrix[row][0] = row  # Deletion operations
    for col in range(1, length2 + 1):
        distance_matrix[0][col] = col  # Insertion operations

    # Fill the matrix using dynamic programming
    for row in range(1, length1 + 1):
        for col in range(1, length2 + 1):
            if first_string[row - 1] == second_string[col - 1]:
                distance_matrix[row][col] = distance_matrix[row - 1][col - 1]  # No operation needed
            else:
                distance_matrix[row][col] = min(
                    distance_matrix[row - 1][col] + 1,      # Deletion
                    distance_matrix[row][col - 1] + 1,      # Insertion
                    distance_matrix[row - 1][col - 1] + 1,  # Substitution
                )

    return distance_matrix[length1][length2]


def calculate_operation_cost(state_info, target_state):
    """
    Determines the cost of performing a specific operation
    Based on the type of move and current state positions
    """
    source_position = list(state_info)[0]
    target_position = list(state_info)[1]
    operation_type = list(state_info)[2]
    operation_cost = 0

    if operation_type == 0:  # Alignment operation
        source_text = source_document[source_position - 1]
        target_text = target_document[target_position - 1]
        operation_cost = compute_levenshtein_distance(source_text, target_text)
    elif operation_type == 1:  # Skip target sentence (insertion)
        target_text = target_document[target_position - 1]
        operation_cost = len(target_text)
    elif operation_type == 2:  # Skip source sentence (deletion)
        source_text = source_document[source_position - 1]
        operation_cost = len(source_text)

    return operation_cost


def generate_successor_states(search_node):
    """
    Generates all possible successor states from current node
    
    Available operations:
    0: Align sentences from both documents
    1: Skip sentence in target document (insertion)
    2: Skip sentence in source document (deletion)
    """
    possible_moves = [(1, 1, 0), (0, 1, 1), (1, 0, 2)]
    current_state_info = list(search_node.current_state)
    successor_list = []
    
    for move_vector in possible_moves:
        move_deltas = list(move_vector)
        new_state_tuple = (
            current_state_info[0] + move_deltas[0], 
            current_state_info[1] + move_deltas[1], 
            move_deltas[2]
        )
        successor_node = SearchNode(new_state_tuple, search_node)
        successor_list.append(successor_node)

    return successor_list


def execute_astar_search(initial_state, final_state):
    """
    Main A* search algorithm implementation
    Finds optimal alignment path between two documents
    """
    start_node = SearchNode(initial_state)
    goal_node = SearchNode(final_state)
    
    # Priority queue for open list
    open_list = []
    heapq.heappush(open_list, (start_node.total_cost, start_node))
    
    # Set for tracking visited states
    explored_states = set()
    node_exploration_count = 0

    while open_list:
        _, current_node = heapq.heappop(open_list)
        
        # Skip if already explored
        if tuple(current_node.current_state) in explored_states:
            continue
            
        explored_states.add(tuple(current_node.current_state))
        node_exploration_count += 1

        # Check if goal reached
        if (list(current_node.current_state)[0] == list(goal_node.current_state)[0] + 1 and 
            list(current_node.current_state)[1] == list(goal_node.current_state)[1] + 1):
            
            # Reconstruct solution path
            solution_path = []
            node_pointer = current_node
            while node_pointer:
                solution_path.append(node_pointer.current_state)
                node_pointer = node_pointer.parent_node
            
            print(f"Search completed. Total nodes explored: {node_exploration_count}")
            return solution_path

        # Generate and evaluate successors
        for successor in generate_successor_states(current_node):
            # Check boundary conditions
            if (list(successor.current_state)[0] <= list(goal_node.current_state)[0] + 1 and 
                list(successor.current_state)[1] <= list(goal_node.current_state)[1] + 1):
                
                # Calculate costs
                successor.path_cost = current_node.path_cost + calculate_operation_cost(successor.current_state, goal_node.current_state)
                successor.heuristic_cost = estimate_remaining_cost(successor.current_state, goal_node.current_state)
                successor.total_cost = successor.path_cost + successor.heuristic_cost
                
                heapq.heappush(open_list, (successor.total_cost, successor))

    print(f"No solution found. Total nodes explored: {node_exploration_count}")
    return None


def reconstruct_aligned_document(state_sequence, start_state, end_state):
    """
    Reconstructs the aligned document based on the optimal path
    Creates new document following the alignment decisions
    """
    aligned_document = []
    
    for state in state_sequence:
        # Skip initial state
        if list(state)[0] == list(start_state)[0] and list(state)[1] == list(start_state)[1]:
            continue
            
        operation_type = list(state)[-1]
        
        if operation_type == 0:  # Alignment - use source document
            aligned_document.append(source_document[list(state)[0] - 1])
        elif operation_type == 1:  # Insertion - use target document
            aligned_document.append(target_document[list(state)[1] - 1])
        elif operation_type == 2:  # Deletion - skip
            continue

        # Check if goal reached
        if list(state)[0] == list(end_state)[0] and list(state)[1] == list(end_state)[1]:
            print("Goal state successfully reached")
            
    return aligned_document


def count_words_in_sentence(sentence_text):
    """
    Helper function to count words in a sentence
    """
    word_list = sentence_text.split()
    return len(word_list)



if __name__ == "__main__":
    # Load and process both documents
    source_document = prepare_document_data("test_case_4_doc1.txt")
    target_document = prepare_document_data("test_case_4_doc2.txt")
    
    # Define search parameters
    initial_state = (0, 0, 0)
    final_state = (len(source_document) - 1, len(target_document) - 1, 0)
    print(f"Search goal state: {final_state}")
    
    # Execute A* search algorithm
    optimal_path = execute_astar_search(initial_state, final_state)
    optimal_path.reverse()
    print(f"Optimal alignment path: {optimal_path}")
    
    # Reconstruct aligned document
    aligned_result = reconstruct_aligned_document(optimal_path, initial_state, final_state)
    print(f"Aligned document result: {aligned_result}")
    
    # Display document information
    print(f"Source document length {len(source_document)}: {source_document}")
    print()
    print(f"Target document length {len(target_document)}: {target_document}")
    print()

    # Calculate total word count
    total_word_count = 0
    for sentence_idx in range(len(source_document)):
        total_word_count += count_words_in_sentence(source_document[sentence_idx])

    # Perform plagiarism analysis
    print("PLAGIARISM DETECTION ANALYSIS")
    for target_idx in range(len(target_document)):
        if target_idx < len(aligned_result):
            edit_distance_score = compute_levenshtein_distance(aligned_result[target_idx], target_document[target_idx])
            
            if edit_distance_score >= 0:
                print(f"Comparing aligned sentences:")
                print(f"Aligned text: {aligned_result[target_idx]}")
                print(f"Target text: {target_document[target_idx]}")
                print(f"Edit distance score: {edit_distance_score}")
                
                # Similarity analysis
                max_length = max(len(aligned_result[target_idx]), len(target_document[target_idx]))
                if max_length > 0:
                    similarity_percentage = ((max_length - edit_distance_score) / max_length) * 100
                    print(f"Similarity percentage: {similarity_percentage:.2f}%")
                    
                    if similarity_percentage >= 80:
                        print("STATUS: HIGH SIMILARITY - Potential plagiarism detected!")
                    elif similarity_percentage >= 60:
                        print("STATUS: MODERATE SIMILARITY - Review recommended")
                    else:
                        print("STATUS: LOW SIMILARITY - No plagiarism detected")
                print("-" * 50)

    print(f"Total word count in source document: {total_word_count}")