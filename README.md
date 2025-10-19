# AI Word Learning Model

A Python desktop application that learns words through user interaction and generates sentences using Markov chains. The AI model can learn from word guessing, text input, and generate meaningful (not at first, but after a lot of learning) sentences from learned vocabulary. This is not an actual AI and doesn't work like it, this is more like just an algorithm. I really wanted to make an app to start AI, so I decided to make this to take my first step. By the way, ChatGPT helped me a lot (ideas, learning new concepts, troubleshooting, not copy-pasting).

## Features

### 1. Word Guessing Learning

- Generates random English-like words
- User provides feedback (T/F) on whether words are real
- Learns and stores word validity in database

`Mathematically, this was a bad Idea! but anyways I created it.`

### 2. Text Learning

- Processes text input to extract words and patterns
- Learns word sequences for sentence generation
- Analyzes text complexity and word frequency

### 3. Sentence Generation

- Uses Markov chain approach to generate sentences
- Learns from word sequences in provided texts
- Generates sentences based on learned patterns

### 4. Statistics Dashboard

- Shows learning progress and statistics
- Displays word counts, sequences learned, and training data
- Tracks learning effectiveness

## Installation

### Prerequisites

- Python 3.8 or higher

### Setup

1. Clone or download this repository
2. Ensure Python 3.8+ is installed on your system
3. No additional dependencies required (uses only Python standard library)

## Usage

### Running the Application

```bash
python main.py
```

### Interface Overview

#### Tab 1: Word Guessing

1. Click "Generate New Word" to create a random word
2. Decide if the word is real (T) or not real (F)
3. Click the appropriate button to provide feedback
4. The AI learns from your responses

#### Tab 2: Text Learning

1. Enter any text in the text area
2. Click "Learn from Text" to process the text
3. The AI extracts words and learns patterns
4. View learning results and statistics

#### Tab 3: Sentence Generation

1. Set minimum and maximum sentence length
2. Click "Generate Sentence" to create a sentence
3. Provide feedback on sentence quality
4. The AI improves based on your feedback

#### Tab 4: Statistics

1. View learning progress and statistics
2. See total words learned, sequences, and training data
3. Refresh statistics to see latest progress
4. Clear all data if needed :(

## How It Works

### Word Generation

- Uses English letter patterns (vowels/consonants)
- Generates realistic-looking words
- Varies word length and complexity

### Text Processing

- Cleans and normalizes input text
- Extracts individual words and sequences
- Learns word relationships and patterns

### Sentence Generation

- Uses Markov chain approach
- Learns from word sequences in training data
- Generates sentences based on learned probabilities
- Improves with user feedback

### Database Storage

- SQLite database for persistent storage
- Stores words, sequences, and training texts
- Tracks learning progress and statistics

## File Structure

```tree
/
├── main.py                 # Main GUI application
├── database.py             # SQLite database management
├── word_generator.py       # Random word generation
├── text_processor.py       # Text parsing and learning
├── sentence_generator.py   # Markov chain sentence generation
├── README.md              # This file
└── word_learning.db       # SQLite database (created automatically)
```

## Learning Process

### 1. Word Guessing

- AI generates random words
- User provides T/F feedback
- Words are stored with validity status
- Builds vocabulary database

### 2. Text Learning

- User provides text input
- AI extracts words and sequences
- Learns word relationships
- Builds pattern database

### 3. Sentence Generation

- Uses learned word sequences
- Generates sentences using Markov chains
- Learns from user feedback
- Improves over time

## Customization

### Word Generation

- Modify `word_generator.py` to change word patterns
- Adjust vowel/consonant distributions
- Change word length ranges

### Text Processing

- Modify `text_processor.py` for different text handling
- Adjust word extraction rules
- Change sequence learning parameters

### Sentence Generation

- Modify `sentence_generator.py` for different generation methods
- Adjust Markov chain parameters
- Change sentence quality metrics

## Troubleshooting

### Common Issues

1. **Application won't start**: Ensure Python 3.8+ is installed
2. **Database errors**: Check file permissions in the application directory
3. **GUI issues**: Ensure tkinter is available (usually included with Python)

### Performance

- The application uses SQLite for storage (lightweight)
- Text processing runs in background threads
- Large texts may take time to process

## Future Enhancements

- Advanced sentence generation algorithms
- Machine learning model integration
- Export/import functionality
- Advanced text analysis features
- Multi-language support

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to contribute by:

- Reporting bugs
- Suggesting new features
- Improving the code
- Adding documentation

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository
