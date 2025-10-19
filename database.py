import sqlite3
import os
from typing import List, Tuple, Optional

class WordDatabase:
    def __init__(self, db_path: str = "word_learning.db"):
        """Initialize the database connection and create tables if they don't exist."""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create words table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS words (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT UNIQUE NOT NULL,
                    is_valid INTEGER NOT NULL,
                    learned_from TEXT DEFAULT 'guessing',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create word_sequences table for Markov chain
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS word_sequences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word1 TEXT NOT NULL,
                    word2 TEXT NOT NULL,
                    frequency INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create training_texts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS training_texts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text_content TEXT NOT NULL,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def add_word(self, word: str, is_valid: bool, learned_from: str = 'guessing') -> bool:
        """Add a word to the database or update if it exists."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO words (word, is_valid, learned_from)
                    VALUES (?, ?, ?)
                ''', (word.lower(), 1 if is_valid else 0, learned_from))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding word: {e}")
            return False
    
    def get_word(self, word: str) -> Optional[Tuple[str, bool, str]]:
        """Get word information from database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT word, is_valid, learned_from FROM words WHERE word = ?', (word.lower(),))
            result = cursor.fetchone()
            if result:
                return result[0], bool(result[1]), result[2]
            return None
    
    def get_all_words(self) -> List[Tuple[str, bool, str]]:
        """Get all words from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT word, is_valid, learned_from FROM words ORDER BY created_at DESC')
            return [(row[0], bool(row[1]), row[2]) for row in cursor.fetchall()]
    
    def get_valid_words(self) -> List[str]:
        """Get all valid words from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT word FROM words WHERE is_valid = 1')
            return [row[0] for row in cursor.fetchall()]
    
    def add_word_sequence(self, word1: str, word2: str) -> bool:
        """Add or update a word sequence for Markov chain."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO word_sequences (word1, word2, frequency)
                    VALUES (?, ?, 1)
                    ON CONFLICT(word1, word2) DO UPDATE SET
                    frequency = frequency + 1
                ''', (word1.lower(), word2.lower()))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding word sequence: {e}")
            return False
    
    def get_word_sequences(self, word: str) -> List[Tuple[str, int]]:
        """Get all sequences starting with a given word."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT word2, frequency FROM word_sequences 
                WHERE word1 = ? ORDER BY frequency DESC
            ''', (word.lower(),))
            return cursor.fetchall()
    
    def add_training_text(self, text: str) -> bool:
        """Add a training text to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO training_texts (text_content) VALUES (?)', (text,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding training text: {e}")
            return False
    
    def get_statistics(self) -> dict:
        """Get learning statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total words
            cursor.execute('SELECT COUNT(*) FROM words')
            total_words = cursor.fetchone()[0]
            
            # Valid words
            cursor.execute('SELECT COUNT(*) FROM words WHERE is_valid = 1')
            valid_words = cursor.fetchone()[0]
            
            # Invalid words
            cursor.execute('SELECT COUNT(*) FROM words WHERE is_valid = 0')
            invalid_words = cursor.fetchone()[0]
            
            # Training texts
            cursor.execute('SELECT COUNT(*) FROM training_texts')
            training_texts = cursor.fetchone()[0]
            
            # Word sequences
            cursor.execute('SELECT COUNT(*) FROM word_sequences')
            word_sequences = cursor.fetchone()[0]
            
            return {
                'total_words': total_words,
                'valid_words': valid_words,
                'invalid_words': invalid_words,
                'training_texts': training_texts,
                'word_sequences': word_sequences
            }
    
    def clear_database(self):
        """Clear all data from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM words')
            cursor.execute('DELETE FROM word_sequences')
            cursor.execute('DELETE FROM training_texts')
            conn.commit()
