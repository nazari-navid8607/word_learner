import random
from typing import List, Tuple, Optional
from database import WordDatabase

class SentenceGenerator:
    def __init__(self, database: WordDatabase):
        """Initialize the sentence generator with a database connection."""
        self.db = database
    
    def generate_sentence(self, max_length: int = 15, min_length: int = 3) -> str:
        """Generate a sentence using Markov chain from learned words."""
        # Get all valid words from database
        valid_words = self.db.get_valid_words()
        
        if not valid_words:
            return "No words learned yet. Please learn some words first!"
        
        # Start with a random word
        current_word = random.choice(valid_words)
        sentence_words = [current_word]
        
        # Generate the rest of the sentence using Markov chain
        for _ in range(max_length - 1):
            # Get possible next words
            next_words = self.db.get_word_sequences(current_word)
            
            if not next_words:
                # If no sequences found, choose a random word
                next_word = random.choice(valid_words)
            else:
                # Choose next word based on frequency
                next_word = self._weighted_choice(next_words)
            
            sentence_words.append(next_word)
            current_word = next_word
            
            # Stop if we have enough words and hit a natural stopping point
            if len(sentence_words) >= min_length and random.random() < 0.3:
                break
        
        # Capitalize first word and add period
        sentence = ' '.join(sentence_words).capitalize() + '.'
        
        return sentence
    
    def _weighted_choice(self, choices: List[Tuple[str, int]]) -> str:
        """Choose a word based on frequency weights."""
        if not choices:
            return ""
        
        words, frequencies = zip(*choices)
        total_frequency = sum(frequencies)
        
        # Create weighted probabilities
        probabilities = [freq / total_frequency for freq in frequencies]
        
        # Choose based on probabilities
        rand = random.random()
        cumulative = 0
        
        for i, prob in enumerate(probabilities):
            cumulative += prob
            if rand <= cumulative:
                return words[i]
        
        # Fallback to last choice
        return words[-1]
    
    def generate_multiple_sentences(self, count: int, max_length: int = 15, min_length: int = 3) -> List[str]:
        """Generate multiple sentences."""
        sentences = []
        for _ in range(count):
            sentence = self.generate_sentence(max_length, min_length)
            sentences.append(sentence)
        return sentences
    
    def generate_sentence_with_seed(self, seed_word: str, max_length: int = 15) -> str:
        """Generate a sentence starting with a specific word."""
        # Check if seed word exists in database
        word_info = self.db.get_word(seed_word)
        if not word_info or not word_info[1]:  # Word doesn't exist or is invalid
            return f"Word '{seed_word}' not found in learned words."
        
        sentence_words = [seed_word]
        current_word = seed_word
        
        # Generate the rest of the sentence
        for _ in range(max_length - 1):
            next_words = self.db.get_word_sequences(current_word)
            
            if not next_words:
                # If no sequences found, choose a random valid word
                valid_words = self.db.get_valid_words()
                if valid_words:
                    next_word = random.choice(valid_words)
                else:
                    break
            else:
                next_word = self._weighted_choice(next_words)
            
            sentence_words.append(next_word)
            current_word = next_word
            
            # Random stopping point
            if random.random() < 0.3:
                break
        
        # Capitalize first word and add period
        sentence = ' '.join(sentence_words).capitalize() + '.'
        
        return sentence
    
    def get_sentence_variations(self, base_sentence: str, count: int = 3) -> List[str]:
        """Generate variations of a base sentence."""
        words = base_sentence.lower().strip('.,!?').split()
        variations = []
        
        for _ in range(count):
            variation_words = []
            current_word = random.choice(words)
            variation_words.append(current_word)
            
            # Generate variation using Markov chain
            for _ in range(len(words)):
                next_words = self.db.get_word_sequences(current_word)
                
                if not next_words:
                    break
                
                next_word = self._weighted_choice(next_words)
                variation_words.append(next_word)
                current_word = next_word
                
                if random.random() < 0.4:
                    break
            
            variation = ' '.join(variation_words).capitalize() + '.'
            variations.append(variation)
        
        return variations
    
    def analyze_sentence_quality(self, sentence: str) -> dict:
        """Analyze the quality of a generated sentence."""
        words = sentence.lower().strip('.,!?').split()
        
        if not words:
            return {
                'word_count': 0,
                'avg_word_length': 0,
                'coherence_score': 0,
                'quality': 'empty'
            }
        
        # Calculate basic metrics
        word_count = len(words)
        avg_word_length = sum(len(word) for word in words) / word_count
        
        # Calculate coherence score based on learned sequences
        coherence_score = 0
        for i in range(len(words) - 1):
            sequences = self.db.get_word_sequences(words[i])
            if sequences:
                # Check if next word appears in sequences
                next_word = words[i + 1]
                for seq_word, freq in sequences:
                    if seq_word == next_word:
                        coherence_score += freq
                        break
        
        # Normalize coherence score
        if word_count > 1:
            coherence_score = coherence_score / (word_count - 1)
        
        # Determine quality
        if coherence_score > 2:
            quality = 'high'
        elif coherence_score > 1:
            quality = 'medium'
        else:
            quality = 'low'
        
        return {
            'word_count': word_count,
            'avg_word_length': round(avg_word_length, 2),
            'coherence_score': round(coherence_score, 2),
            'quality': quality
        }
    
    def get_available_start_words(self) -> List[str]:
        """Get words that can be used to start sentences."""
        valid_words = self.db.get_valid_words()
        start_words = []
        
        for word in valid_words:
            # Check if this word has sequences (can be followed by other words)
            sequences = self.db.get_word_sequences(word)
            if sequences:
                start_words.append(word)
        
        return start_words
    
    def get_sentence_statistics(self) -> dict:
        """Get statistics about sentence generation capabilities."""
        stats = self.db.get_statistics()
        
        # Calculate additional metrics
        valid_words = self.db.get_valid_words()
        start_words = self.get_available_start_words()
        
        return {
            'total_words': stats['total_words'],
            'valid_words': stats['valid_words'],
            'word_sequences': stats['word_sequences'],
            'available_start_words': len(start_words),
            'generation_ready': len(valid_words) > 0 and stats['word_sequences'] > 0
        }
    
    def improve_sentence_generation(self, feedback: str, sentence: str) -> bool:
        """Use feedback to improve future sentence generation."""
        # This is a placeholder for future improvement
        # Could implement reinforcement learning here
        return True
