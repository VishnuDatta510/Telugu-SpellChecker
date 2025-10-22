import re

def clean_telugu_text(input_filepath, output_filepath):
    """
    Cleans a text file by removing headers, wiki markup, other noise,
    consecutive full stops, very short sentences (1-2 words), and single letters.
    """
    try:
        # Step 1: Read the entire content of the file
        with open(input_filepath, "r", encoding="utf-8") as file:
            text = file.read()
        
        print("Starting bulk data cleaning process...")

        # Step 2: Remove custom headers and Wikipedia section headers
        text = re.sub(r'---.*?---|==.*?==', '', text, flags=re.DOTALL)
        
        # Step 3: Remove common Wikipedia markup and HTML tags
        text = re.sub(r'\[\[(.*?)\]\]', r'\1', text) 
        text = re.sub(r'\{\{(.*?)\}\}', '', text)    
        text = re.sub(r'<[^>]*>', '', text)          

        # Step 4: Remove English words, Hindi words, numbers, and mathematical symbols
        text = re.sub(r'[a-zA-Z]+', '', text, flags=re.UNICODE)
        text = re.sub(r'[\u0900-\u097F]+', '', text, flags=re.UNICODE)  # Hindi
        text = re.sub(r'[0-9+\-*/=()]+', '', text, flags=re.UNICODE)
        
        # Step 5: Keep only Telugu characters and basic punctuation.
        cleaned_text = re.sub(r'[^\u0C00-\u0C7F\s\.,]', '', text, flags=re.UNICODE)
        
        # Step 6: Normalize whitespace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        print("Bulk cleaning complete. Starting line-by-line filtering...")
        
        # Step 7: Filter out unwanted lines
        # Split the text into sentences
        lines = cleaned_text.split('.')
        
        # Regex for junk lines (e.g., "కె.", ",.", or just ".")
        junk_line_pattern = re.compile(r'^\s*([\u0C00-\u0C7F]{1,2}\s*[,\.]?\s*|\s*,\s*\.\s*|\s*\.\s*)$', flags=re.UNICODE)
        
        filtered_lines = []
        for line in lines:
            line = line.strip()
            
            # Skip empty lines or junk lines
            if not line or junk_line_pattern.match(line):
                continue
            
            # Find Telugu words in the sentence
            words = re.findall(r'[\u0C00-\u0C7F]+', line)
            
            # Skip sentences with <= 2 Telugu words
            if len(words) <= 2:
                continue
            
            # Remove single letters (standalone Telugu characters) in the sentence
            line = ' '.join([w for w in words if len(w) > 1])
            
            if line:  # only keep non-empty sentences
                filtered_lines.append(line)
        
        # Join the filtered lines with a full stop and a newline
        final_text = '.\n'.join(filtered_lines) + '.'

        # Remove consecutive full stops (if any)
        final_text = re.sub(r'\.{2,}', '.', final_text)

        # Save the cleaned text to a new file
        with open(output_filepath, "w", encoding="utf-8") as file:
            file.write(final_text)

        print(f"Data cleaning complete. Cleaned data saved to '{output_filepath}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_filepath}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = "corpus.txt" 
    output_file = "final_cleaned_telugu_data_2.txt"
    
    clean_telugu_text(input_file, output_file)
