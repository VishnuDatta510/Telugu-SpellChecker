# Telugu Spell Checker

## Project Overview

A comprehensive spell checker implementation for Telugu language that identifies misspelled words, provides ranked correction candidates based on semantic importance, and performs corrections using four edit operations: insertion, deletion, substitution, and transposition.

## Author Information

**Roll Number:** S20230010083 
**Language:** Telugu  
**Dataset Sources:** Wikipedia dumps and web-scraped corpus data

---

## Table of Contents

1. [Features](#features)
2. [System Architecture](#system-architecture)
3. [Dataset Information](#dataset-information)
4. [Installation & Setup](#installation--setup)
5. [Project Structure](#project-structure)
6. [Module Descriptions](#module-descriptions)
7. [Usage Instructions](#usage-instructions)
8. [Test Cases](#test-cases)
9. [Memory Architecture](#memory-architecture)
10. [Technical Details](#technical-details)
11. [Output Files](#output-files)

---

## Features

✅ **Misspelled Word Detection** - Identifies Telugu words not present in the vocabulary  
✅ **Semantic Ranking** - Ranks correction candidates based on word frequency (semantic importance)  
✅ **4 Edit Operations** - Implements INSERT, DELETE, SUBSTITUTE, and TRANSPOSE operations  
✅ **Dual Memory Architecture** - Main memory (RAM) for active documents, secondary memory (disk) for persistent index  
✅ **Auto-Correction** - Automatically corrects documents using top-ranked candidates  
✅ **Export Functionality** - Exports detailed results to JSON format 
✅ **Performance Metrics** - Tracks accuracy, detection rates, and operation statistics

---

## System Architecture

### Memory Architecture

**Main Memory (RAM):**
- Source documents (original text)
- Candidate correction sets (cached results)
- Currently processed data

**Secondary Memory (Disk):**
- Complete vocabulary index
- Word frequency data
- Persistent storage in `spellcheck_index.pkl`

---

## Dataset Information

### Sources

1. **Wikipedia Dump**: Telugu Wikipedia articles (XML format)
2. **Web Corpus**: Telugu text crawled from various web sources

### Dataset Access

Full datasets and generated index files available at:  
**[Google Drive Link](https://drive.google.com/drive/folders/1-yJOhP0d0on2vaYXk9QnvT0pG2hklsLY?usp=sharing)**

**Files included:**
- `corpus.txt` - Raw web-scraped Telugu content
- `wiki_data.txt` - Raw Wikipedia dump content
- `spellcheck_index.pkl` - Pre-built vocabulary index
- `telugu_vocabulary.txt` - Final merged vocabulary

---

## Installation & Setup

### Prerequisites

```bash
Python 3.7 or higher
```

### Required Libraries

```bash
# All libraries are part of Python standard library
# No additional installations required
```

### Setup Steps

1. **Clone/Extract the project:**
   ```bash
  git clone https://github.com/VishnuDatta510/Telugu-SpellChecker.git .
   ```

   **OR**
   
   - Extract the S20230010083-src.zip
   - Open in VS Code

2. **Prepare datasets:**
   - Download Wikipedia dump for Telugu
   - Collect corpus data (or use provided corpus.txt)
   - Download Wikidata.txt and corpus.txt from the drive link provided
   - Place files in project root directory

3. **Verify file structure:**
   ```
   S20230010083-src/
   ├── corpus.txt
   ├── wiki_data.txt
   ├── clean_corpus.py
   ├── clean_wiki.py
   ├── tokenizationAndVocabulary1.py
   ├── tokenizationAndVocabulary2.py
   ├── merge.py
   ├── telugu_spellchecker.py
   └── test_spellchecker.py
   ```

---

## Project Structure

```
S20230010083-src/
│
├── Data Cleaning Scripts
│   ├── clean_wiki.py                      # Cleans Wikipedia data
│   └── clean_corpus.py                    # Cleans corpus data
│
├── Tokenization Scripts
│   ├── tokenizationAndVocabulary1.py      # Processes cleaned Wikipedia data
│   └── tokenizationAndVocabulary2.py      # Processes cleaned corpus data
│
├── Merging Script
│   └── merge.py                           # Merges all processed data
│
├── Core Spell Checker
│   ├── telugu_spellchecker.py             # Main spell checker implementation
│   └── test_spellchecker.py               # Comprehensive test suite
│
├── Input Data Files
│   ├── corpus.txt                         # Raw corpus data
│   └── wiki_data.txt                      # Raw Wikipedia data
│
├── Intermediate Files (Generated)
│   ├── final_cleaned_telugu_data_1.txt    # Cleaned Wikipedia data
│   ├── final_cleaned_telugu_data_2.txt    # Cleaned corpus data
│   ├── telugu_sentences_1.txt             # Wikipedia sentences
│   ├── telugu_sentences_2.txt             # Corpus sentences
│   ├── telugu_vocabulary_1.txt            # Wikipedia vocabulary
│   ├── telugu_vocabulary_2.txt            # Corpus vocabulary
│   ├── telugu_tokenized_sentences_1.json  # Wikipedia tokens
│   └── telugu_tokenized_sentences_2.json  # Corpus tokens
│
├── Final Output Files (Generated)
│   ├── telugu_vocabulary.txt              # Merged vocabulary
│   ├── telugu_sentences.txt               # Merged sentences
│   ├── final_cleaned_telugu_data.txt      # Merged cleaned data
│   ├── telugu_tokenized_sentences.json    # Merged tokens
│   └── spellcheck_index.pkl               # Vocabulary index (37.67 MB)
│
└── Test Results
    ├── spellchecker_test_results_*.txt    # Test output logs
    └── export_demo_results.json           # Sample exported results
```

---

## Module Descriptions

### 1. Data Cleaning Modules

#### `clean_wiki.py`
**Purpose:** Cleans raw Wikipedia dump data  
**Input:** `wiki_data.txt`  
**Output:** `final_cleaned_telugu_data_1.txt`

**Cleaning Operations:**
- Removes Wikipedia markup (`[[...]]`, `{{...}}`, `<...>`)
- Removes section headers (`==...==`)
- Filters out English and Hindi text
- Removes numbers and mathematical symbols
- Keeps only Telugu Unicode characters (U+0C00 to U+0C7F)
- Filters sentences with fewer than 3 words
- Removes single-character words
- Normalizes whitespace

#### `clean_corpus.py`
**Purpose:** Cleans web-scraped corpus data  
**Input:** `corpus.txt`  
**Output:** `final_cleaned_telugu_data_2.txt`

**Operations:** Same as `clean_wiki.py` (ensures consistent cleaning across both datasets)

### 2. Tokenization Modules

#### `tokenizationAndVocabulary1.py`
**Purpose:** Tokenizes cleaned Wikipedia data  
**Input:** `final_cleaned_telugu_data_1.txt`  
**Outputs:**
- `telugu_sentences_1.txt` - Extracted sentences
- `telugu_vocabulary_1.txt` - Unique words
- `telugu_tokenized_sentences_1.json` - Tokenized sentences

**Process:**
1. Splits text into sentences (period-delimited)
2. Extracts Telugu words using regex pattern
3. Builds vocabulary set
4. Saves in multiple formats for flexibility

#### `tokenizationAndVocabulary2.py`
**Purpose:** Tokenizes cleaned corpus data  
**Input:** `final_cleaned_telugu_data_2.txt`  
**Outputs:**
- `telugu_sentences_2.txt`
- `telugu_vocabulary_2.txt`
- `telugu_tokenized_sentences_2.json`

**Process:** Identical to `tokenizationAndVocabulary1.py`

### 3. Merging Module

#### `merge.py`
**Purpose:** Merges and deduplicates all processed data  
**Inputs:**
- `telugu_sentences_1.txt` + `telugu_sentences_2.txt`
- `telugu_vocabulary_1.txt` + `telugu_vocabulary_2.txt`
- `final_cleaned_telugu_data_1.txt` + `final_cleaned_telugu_data_2.txt`
- `telugu_tokenized_sentences_1.json` + `telugu_tokenized_sentences_2.json`

**Outputs:**
- `telugu_sentences.txt` - Deduplicated sentences
- `telugu_vocabulary.txt` - **Final vocabulary (959,816 unique words)**
- `final_cleaned_telugu_data.txt` - Combined cleaned data
- `telugu_tokenized_sentences.json` - Deduplicated tokens

**Operations:**
- Uses Python sets to remove duplicates
- Sorts output for consistency
- Reports statistics for each merge operation

### 4. Core Spell Checker Module

#### `telugu_spellchecker.py`
**Purpose:** Main spell checker implementation  
**Input:** `telugu_vocabulary.txt`  
**Output:** `spellcheck_index.pkl` (persistent index)

**Key Components:**

##### TeluguSpellChecker Class

**Initialization:**
```python
checker = TeluguSpellChecker(vocab_file='telugu_vocabulary.txt')
```
- Loads vocabulary from file
- Builds frequency index
- Creates or loads persistent index from disk

**Core Methods:**

1. **`_generate_edits_all_operations(word)`**
   - Generates candidates using 4 operations:
     - **INSERTION**: Adds one Telugu character at any position
     - **DELETION**: Removes one character
     - **SUBSTITUTION**: Replaces one character with another
     - **TRANSPOSITION**: Swaps two adjacent characters
   - Returns dictionary mapping operation type to candidate list

2. **`_calculate_edit_distance_with_ops(source, target)`**
   - Uses Damerau-Levenshtein distance algorithm
   - Calculates minimum edit distance
   - Tracks which operations were used
   - Returns distance and operation sequence

3. **`_rank_candidates_semantic(misspelled_word, candidates)`**
   - Ranks candidates by semantic importance
   - **Ranking Formula:**
     ```
     semantic_score = log(frequency + 1) × (frequency / max_frequency)
     combined_score = (semantic_score × 100) - (edit_distance × 10) - (length_penalty × 0.5)
     ```
   - Higher frequency words ranked higher
   - Lower edit distance preferred
   - Returns sorted list with detailed scores

4. **`get_correction_candidates(word, max_candidates=5)`**
   - Main correction method
   - Generates 1-edit candidates first
   - Falls back to 2-edit if needed
   - Caches results in main memory
   - Returns top-ranked candidates

5. **`check_document(document_id, text)`**
   - Processes entire document
   - Stores document in main memory
   - Identifies all misspelled words
   - Gets candidates for each error
   - Returns detailed results

6. **`correct_document(document_id)`**
   - Auto-corrects document
   - Uses top-ranked candidate for each error
   - Returns corrected text

7. **`export_results(document_id, output_file)`**
   - Exports results to JSON
   - Includes original and corrected text
   - Provides statistics and detailed analysis

**Memory Management:**

- **Main Memory (RAM):**
  - `source_documents`: Dictionary of processed documents
  - `misspelled_candidates`: Cache of candidate corrections
  - `vocabulary`: Set for fast lookup

- **Secondary Memory (Disk):**
  - `spellcheck_index.pkl`: Persistent vocabulary and frequency data
  - Automatically loaded on initialization
  - Saved once during index building

**Statistics Tracking:**
- Total corrections made
- Operation type counts (INSERT, DELETE, SUBSTITUTE, TRANSPOSE)
- Words checked, correct, and misspelled
- Documents processed

### 5. Test Module

#### `test_spellchecker.py`
**Purpose:** Comprehensive testing and demonstration  

**Test Cases:**

1. **Test Case 1: Basic Misspelling**
   - Tests missing character detection
   - Verifies INSERTION operation

2. **Test Case 2: Extra Characters**
   - Tests extra character detection
   - Verifies DELETION operation

3. **Test Case 3: Wrong Characters**
   - Tests incorrect character detection
   - Verifies SUBSTITUTION operation

4. **Test Case 4: Character Swapping**
   - Tests adjacent character swap
   - Verifies TRANSPOSITION operation

5. **Test Case 5: Multiple Errors**
   - Tests mixed error types
   - Verifies combination of operations

**Additional Demonstrations:**
- Memory architecture status display
- Auto-correction feature
- Result export to JSON
- Performance metrics

**Output:**
- Generates timestamped log file: `spellchecker_test_results_YYYYMMDD_HHMMSS.txt`
- Detailed candidate rankings with operation breakdowns
- Accuracy statistics

---

## Usage Instructions

### Complete Workflow (From Scratch)

#### Step 1: Prepare Raw Data
```bash
# Ensure you have:
# - corpus.txt (web-scraped Telugu content)
# - wiki_data.txt (Wikipedia dump)
```

#### Step 2: Clean the Data
```bash
# Clean Wikipedia data
python clean_wiki.py

# Clean corpus data
python clean_corpus.py

# Output:
# - final_cleaned_telugu_data_1.txt
# - final_cleaned_telugu_data_2.txt
```

#### Step 3: Tokenize and Build Vocabulary
```bash
# Process Wikipedia data
python tokenizationAndVocabulary1.py

# Process corpus data
python tokenizationAndVocabulary2.py

# Outputs:
# - telugu_sentences_1.txt, telugu_vocabulary_1.txt, telugu_tokenized_sentences_1.json
# - telugu_sentences_2.txt, telugu_vocabulary_2.txt, telugu_tokenized_sentences_2.json
```

#### Step 4: Merge All Data
```bash
python merge.py

# Outputs:
# - telugu_vocabulary.txt (959,816 words)
# - telugu_sentences.txt
# - final_cleaned_telugu_data.txt
# - telugu_tokenized_sentences.json
```

#### Step 5: Run Spell Checker Tests
```bash
python test_spellchecker.py

# This will:
# 1. Load/build vocabulary index (creates spellcheck_index.pkl)
# 2. Run all 5 test cases
# 3. Demonstrate memory architecture
# 4. Show auto-correction
# 5. Export sample results
# 6. Generate timestamped log file
```

### Using the Spell Checker Programmatically

```python
from telugu_spellchecker import create_spell_checker

# Initialize
checker = create_spell_checker()

# Check a document
text = "మీ తెలుగు వచనం ఇక్కడ"
results = checker.check_document('my_doc', text)

# Get correction candidates
for result in results:
    if not result['is_correct']:
        print(f"Misspelled: {result['word']}")
        for candidate in result['candidates']:
            print(f"  → {candidate['word']} (score: {candidate['combined_score']:.2f})")

# Auto-correct
corrected_text = checker.correct_document('my_doc')
print(f"Corrected: {corrected_text}")

# Export results
checker.export_results('my_doc', 'output.json')

# View statistics
checker.print_memory_status()
```

---

## Test Cases

### Test Case 1: Missing Character (INSERTION)
**Input:** `తెలుగ భాష చాల మధురమైనద`  
**Error:** `మధురమైనద` (missing `ో`)  
**Correction:** `మధురమైనదో`  
**Operation:** INSERTION  
**Accuracy:** 75.0%

### Test Case 2: Extra Characters (DELETION)
**Input:** `హైదరాబాదదద తెలంగాణాఆ రాజధాని`  
**Errors:**
- `హైదరాబాదదద` → `హైదరాబాదా` (extra `ద`)
- `తెలంగాణాఆ` → `తెలంగాణానా` (extra `ఆ`)

**Operation:** DELETION  
**Accuracy:** 50.0%

### Test Case 3: Wrong Characters (SUBSTITUTION)
**Input:** `కంపూటర శాసతరం చాలా ఆసకతికరం`  
**Errors:**
- `శాసతరం` → `యాస్రం` (wrong characters)
- `ఆసకతికరం` → `ఆసక్తికర` (wrong characters)

**Operation:** SUBSTITUTION  
**Accuracy:** 66.7%

### Test Case 4: Swapped Characters (TRANSPOSITION)
**Input:** `విద్యార్థులు పుసతకాలు చదువుతారు`  
**Error:** `పుసతకాలు` → `పుస్తకాలు` (swapped `స` and `త`)  
**Operation:** TRANSPOSITION  
**Accuracy:** 66.7%

### Test Case 5: Multiple Error Types (MIXED)
**Input:** `భారతదేశం సావతంత్రం పొందింది ఆగస్టు పదహేనూ`  
**Errors:**
- `భారతదేశం` → `భారతదేశం` (wrong ending)
- `సావతంత్రం` → `స్వతంత్రా` (multiple wrong characters)
- `పదహేనూ` → `పదనేనూ` (wrong character)

**Operations:** INSERTION + DELETION + SUBSTITUTION  
**Accuracy:** 40.0%

---

## Memory Architecture

### Main Memory (RAM) Contents

**During Execution:**
- Source documents: ~150 characters (5 test documents)
- Cached candidate sets: 10 words
- Active vocabulary set for fast lookup

**Advantages:**
- Fast access to frequently used data
- Efficient candidate caching
- Quick document retrieval

### Secondary Memory (Disk) Contents

**Persistent Storage:**
- `spellcheck_index.pkl`
- Vocabulary: 959,816 unique words
- Frequency data: 959,816 entries
- Created once, reused across sessions

**Advantages:**
- Persistent across program runs
- No need to rebuild vocabulary each time
- Shareable index file

---

## Technical Details

### Algorithm: Damerau-Levenshtein Distance

Uses dynamic programming with O(m×n) complexity where m and n are word lengths.

**Supported Operations:**
1. **Insertion**: Add character at any position
2. **Deletion**: Remove any character
3. **Substitution**: Replace any character
4. **Transposition**: Swap adjacent characters

### Telugu Unicode Range

Characters: U+0C00 to U+0C7F  
Includes: Vowels, consonants, vowel signs, and special symbols

### Ranking Algorithm

```python
semantic_score = log(frequency + 1) × (frequency / max_frequency)
edit_penalty = edit_distance × 10
length_penalty = |len(candidate) - len(misspelled)| × 0.5
combined_score = (semantic_score × 100) - edit_penalty - length_penalty
```

**Sorting:** Descending by combined_score, then by edit_distance, then by frequency

---

## Output Files

### Generated Files

1. **`spellcheck_index.pkl`** - Binary vocabulary index (37.67 MB)
2. **`spellchecker_test_results_*.txt`** - Test execution logs with timestamps
3. **`export_demo_results.json`** - Sample exported results in JSON format
4. **`*_results.json`** - User-generated export files from document processing

### Log File Format

```
======================================================================
 INITIALIZATION
======================================================================
 Initializing Telugu Spell Checker...
 Ready! Loaded 959,816 words

=============================================
TEST CASE 1
=============================================
Original Text: తెలుగ భాష చాల మధురమైనద
 Found 1 misspelled word(s):

1. Misspelled: 'మధురమైనద'
   Candidates (Ranked by Semantic Importance):
   
   Rank 1: మధురమైనదో
   ─────────────────────────────────────────────────────────────────
    Word Frequency:    1
    Edit Distance:     1
    Operations Used:   INSERTION → SUBSTITUTION (multiple)
    Operation Breakdown:
      • INSERTION: 1
      • SUBSTITUTION: 8
```


---

## Performance Metrics

### Test Results Summary

- **Vocabulary Size:** 959,816 unique words
- **Index Size:** 37.67 MB
- **Documents Processed:** 5
- **Words Checked:** 19
- **Correct Words:** 9
- **Misspelled Words:** 10
- **Corrections Made:** 10

### Operation Statistics

- **INSERTION:** 3 operations
- **DELETION:** 1 operation
- **SUBSTITUTION:** 35 operations
- **TRANSPOSITION:** 1 operation

---

## Troubleshooting

### Common Issues

**1. FileNotFoundError for vocabulary file**
```bash
Solution: Run steps 1-4 in order to generate telugu_vocabulary.txt
```

**2. Empty candidates for misspelled words**
```bash
Reason: Word too different from vocabulary (>2 edit distance)
Solution: Expand vocabulary or adjust max_edit_distance
```

**3. Memory error during index building**
```bash
Solution: Process vocabulary in chunks or increase available RAM
```

**4. Slow candidate generation**
```bash
Reason: Large vocabulary (959K words)
Solution: Use caching (already implemented) or filter by prefix
```

---

## References

1. Wikipedia Telugu Dump: https://dumps.wikimedia.org/tewiki/
2. Peter Norvig's Spell Checker: https://norvig.com/spell-correct.html
3. Damerau-Levenshtein Distance: https://en.wikipedia.org/wiki/Damerau–Levenshtein_distance
4. Telugu Unicode: https://unicode.org/charts/PDF/U0C00.pdf

---

## Conclusion

This Telugu spell checker demonstrates a complete information retrieval system with:
- Efficient data collection and indexing
- Sophisticated error detection and correction
- Intelligent ranking based on multiple metrics
- Proper memory management architecture
- Comprehensive testing and documentation

The system is modular, extensible, and ready for production use with larger datasets.

---

## License

This project is created for academic purposes as part of coursework requirements.

---

## Contact

For questions or issues, please contact: vishnudatta.g23@iiits.in

---
