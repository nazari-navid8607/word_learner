import re
import string
from typing import List, Tuple
from database import WordDatabase

class TextProcessor:
    def __init__(self, database: WordDatabase):
        """Initialize the text processor with a database connection."""
        self.db = database
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text for processing."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation for sentence structure
        # Keep periods, commas, exclamation marks, question marks
        text = re.sub(r'[^\w\s.,!?]', '', text)
        
        return text.strip()
    
    def extract_words(self, text: str) -> List[str]:
        """Extract individual words from text."""
        cleaned_text = self.clean_text(text)
        
        # Split by whitespace and filter out empty strings
        words = [word.strip() for word in cleaned_text.split() if word.strip()]
        
        # Remove punctuation from individual words
        words = [word.strip(string.punctuation) for word in words]
        
        # Filter out empty strings and very short words (less than 2 characters)
        words = [word for word in words if len(word) >= 2]
        
        return words
    
    def extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text."""
        cleaned_text = self.clean_text(text)
        
        # Split by sentence-ending punctuation
        sentences = re.split(r'[.!?]+', cleaned_text)
        
        # Clean and filter sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def extract_word_sequences(self, text: str, n: int = 2) -> List[Tuple[str, ...]]:
        """Extract n-gram sequences from text."""
        words = self.extract_words(text)
        sequences = []
        
        for i in range(len(words) - n + 1):
            sequence = tuple(words[i:i + n])
            sequences.append(sequence)
        
        return sequences
    
    def learn_from_text(self, text: str) -> dict:
        """Process text and learn words and sequences."""
        # Store the training text
        self.db.add_training_text(text)
        
        # Extract words and sequences
        words = self.extract_words(text)
        sentences = self.extract_sentences(text)
        bigrams = self.extract_word_sequences(text, 2)
        trigrams = self.extract_word_sequences(text, 3)
        
        # Learn individual words (assume all words from text are valid)
        learned_words = set()
        for word in words:
            if len(word) >= 2:  # Only learn words with 2+ characters
                self.db.add_word(word, True, 'text_learning')
                learned_words.add(word)
        
        # Learn word sequences for Markov chain
        learned_sequences = 0
        for word1, word2 in bigrams:
            if len(word1) >= 2 and len(word2) >= 2:
                self.db.add_word_sequence(word1, word2)
                learned_sequences += 1
        
        # Also learn trigrams for better sentence generation
        for word1, word2, word3 in trigrams:
            if len(word1) >= 2 and len(word2) >= 2 and len(word3) >= 2:
                # Store as two bigrams: word1->word2 and word2->word3
                self.db.add_word_sequence(word1, word2)
                self.db.add_word_sequence(word2, word3)
                learned_sequences += 1
        
        return {
            'words_learned': len(learned_words),
            'sentences_processed': len(sentences),
            'bigrams_learned': len(bigrams),
            'trigrams_learned': len(trigrams),
            'sequences_stored': learned_sequences,
            'unique_words': list(learned_words)
        }
    
    def get_word_frequency(self, text: str) -> dict:
        """Get frequency of words in text."""
        words = self.extract_words(text)
        frequency = {}
        
        for word in words:
            frequency[word] = frequency.get(word, 0) + 1
        
        return frequency
    
    def get_common_words(self, text: str, min_frequency: int = 2) -> List[Tuple[str, int]]:
        """Get words that appear frequently in text."""
        frequency = self.get_word_frequency(text)
        common_words = [(word, freq) for word, freq in frequency.items() 
                       if freq >= min_frequency]
        
        # Sort by frequency (descending)
        common_words.sort(key=lambda x: x[1], reverse=True)
        
        return common_words
    
    def analyze_text_complexity(self, text: str) -> dict:
        """Analyze the complexity of the input text."""
        words = self.extract_words(text)
        sentences = self.extract_sentences(text)
        
        if not words:
            return {
                'word_count': 0,
                'sentence_count': 0,
                'avg_words_per_sentence': 0,
                'avg_word_length': 0,
                'unique_words': 0,
                'complexity': 'empty'
            }
        
        # Calculate metrics
        word_count = len(words)
        sentence_count = len(sentences)
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        avg_word_length = sum(len(word) for word in words) / word_count
        unique_words = len(set(words))
        
        # Determine complexity
        if avg_word_length < 4 and avg_words_per_sentence < 8:
            complexity = 'simple'
        elif avg_word_length < 6 and avg_words_per_sentence < 15:
            complexity = 'medium'
        else:
            complexity = 'complex'
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'avg_word_length': round(avg_word_length, 2),
            'unique_words': unique_words,
            'complexity': complexity
        }
    
    def validate_word(self, word: str) -> bool:
        """Check if a word is valid (basic validation)."""
        if not word or len(word) < 2:
            return False
        
        # Check if word contains only letters
        if not word.isalpha():
            return False
        
        # Check if word is not all the same character
        if len(set(word)) == 1:
            return False
        
        return True
    
    def get_learning_progress(self) -> dict:
        """Get the current learning progress from the database."""
        stats = self.db.get_statistics()
        return stats
