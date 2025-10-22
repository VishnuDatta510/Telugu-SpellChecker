from telugu_spellchecker import TeluguSpellChecker, create_spell_checker
import time
import sys
from datetime import datetime


class DualOutput:
    """Class to write output to both console and file simultaneously"""
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log_file = open(filename, 'w', encoding='utf-8')
    
    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)
    
    def flush(self):
        self.terminal.flush()
        self.log_file.flush()
    
    def close(self):
        self.log_file.close()


def print_section_header(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70 + "\n")


def print_test_header(test_num, test_name):
    """Print test case header"""
    print("\n" + "="*70)
    print(f"TEST CASE {test_num}: {test_name}")
    print("="*70)


def print_candidate_details(rank, candidate):
    """Print detailed candidate information"""
    print(f"\n   Rank {rank}: {candidate['word']}")
    print(f"   {'─'*65}")
    print(f"    Word Frequency:    {candidate['frequency']}")
    print(f"    Edit Distance:     {candidate['edit_distance']}")
    print(f"    Operations Used:   {' → '.join(candidate['operations']) if candidate['operations'] else 'None'}")
    print(f"    Operation Breakdown:")
    for op, count in candidate['operation_counts'].items():
        if count > 0:
            print(f"      • {op}: {count}")


def run_test_case_1(checker):
    
    print('=============================================')
    print('TEST CASE 1')
    print('=============================================')

    test_text = "తెలుగ భాష చాల మధురమైనద"  # Missing characters intentionally
    
    print(f"Original Text: {test_text}")
    
    results = checker.check_document('test_1', test_text)
    
    misspelled = [r for r in results if not r['is_correct']]
    
    if not misspelled:
        print("  Note: All words found in vocabulary (possible data leakage)")
        print("  Suggestion: Use words intentionally misspelled and not in vocabulary")
    else:
        print(f" Found {len(misspelled)} misspelled word(s):\n")
        
        for i, result in enumerate(misspelled, 1):
            print(f"{i}. Misspelled: '{result['word']}'")
            print(f"   Candidates (Ranked by Semantic Importance):")
            
            if result['candidates']:
                for rank, candidate in enumerate(result['candidates'][:3], 1):  # Show top 3
                    print_candidate_details(rank, candidate)
            else:
                print("    No candidates found (word too different from vocabulary)")
            print()
    
    print("─"*70)
    print(f" Test Case 1 Complete\n")


def run_test_case_2(checker):


    print('=============================================')
    print('TEST CASE 2')
    print('=============================================')
    
    test_text = "హైదరాబాదదద తెలంగాణాఅా రాజధాని"  # Extra characters
    
    print(f"Description: Extra characters - requires DELETION operation")
    print(f"Original Text: {test_text}")
    print(f"Expected: Extra 'ద' and 'అ' should trigger DELETION\n")
    
    results = checker.check_document('test_2', test_text)
    
    misspelled = [r for r in results if not r['is_correct']]
    
    if not misspelled:
        print("  No spelling errors found in vocabulary")
    else:
        print(f" Found {len(misspelled)} misspelled word(s):\n")
        
        for i, result in enumerate(misspelled, 1):
            print(f"{i}. Misspelled: '{result['word']}'")
            print(f"   Candidates (Ranked by Semantic Importance):")
            
            if result['candidates']:
                for rank, candidate in enumerate(result['candidates'][:3], 1):
                    print_candidate_details(rank, candidate)
            else:
                print("    No candidates found")
            print()
    
    print("─"*70)
    print(f" Test Case 2 Complete\n")


def run_test_case_3(checker):


    print('=============================================')
    print('TEST CASE 3')
    print('=============================================')

    test_text = "కంపూటర శాసతరమ చాలా ఆసకతికరమ"  # Wrong characters
    
    print(f"Description: Wrong characters - requires SUBSTITUTION operation")
    print(f"Original Text: {test_text}")
    print(f"Expected: Wrong 'త' and 'క' should trigger SUBSTITUTION\n")
    
    results = checker.check_document('test_3', test_text)
    
    misspelled = [r for r in results if not r['is_correct']]
    
    if not misspelled:
        print("  No spelling errors found")
    else:
        print(f"Found {len(misspelled)} misspelled word(s):\n")
        
        for i, result in enumerate(misspelled, 1):
            print(f"{i}. Misspelled: '{result['word']}'")
            print(f"   Candidates (Ranked by Semantic Importance):")
            
            if result['candidates']:
                for rank, candidate in enumerate(result['candidates'][:3], 1):
                    print_candidate_details(rank, candidate)
            else:
                print("    No candidates found")
            print()
    
    print("─"*70)
    print(f" Test Case 3 Complete\n")


def run_test_case_4(checker):


    print('=============================================')
    print('TEST CASE 4')
    print('=============================================')
    
    # FIXED: Using clear transposition examples
    test_text = "విద్యార్ధులు పుసతకాలు చదువుతారు"  # స and త swapped in పుస్తకాలు
    
    print(f"Description: Adjacent characters swapped - requires TRANSPOSITION")
    print(f"Original Text: {test_text}")
    print(f"Expected: 'పుసతకాలు' should be corrected to 'పుస్తకాలు' via TRANSPOSITION\n")
    
    results = checker.check_document('test_4', test_text)
    
    misspelled = [r for r in results if not r['is_correct']]
    
    if not misspelled:
        print("  No spelling errors found")
    else:
        print(f" Found {len(misspelled)} misspelled word(s):\n")
        
        for i, result in enumerate(misspelled, 1):
            print(f"{i}. Misspelled: '{result['word']}'")
            print(f"   Candidates (Ranked by Semantic Importance):")
            
            if result['candidates']:
                for rank, candidate in enumerate(result['candidates'][:3], 1):
                    print_candidate_details(rank, candidate)
                    
                # VERIFICATION: Check if transposition was detected
                if any(c['operation_counts']['TRANSPOSITION'] > 0 for c in result['candidates']):
                    print("   ✅ TRANSPOSITION operation detected successfully!")
                else:
                    print("    Note: TRANSPOSITION not detected (using other operations)")
            else:
                print("    No candidates found")
            print()
    
    print("─"*70)
    print(f" Test Case 4 Complete\n")


def run_test_case_5(checker):


    print('=============================================')
    print('TEST CASE 5')
    print('=============================================')
    
    test_text = "భారతదేశమ సావతంత్రమ పొందింది ఆగస్టు పదహేనూ"
    
    print(f"Description: Multiple error types - requires mixed operations")
    print(f"Original Text: {test_text}")
    print(f"Expected: Mix of INSERTION, DELETION, SUBSTITUTION operations\n")
    
    results = checker.check_document('test_5', test_text)
    
    misspelled = [r for r in results if not r['is_correct']]
    
    if not misspelled:
        print("  No spelling errors found")
    else:
        print(f" Found {len(misspelled)} misspelled word(s):\n")
        
        for i, result in enumerate(misspelled, 1):
            print(f"{i}. Misspelled: '{result['word']}'")
            print(f"   Candidates (Ranked by Semantic Importance):")
            
            if result['candidates']:
                for rank, candidate in enumerate(result['candidates'][:3], 1):
                    print_candidate_details(rank, candidate)
            else:
                print("    No candidates found")
            print()
    
    print("─"*70)
    print(f" Test Case 5 Complete\n")


def demonstrate_memory_architecture(checker):
    """Demonstrate the dual memory architecture"""
    print_section_header("MEMORY ARCHITECTURE DEMONSTRATION")
    
    print("This demonstrates the dual-tier memory system:\n")
    
    print("   MAIN MEMORY (RAM) - Fast Access:")
    print("   - Source documents (original text)")
    print("   - Candidate correction sets (cached results)")
    print("   - Currently processed data\n")
    
    print("   SECONDARY MEMORY (Disk) - Persistent Storage:")
    print("   - Complete vocabulary index")
    print("   - Word frequency data")
    print("   - Saved permanently for reuse\n")
    
    checker.print_memory_status()


def demonstrate_auto_correction(checker):
    """Demonstrate auto-correction feature"""
    print_section_header("AUTO-CORRECTION DEMONSTRATION")
    
    test_docs = [
        ('doc_1', 'తెలుగ భాష చాల మధురమైనద'),
        ('doc_2', 'హైదరాబాదదద రాజధాని')
        ]
    
    for doc_id, text in test_docs:
        print(f"\nDocument ID: {doc_id}")
        print(f"Original:  {text}")
        
        checker.check_document(doc_id, text)
        corrected = checker.correct_document(doc_id)
        
        print(f"Corrected: {corrected}")
        
        summary = checker.get_document_summary(doc_id)
        if summary:
            print(f"Accuracy:  {summary['accuracy']:.1f}%")
            print(f"Errors:    {summary['misspelled_count']}/{summary['word_count']}")


def demonstrate_export_feature(checker):
    """Demonstrate result export to JSON"""
    print_section_header("EXPORT FEATURE DEMONSTRATION")
    
    test_text = "తెలుగ భాష చాల మధురమైనద"
    doc_id = 'export_demo'
    
    print(f"Processing document: {test_text}")
    checker.check_document(doc_id, test_text)
    
    output_file = f'{doc_id}_results.json'
    checker.export_results(doc_id, output_file)
    
    print(f"\n Detailed results exported to: {output_file}")
    print("   This file contains:")
    print("   - Original text")
    print("   - Corrected text")
    print("   - Statistics")
    print("   - Detailed word-by-word analysis")


def run_all_tests():
    """Run complete test suite with file logging"""
    
    # Generate timestamp for log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"spellchecker_test_results_{timestamp}.txt"
    
    # Redirect output to both console and file
    dual_output = DualOutput(log_filename)
    sys.stdout = dual_output
    
    try:
        
        time.sleep(1)
        
        # Initialize spell checker
        print_section_header("INITIALIZATION")
        checker = create_spell_checker()
        
        # Run test cases
        run_test_case_1(checker)
        time.sleep(0.5)
        
        run_test_case_2(checker)
        time.sleep(0.5)
        
        run_test_case_3(checker)
        time.sleep(0.5)
        
        run_test_case_4(checker)
        time.sleep(0.5)
        
        run_test_case_5(checker)
        time.sleep(0.5)
        
        # Memory architecture demonstration
        demonstrate_memory_architecture(checker)
        time.sleep(0.5)
        
        # Auto-correction demonstration
        demonstrate_auto_correction(checker)
        time.sleep(0.5)
        
        # Export feature demonstration
        demonstrate_export_feature(checker)
        time.sleep(0.5)
        
    finally:
        # Restore original stdout and close log file
        sys.stdout = dual_output.terminal
        dual_output.close()
        
        print(f"\n✅ Test results successfully saved to: {log_filename}")
        from pathlib import Path
        print(f"   File size: {Path(log_filename).stat().st_size / 1024:.2f} KB")


if __name__ == "__main__":
    run_all_tests()
