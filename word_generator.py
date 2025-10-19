import random
import string
from typing import List

class WordGenerator:
    def __init__(self):
        """Initialize the word generator with English letter patterns."""
        # Vowels and consonants for more realistic word generation
        self.vowels = 'aeiou'
        self.consonants = 'bcdfghjklmnpqrstvwxyz'
        self.all_letters = string.ascii_lowercase
        
        # Common English letter patterns
        self.common_patterns = [
            'CVC',  # Consonant-Vowel-Consonant
            'VC',   # Vowel-Consonant
            'CV',   # Consonant-Vowel
            'CVCV', # Consonant-Vowel-Consonant-Vowel
            'VCV',  # Vowel-Consonant-Vowel
            'CVCVC', # Longer pattern
            'VCVC', # Vowel-Consonant-Vowel-Consonant
        ]
    
    def generate_random_word(self, min_length: int = 3, max_length: int = 8) -> str:
        """Generate a random word with English-like patterns."""
        length = random.randint(min_length, max_length)
        
        # Choose a pattern or create a random one
        if length <= 5:
            pattern = random.choice(self.common_patterns[:4])  # Shorter patterns
        else:
            pattern = random.choice(self.common_patterns[4:])  # Longer patterns
        
        # If pattern is too long, truncate it
        if len(pattern) > length:
            pattern = pattern[:length]
        
        # If pattern is too short, extend it randomly
        while len(pattern) < length:
            if len(pattern) % 2 == 0:  # Even position, add consonant
                pattern += 'C'
            else:  # Odd position, add vowel
                pattern += 'V'
        
        # Generate word based on pattern
        word = ""
        for char in pattern:
            if char == 'C':
                word += random.choice(self.consonants)
            elif char == 'V':
                word += random.choice(self.vowels)
        
        return word
    
    def generate_simple_random_word(self, min_length: int = 3, max_length: int = 8) -> str:
        """Generate a completely random word using all letters."""
        length = random.randint(min_length, max_length)
        return ''.join(random.choice(self.all_letters) for _ in range(length))
    
    def generate_realistic_word(self, min_length: int = 3, max_length: int = 8) -> str:
        """Generate a word that follows English-like patterns more closely."""
        length = random.randint(min_length, max_length)
        word = ""
        
        # Start with consonant or vowel randomly
        start_with_consonant = random.choice([True, False])
        
        for i in range(length):
            if i == 0:
                # First letter
                if start_with_consonant:
                    word += random.choice(self.consonants)
                else:
                    word += random.choice(self.vowels)
            else:
                # Subsequent letters - alternate or repeat based on probability
                last_char = word[-1]
                if last_char in self.vowels:
                    # After vowel, 70% chance of consonant, 30% vowel
                    if random.random() < 0.7:
                        word += random.choice(self.consonants)
                    else:
                        word += random.choice(self.vowels)
                else:
                    # After consonant, 80% chance of vowel, 20% consonant
                    if random.random() < 0.8:
                        word += random.choice(self.vowels)
                    else:
                        word += random.choice(self.consonants)
        
        return word
    
    def generate_multiple_words(self, count: int, method: str = 'realistic') -> List[str]:
        """Generate multiple words using the specified method."""
        words = []
        for _ in range(count):
            if method == 'pattern':
                word = self.generate_random_word()
            elif method == 'simple':
                word = self.generate_simple_random_word()
            else:  # realistic
                word = self.generate_realistic_word()
            words.append(word)
        return words
    
    def get_word_complexity(self, word: str) -> str:
        """Determine the complexity level of a word."""
        length = len(word)
        vowel_count = sum(1 for char in word if char in self.vowels)
        consonant_count = length - vowel_count
        
        if length <= 3:
            return "simple"
        elif length <= 5:
            return "medium"
        else:
            return "complex"
    
    def analyze_word_pattern(self, word: str) -> dict:
        """Analyze the pattern of a word."""
        vowel_count = sum(1 for char in word if char in self.vowels)
        consonant_count = len(word) - vowel_count
        
        return {
            'length': len(word),
            'vowel_count': vowel_count,
            'consonant_count': consonant_count,
            'vowel_ratio': vowel_count / len(word) if word else 0,
            'pattern': ''.join(['V' if c in self.vowels else 'C' for c in word])
        }
