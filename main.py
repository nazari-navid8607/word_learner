import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from database import WordDatabase
from word_generator import WordGenerator
from text_processor import TextProcessor
from sentence_generator import SentenceGenerator

class AIWordLearningApp:
    def __init__(self, root):
        """Initialize the main application."""
        self.root = root
        self.root.title("AI Word Learning Model")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.db = WordDatabase()
        self.word_generator = WordGenerator()
        self.text_processor = TextProcessor(self.db)
        self.sentence_generator = SentenceGenerator(self.db)
        
        # Current word for guessing
        self.current_word = ""
        
        # Create GUI
        self.create_gui()
        self.update_statistics()
    
    def create_gui(self):
        """Create the main GUI with tabs."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Word Guessing
        self.create_word_guessing_tab()
        
        # Tab 2: Text Learning
        self.create_text_learning_tab()
        
        # Tab 3: Sentence Generation
        self.create_sentence_generation_tab()
        
        # Tab 4: Statistics
        self.create_statistics_tab()
    
    def create_word_guessing_tab(self):
        """Create the word guessing interface."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Word Guessing")
        
        # Title
        title_label = ttk.Label(frame, text="AI Word Learning - Guess the Word", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Current word display
        self.word_display = ttk.Label(frame, text="Click 'Generate Word' to start", 
                                     font=('Arial', 24, 'bold'), 
                                     foreground='#2c3e50')
        self.word_display.pack(pady=20)
        
        # Generate word button
        generate_btn = ttk.Button(frame, text="Generate New Word", 
                                 command=self.generate_new_word)
        generate_btn.pack(pady=10)
        
        # Feedback buttons
        feedback_frame = ttk.Frame(frame)
        feedback_frame.pack(pady=20)
        
        true_btn = ttk.Button(feedback_frame, text="T (True/Real Word)", 
                             command=lambda: self.submit_feedback(True),
                             style='Success.TButton')
        true_btn.pack(side='left', padx=10)
        
        false_btn = ttk.Button(feedback_frame, text="F (False/Not Real)", 
                              command=lambda: self.submit_feedback(False),
                              style='Danger.TButton')
        false_btn.pack(side='left', padx=10)
        
        # Status label
        self.guessing_status = ttk.Label(frame, text="", foreground='#27ae60')
        self.guessing_status.pack(pady=10)
        
        # Configure button styles
        style = ttk.Style()
        style.configure('Success.TButton', foreground='white', background='#27ae60')
        style.configure('Danger.TButton', foreground='white', background='#e74c3c')
    
    def create_text_learning_tab(self):
        """Create the text learning interface."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Text Learning")
        
        # Title
        title_label = ttk.Label(frame, text="Learn from Text Input", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Instructions
        instructions = ttk.Label(frame, 
                                text="Enter text below and click 'Learn from Text' to teach the AI new words and patterns:",
                                font=('Arial', 10))
        instructions.pack(pady=10)
        
        # Text input area
        self.text_input = scrolledtext.ScrolledText(frame, height=15, width=70, 
                                                   font=('Arial', 11))
        self.text_input.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Buttons frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        learn_btn = ttk.Button(button_frame, text="Learn from Text", 
                              command=self.learn_from_text)
        learn_btn.pack(side='left', padx=10)
        
        clear_btn = ttk.Button(button_frame, text="Clear Text", 
                              command=self.clear_text_input)
        clear_btn.pack(side='left', padx=10)
        
        # Learning status
        self.learning_status = ttk.Label(frame, text="", foreground='#27ae60')
        self.learning_status.pack(pady=10)
        
        # Learning results
        self.learning_results = ttk.Label(frame, text="", font=('Arial', 9))
        self.learning_results.pack(pady=5)
    
    def create_sentence_generation_tab(self):
        """Create the sentence generation interface."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Sentence Generation")
        
        # Title
        title_label = ttk.Label(frame, text="Generate Sentences", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Generation controls
        controls_frame = ttk.Frame(frame)
        controls_frame.pack(pady=10)
        
        ttk.Label(controls_frame, text="Max Length:").pack(side='left', padx=5)
        self.max_length_var = tk.StringVar(value="15")
        max_length_entry = ttk.Entry(controls_frame, textvariable=self.max_length_var, width=5)
        max_length_entry.pack(side='left', padx=5)
        
        ttk.Label(controls_frame, text="Min Length:").pack(side='left', padx=5)
        self.min_length_var = tk.StringVar(value="3")
        min_length_entry = ttk.Entry(controls_frame, textvariable=self.min_length_var, width=5)
        min_length_entry.pack(side='left', padx=5)
        
        # Generate button
        generate_btn = ttk.Button(controls_frame, text="Generate Sentence", 
                                 command=self.generate_sentence)
        generate_btn.pack(side='left', padx=20)
        
        # Generated sentence display
        self.sentence_display = ttk.Label(frame, text="Click 'Generate Sentence' to create a sentence", 
                                         font=('Arial', 14), 
                                         foreground='#2c3e50',
                                         wraplength=600)
        self.sentence_display.pack(pady=20)
        
        # Feedback buttons for generated sentence
        feedback_frame = ttk.Frame(frame)
        feedback_frame.pack(pady=10)
        
        good_btn = ttk.Button(feedback_frame, text="Good Sentence", 
                             command=lambda: self.sentence_feedback(True))
        good_btn.pack(side='left', padx=10)
        
        bad_btn = ttk.Button(feedback_frame, text="Bad Sentence", 
                            command=lambda: self.sentence_feedback(False))
        bad_btn.pack(side='left', padx=10)
        
        # Generation status
        self.generation_status = ttk.Label(frame, text="", foreground='#27ae60')
        self.generation_status.pack(pady=10)
    
    def create_statistics_tab(self):
        """Create the statistics display tab."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Statistics")
        
        # Title
        title_label = ttk.Label(frame, text="Learning Statistics", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Statistics display
        self.stats_display = ttk.Label(frame, text="", font=('Arial', 12), 
                                      justify='left')
        self.stats_display.pack(pady=20, padx=20)
        
        # Refresh button
        refresh_btn = ttk.Button(frame, text="Refresh Statistics", 
                                command=self.update_statistics)
        refresh_btn.pack(pady=10)
        
        # Clear database button
        clear_btn = ttk.Button(frame, text="Clear All Data", 
                              command=self.clear_database)
        clear_btn.pack(pady=5)
    
    def generate_new_word(self):
        """Generate a new random word for guessing."""
        self.current_word = self.word_generator.generate_realistic_word()
        self.word_display.config(text=self.current_word)
        self.guessing_status.config(text="Is this a real word? Click T for True or F for False")
    
    def submit_feedback(self, is_valid):
        """Submit feedback for the current word."""
        if not self.current_word:
            messagebox.showwarning("Warning", "Please generate a word first!")
            return
        
        # Save word to database
        success = self.db.add_word(self.current_word, is_valid, 'guessing')
        
        if success:
            status = "Real word" if is_valid else "Not a real word"
            self.guessing_status.config(text=f"Saved: '{self.current_word}' as {status}")
            self.update_statistics()
        else:
            self.guessing_status.config(text="Error saving word!")
        
        # Clear current word
        self.current_word = ""
        self.word_display.config(text="Click 'Generate Word' for next word")
    
    def learn_from_text(self):
        """Learn from the input text."""
        text = self.text_input.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to learn from!")
            return
        
        # Process text in a separate thread to avoid GUI freezing
        def process_text():
            try:
                results = self.text_processor.learn_from_text(text)
                
                # Update GUI in main thread
                self.root.after(0, lambda: self.display_learning_results(results))
            except Exception as e:
                self.root.after(0, lambda: self.display_learning_error(str(e)))
        
        threading.Thread(target=process_text, daemon=True).start()
        self.learning_status.config(text="Processing text...")
    
    def display_learning_results(self, results):
        """Display the results of text learning."""
        self.learning_status.config(text="Text processed successfully!")
        
        results_text = (f"Words learned: {results['words_learned']}\n"
                       f"Sentences processed: {results['sentences_processed']}\n"
                       f"Word sequences learned: {results['sequences_stored']}")
        
        self.learning_results.config(text=results_text)
        self.update_statistics()
    
    def display_learning_error(self, error_msg):
        """Display error from text learning."""
        self.learning_status.config(text=f"Error: {error_msg}")
        self.learning_results.config(text="")
    
    def clear_text_input(self):
        """Clear the text input area."""
        self.text_input.delete("1.0", tk.END)
        self.learning_status.config(text="")
        self.learning_results.config(text="")
    
    def generate_sentence(self):
        """Generate a sentence using learned words."""
        try:
            max_length = int(self.max_length_var.get())
            min_length = int(self.min_length_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for length!")
            return
        
        sentence = self.sentence_generator.generate_sentence(max_length, min_length)
        self.sentence_display.config(text=sentence)
        self.generation_status.config(text="Sentence generated! Rate it below.")
    
    def sentence_feedback(self, is_good):
        """Provide feedback on generated sentence."""
        feedback = "Good" if is_good else "Bad"
        self.generation_status.config(text=f"Feedback recorded: {feedback} sentence")
        
        # Here you could implement learning from feedback
        # For now, just acknowledge the feedback
    
    def update_statistics(self):
        """Update the statistics display."""
        stats = self.db.get_statistics()
        
        stats_text = f"""
Learning Progress:
• Total words learned: {stats['total_words']}
• Valid words: {stats['valid_words']}
• Invalid words: {stats['invalid_words']}
• Training texts processed: {stats['training_texts']}
• Word sequences learned: {stats['word_sequences']}

Ready for sentence generation: {'Yes' if stats['word_sequences'] > 0 else 'No'}
        """
        
        self.stats_display.config(text=stats_text)
    
    def clear_database(self):
        """Clear all data from the database."""
        result = messagebox.askyesno("Confirm", "Are you sure you want to clear all learned data?")
        if result:
            self.db.clear_database()
            self.update_statistics()
            messagebox.showinfo("Success", "All data has been cleared!")

def main():
    """Main function to run the application."""
    root = tk.Tk()
    app = AIWordLearningApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
