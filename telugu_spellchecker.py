import re
import json
import pickle
import math
from collections import defaultdict, Counter
from pathlib import Path
import time


class TeluguSpellChecker:
    """
    Main spell checker class with dual memory architecture
    """
    
    def __init__(self, vocab_file='telugu_vocabulary.txt'):
        """
        Initialize the spell checker
        
        Args:
            vocab_file: Path to vocabulary file
        """
        self.vocab_file = vocab_file
        
        # Telugu Unicode pattern (0x0C00 to 0x0C7F)
        self.telugu_pattern = re.compile(r'[\u0C00-\u0C7F]+')
        
        # === MAIN MEMORY (RAM) ===
        # As per requirement: source document + candidate sets stored here
        self.source_documents = {}        # Document ID → {text, timestamp, results}
        self.misspelled_candidates = {}   # Word → list of candidates (cached in RAM)
        self.vocabulary = set()           # Fast lookup set
        self.word_freq = {}               # For semantic ranking
        
        # === SECONDARY MEMORY (Disk) ===
        # As per requirement: entire spell checker index on disk
        self.index_file = Path('spellcheck_index.pkl')
        
        # Statistics tracking
        self.stats = {
            'total_corrections': 0,
            'insertion_ops': 0,
            'deletion_ops': 0,
            'substitution_ops': 0,
            'transposition_ops': 0,
            'words_checked': 0,
            'documents_processed': 0,
            'correct_words': 0,
            'misspelled_words': 0,
            'candidates_found': 0,
            'candidates_not_found': 0
        }
        
        # Initialize
        self._initialize()
    
    def _initialize(self):
        """Load or build spell checker index"""
        print("🔧 Initializing Telugu Spell Checker...")
        
        if self.index_file.exists():
            print(f"📂 Loading index from SECONDARY MEMORY (disk): {self.index_file}")
            self._load_from_disk()
        else:
            print("🔨 Building index and saving to SECONDARY MEMORY...")
            self._build_index()
            self._save_to_disk()
        
        print(f"✅ Ready! Loaded {len(self.vocabulary):,} words")
        
        # Print frequency distribution for verification
        if self.word_freq:
            max_freq = max(self.word_freq.values())
            min_freq = min(self.word_freq.values())
            avg_freq = sum(self.word_freq.values()) / len(self.word_freq)
            print(f"   Frequency range: {min_freq} - {max_freq} (avg: {avg_freq:.2f})\n")
    
    def _build_index(self):
        """Build vocabulary and frequency index from vocabulary file"""
        print(f"   Reading vocabulary from: {self.vocab_file}")
        
        try:
            with open(self.vocab_file, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"   ⚠️  Vocabulary file not found: {self.vocab_file}")
            print(f"   Creating empty vocabulary. Please add words to {self.vocab_file}")
            words = []
        
        # FIXED: Count actual frequencies from the corpus
        # This creates realistic frequency distribution
        word_counts = Counter(words)
        
        # Add to vocabulary with frequencies
        for word, freq in word_counts.items():
            self.vocabulary.add(word)
            self.word_freq[word] = freq
        
        print(f"   Built vocabulary: {len(self.vocabulary):,} unique words")
        print(f"   Total word occurrences: {len(words):,}")
        print(f"   Frequency data: {len(self.word_freq):,} entries")
    
    def _save_to_disk(self):
        """Save complete index to SECONDARY MEMORY (disk)"""
        print(f"\n💾 Saving complete index to SECONDARY MEMORY...")
        
        index_data = {
            'vocabulary': self.vocabulary,
            'word_freq': self.word_freq,
            'metadata': {
                'version': '1.1',  # Updated version
                'total_words': len(self.vocabulary),
                'total_occurrences': sum(self.word_freq.values()),
                'created': time.strftime('%Y-%m-%d %H:%M:%S'),
                'source_file': str(self.vocab_file)
            }
        }
        
        with open(self.index_file, 'wb') as f:
            pickle.dump(index_data, f)
        
        size_mb = self.index_file.stat().st_size / (1024 * 1024)
        print(f"✅ Saved {size_mb:.2f} MB to disk: {self.index_file}")
    
    def _load_from_disk(self):
        """Load index from SECONDARY MEMORY (disk)"""
        start_time = time.time()
        
        with open(self.index_file, 'rb') as f:
            index_data = pickle.load(f)
        
        self.vocabulary = index_data['vocabulary']
        self.word_freq = index_data['word_freq']
        
        elapsed = time.time() - start_time
        
        if 'metadata' in index_data:
            meta = index_data['metadata']
    
    # ========== 4 EDIT OPERATIONS IMPLEMENTATION (FIXED) ==========
    
    def _generate_edits_all_operations(self, word):
        """
        FIXED: Generate all possible words using 4 operations with proper implementation
        1. INSERTION - Add one character
        2. DELETION - Remove one character
        3. SUBSTITUTION - Replace one character
        4. TRANSPOSITION - Swap adjacent characters (FIXED to work correctly)
        
        Args:
            word: Telugu word to generate edits for
            
        Returns:
            dict: Mapping of operation type to list of edited words
        """
        # Telugu character range (0x0C00 to 0x0C7F)
        telugu_chars = [chr(i) for i in range(0x0C00, 0x0C7F)]
        
        # Split word at all positions
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        
        edits = {}
        
        # 1. DELETION: Remove one character
        deletes = [L + R[1:] for L, R in splits if R]
        edits['DELETION'] = [d for d in deletes if d]  # Filter empty strings
        
        # 2. TRANSPOSITION: Swap adjacent characters (FIXED)
        # This was generating incorrect swaps before
        transposes = []
        for i in range(len(word) - 1):
            # Swap characters at position i and i+1
            transposed = word[:i] + word[i+1] + word[i] + word[i+2:]
            transposes.append(transposed)
        edits['TRANSPOSITION'] = transposes
        
        # 3. SUBSTITUTION: Replace one character with another
        replaces = [L + c + R[1:] for L, R in splits if R for c in telugu_chars]
        edits['SUBSTITUTION'] = [r for r in replaces if r]
        
        # 4. INSERTION: Add one character
        inserts = [L + c + R for L, R in splits for c in telugu_chars]
        edits['INSERTION'] = [i for i in inserts if i]
        
        return edits
    
    def _calculate_edit_distance_with_ops(self, source, target):
        """
        FIXED: Calculate minimum edit distance with proper transposition handling
        Uses Damerau-Levenshtein distance algorithm
        
        Args:
            source: Original (misspelled) word
            target: Candidate correction word
            
        Returns:
            tuple: (edit_distance, list_of_operations)
        """
        m, n = len(source), len(target)
        
        # DP table for distances (need extra row/col for transposition)
        INF = float('inf')
        dp = [[INF] * (n + 2) for _ in range(m + 2)]
        
        # Maximum possible distance
        max_dist = m + n
        dp[0][0] = max_dist
        
        # Initialize first row and column
        for i in range(1, m + 2):
            dp[i][0] = max_dist
            dp[i][1] = i - 1
        for j in range(1, n + 2):
            dp[0][j] = max_dist
            dp[1][j] = j - 1
        
        # Track operations
        operations = []
        
        # Dictionary to track last occurrence of each character
        last_match = {}
        
        # Fill DP table with Damerau-Levenshtein algorithm
        for i in range(2, m + 2):
            last_match_j = 0
            for j in range(2, n + 2):
                last_match_i = last_match.get(target[j-2], 0)
                cost = 0 if source[i-2] == target[j-2] else 1
                
                if source[i-2] == target[j-2]:
                    last_match_j = j - 1
                
                # Calculate all possible operations
                deletion = dp[i-1][j] + 1
                insertion = dp[i][j-1] + 1
                substitution = dp[i-1][j-1] + cost
                transposition = dp[last_match_i][last_match_j] + (i - last_match_i - 2) + 1 + (j - last_match_j - 2)
                
                dp[i][j] = min(deletion, insertion, substitution, transposition)
            
            last_match[source[i-2]] = i - 1
        
        # Backtrack to find operations (simplified version)
        distance = dp[m+1][n+1]
        
        # Reconstruct operations
        i, j = m, n
        ops = []
        while i > 0 or j > 0:
            if i == 0:
                ops.append('INSERTION')
                j -= 1
            elif j == 0:
                ops.append('DELETION')
                i -= 1
            elif source[i-1] == target[j-1]:
                i -= 1
                j -= 1
            else:
                # Check which operation was used
                costs = []
                if i > 0 and j > 0:
                    costs.append(('SUBSTITUTION', dp[i][j]))
                if i > 0:
                    costs.append(('DELETION', dp[i][j]))
                if j > 0:
                    costs.append(('INSERTION', dp[i][j]))
                if i > 1 and j > 1 and source[i-1] == target[j-2] and source[i-2] == target[j-1]:
                    costs.append(('TRANSPOSITION', dp[i][j]))
                    ops.append('TRANSPOSITION')
                    i -= 2
                    j -= 2
                    continue
                
                # Find minimum cost operation
                min_cost = min(costs, key=lambda x: x[1])[0]
                ops.append(min_cost)
                
                if min_cost == 'SUBSTITUTION':
                    i -= 1
                    j -= 1
                elif min_cost == 'DELETION':
                    i -= 1
                else:  # INSERTION
                    j -= 1
        
        return distance, list(reversed(ops))
    
    # ========== SEMANTIC RANKING (FIXED) ==========
    
    def _rank_candidates_semantic(self, misspelled_word, candidates):
        """
        FIXED: Rank candidates with proper frequency weighting
        Now produces diverse scores based on actual word frequencies
        
        Ranking formula:
        - Primary: Word frequency (semantic importance) - properly weighted
        - Secondary: Edit distance (strongly weighted)
        - Tertiary: Word length similarity
        
        Args:
            misspelled_word: The incorrect word
            candidates: Set of candidate corrections
            
        Returns:
            list: Ranked list of candidates with diverse scores
        """
        ranked = []
        
        # Get max frequency for normalization
        max_freq = max(self.word_freq.values()) if self.word_freq else 1
        
        for candidate in candidates:
            # FIXED: Better frequency scoring
            freq = self.word_freq.get(candidate, 1)
            
            # Use log scale but with better differentiation
            # Higher frequency words get significantly higher scores
            semantic_score = math.log(freq + 1) * (freq / max_freq)
            
            # Calculate edit distance and track operations
            edit_dist, operations = self._calculate_edit_distance_with_ops(
                misspelled_word, candidate
            )
            
            # Count each operation type
            op_counts = {
                'INSERTION': operations.count('INSERTION'),
                'DELETION': operations.count('DELETION'),
                'SUBSTITUTION': operations.count('SUBSTITUTION'),
                'TRANSPOSITION': operations.count('TRANSPOSITION')
            }
            
            # FIXED: Better combined score calculation
            # Length similarity bonus
            len_diff = abs(len(candidate) - len(misspelled_word))
            length_penalty = len_diff * 0.5
            
            # Edit distance penalty (strong weight)
            edit_penalty = edit_dist * 10
            
            # Combined score: frequency boost - edit penalty - length penalty
            combined_score = (semantic_score * 100) - edit_penalty - length_penalty
            
            ranked.append({
                'word': candidate,
                'semantic_score': semantic_score,
                'frequency': freq,
                'edit_distance': edit_dist,
                'operations': operations,
                'operation_counts': op_counts,
                'combined_score': combined_score
            })
        
        # Sort by combined score (descending)
        ranked.sort(key=lambda x: (-x['combined_score'], x['edit_distance'], -x['frequency']))
        
        return ranked
    
    # ========== CANDIDATE GENERATION ==========
    
    def get_correction_candidates(self, word, max_candidates=5):
        """
        Get ranked correction candidates for a misspelled word
        Candidates stored in MAIN MEMORY as per requirement
        
        Args:
            word: Misspelled Telugu word
            max_candidates: Maximum number of candidates to return
            
        Returns:
            list: Top-ranked candidates with scores
        """
        # Check if word is already correct
        if word in self.vocabulary:
            return []
        
        # Check if candidates already computed (cached in MAIN MEMORY)
        if word in self.misspelled_candidates:
            return self.misspelled_candidates[word]
        
        # Generate all 1-edit candidates using 4 operations
        all_edits = self._generate_edits_all_operations(word)
        
        # Collect valid candidates (exist in vocabulary)
        candidates = set()
        op_tracking = {}  # Track which operation generated each candidate
        
        for op_type, edit_list in all_edits.items():
            for edited_word in edit_list:
                if edited_word in self.vocabulary:
                    candidates.add(edited_word)
                    if edited_word not in op_tracking:
                        op_tracking[edited_word] = op_type
        
        # If no 1-edit candidates found, try 2-edit distance
        if not candidates:
            print(f"   ⚠️  No 1-edit candidates for '{word}', trying 2-edit distance...")
            
            # Generate 2-edit candidates (nested operations)
            for first_edit in sum(all_edits.values(), []):
                if len(candidates) >= 50:  # Limit for performance
                    break
                
                second_edits = self._generate_edits_all_operations(first_edit)
                for edit_list in second_edits.values():
                    for edited_word in edit_list:
                        if edited_word in self.vocabulary:
                            candidates.add(edited_word)
                            if len(candidates) >= 50:
                                break
        
        if not candidates:
            print(f"   ❌ No candidates found for '{word}' (not in vocabulary)")
        
        # Rank candidates by semantic score
        ranked = self._rank_candidates_semantic(word, candidates)
        
        # Store in MAIN MEMORY (as per requirement)
        self.misspelled_candidates[word] = ranked[:max_candidates]
        
        return self.misspelled_candidates[word]
    
    # ========== DOCUMENT PROCESSING ==========
    
    def check_document(self, document_id, text):
        """
        Check entire document and store in MAIN MEMORY
        As per requirement: source document stored in main memory
        
        Args:
            document_id: Unique identifier for document
            text: Telugu text to check
            
        Returns:
            list: Results for each word in document
        """
        # Store source document in MAIN MEMORY
        self.source_documents[document_id] = {
            'text': text,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'word_count': 0,
            'misspelled_count': 0,
            'results': []
        }
        
        # Extract Telugu words
        words = self.telugu_pattern.findall(text)
        self.source_documents[document_id]['word_count'] = len(words)
        
        results = []
        misspelled_count = 0
        
        for word in words:
            self.stats['words_checked'] += 1
            
            if word in self.vocabulary:
                self.stats['correct_words'] += 1
                results.append({
                    'word': word,
                    'is_correct': True,
                    'candidates': []
                })
            else:
                misspelled_count += 1
                self.stats['misspelled_words'] += 1
                candidates = self.get_correction_candidates(word)
                
                if candidates:
                    self.stats['candidates_found'] += 1
                else:
                    self.stats['candidates_not_found'] += 1
                
                results.append({
                    'word': word,
                    'is_correct': False,
                    'candidates': candidates
                })
                
                # Update operation statistics
                if candidates:
                    self.stats['total_corrections'] += 1
                    top_candidate = candidates[0]
                    self.stats['insertion_ops'] += top_candidate['operation_counts']['INSERTION']
                    self.stats['deletion_ops'] += top_candidate['operation_counts']['DELETION']
                    self.stats['substitution_ops'] += top_candidate['operation_counts']['SUBSTITUTION']
                    self.stats['transposition_ops'] += top_candidate['operation_counts']['TRANSPOSITION']
        
        self.source_documents[document_id]['misspelled_count'] = misspelled_count
        self.source_documents[document_id]['results'] = results
        self.stats['documents_processed'] += 1
        
        return results
    
    def correct_document(self, document_id):
        """
        Auto-correct a document using top-ranked candidates
        
        Args:
            document_id: ID of document to correct
            
        Returns:
            str: Corrected text
        """
        if document_id not in self.source_documents:
            raise ValueError(f"Document '{document_id}' not found in main memory")
        
        original_text = self.source_documents[document_id]['text']
        corrected_text = original_text
        results = self.source_documents[document_id]['results']
        
        # Apply corrections
        for result in results:
            if not result['is_correct'] and result['candidates']:
                original_word = result['word']
                correction = result['candidates'][0]['word']
                corrected_text = corrected_text.replace(original_word, correction, 1)
        
        return corrected_text
    
    # ========== UTILITY METHODS ==========
    
    def print_memory_status(self):
        """Display current memory usage and statistics"""
        print("\n" + "="*70)
        print("📊 MEMORY ARCHITECTURE STATUS")
        print("="*70)
        
        print("\n🔴 MAIN MEMORY (RAM):")
        print(f"   Source documents stored: {len(self.source_documents)}")
        total_chars = sum(len(doc['text']) for doc in self.source_documents.values())
        print(f"   Total characters in memory: {total_chars:,}")
        print(f"   Cached candidate sets: {len(self.misspelled_candidates)} words")
        
        print("\n🔵 SECONDARY MEMORY (Disk):")
        if self.index_file.exists():
            size_mb = self.index_file.stat().st_size / (1024 * 1024)
            print(f"   Index file: {self.index_file}")
            print(f"   File size: {size_mb:.2f} MB")
            print(f"   Total vocabulary: {len(self.vocabulary):,} words")
            print(f"   Frequency entries: {len(self.word_freq):,}")
        else:
            print(f"   No index file found")
        
        print("\n📈 OPERATION STATISTICS:")
        print(f"   Documents processed: {self.stats['documents_processed']}")
        print(f"   Words checked: {self.stats['words_checked']}")
        print(f"   Correct words: {self.stats['correct_words']}")
        print(f"   Misspelled words: {self.stats['misspelled_words']}")
        print(f"   Corrections made: {self.stats['total_corrections']}")
        print(f"   Operations breakdown:")
        print(f"      - INSERTION: {self.stats['insertion_ops']}")
        print(f"      - DELETION: {self.stats['deletion_ops']}")
        print(f"      - SUBSTITUTION: {self.stats['substitution_ops']}")
        print(f"      - TRANSPOSITION: {self.stats['transposition_ops']}")
        
        print("="*70 + "\n")
    
    def get_document_summary(self, document_id):
        """Get summary of a processed document"""
        if document_id not in self.source_documents:
            return None
        
        doc = self.source_documents[document_id]
        return {
            'document_id': document_id,
            'timestamp': doc['timestamp'],
            'word_count': doc['word_count'],
            'misspelled_count': doc['misspelled_count'],
            'accuracy': (doc['word_count'] - doc['misspelled_count']) / doc['word_count'] * 100 if doc['word_count'] > 0 else 0
        }
    
    def get_evaluation_metrics(self):
        """
        Calculate spell checker evaluation metrics
        Based on standard IR metrics
        """
        total_words = self.stats['words_checked']
        if total_words == 0:
            return None
        
        # True Positives: Correct words identified as correct
        tp = self.stats['correct_words']
        
        # True Negatives: Misspelled words identified with candidates
        tn = self.stats['candidates_found']
        
        # False Positives: Misspelled words where no candidates found
        fp = self.stats['candidates_not_found']
        
        # Calculate metrics
        detection_accuracy = (tp + tn) / total_words * 100 if total_words > 0 else 0
        
        correction_rate = (tn / self.stats['misspelled_words'] * 100) if self.stats['misspelled_words'] > 0 else 0
        
        return {
            'total_words_checked': total_words,
            'correct_words': tp,
            'misspelled_detected': self.stats['misspelled_words'],
            'candidates_provided': tn,
            'candidates_missing': fp,
            'detection_accuracy': detection_accuracy,
            'correction_rate': correction_rate,
            'vocabulary_size': len(self.vocabulary)
        }
    
    def clear_main_memory(self):
        """Clear main memory caches (keep secondary memory intact)"""
        self.source_documents.clear()
        self.misspelled_candidates.clear()
        print("✅ Main memory cleared")
    
    def export_results(self, document_id, output_file):
        """Export detailed results to JSON file"""
        if document_id not in self.source_documents:
            raise ValueError(f"Document '{document_id}' not found")
        
        doc = self.source_documents[document_id]
        
        export_data = {
            'document_id': document_id,
            'timestamp': doc['timestamp'],
            'original_text': doc['text'],
            'corrected_text': self.correct_document(document_id),
            'statistics': self.get_document_summary(document_id),
            'detailed_results': doc['results']
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Results exported to: {output_file}")


# ========== MODULE-LEVEL FUNCTION ==========

def create_spell_checker(vocab_file='telugu_vocabulary.txt'):
    """
    Factory function to create a spell checker instance
    
    Args:
        vocab_file: Path to vocabulary file
        
    Returns:
        TeluguSpellChecker: Initialized spell checker
    """
    return TeluguSpellChecker(vocab_file)


if __name__ == "__main__":
    # Quick test when run directly
    print("Telugu Spell Checker - Main Module (FIXED VERSION)")
    print("This is the core module. Use test_spellchecker.py for comprehensive testing.\n")
    
    checker = create_spell_checker()
    checker.print_memory_status()
