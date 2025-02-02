from FM_Index import *


def run_tests():
    # Initialize FMIndex with a basic text
    text = "banana"
    fm_index = FMIndex(text)

    print("=== FM-Index Test Cases ===")

    # Test Case 1: Initialization and Building
    print("\nTest Case 1: Initialization")
    assert fm_index.text == "banana$", "Text initialization failed."
    assert fm_index.bwt == "annb$aa", "BWT computation failed."
    assert fm_index.suffix_array == [6, 5, 3, 1, 0, 4, 2], "Suffix array computation failed."
    print("Initialization successful!")

    # Test Case 2: Searching for patterns
    print("\nTest Case 2: Pattern Search")
    pattern1 = "ana"
    pattern2 = "ban"
    pattern3 = "xyz"
    assert fm_index.search(pattern1) == [1,3], f"Search for '{pattern1}' failed."
    assert fm_index.search(pattern2) == [0], f"Search for '{pattern2}' failed."
    assert fm_index.search(pattern3) == [], f"Search for '{pattern3}' failed."
    print("Pattern search passed for all cases.")

    # Test Case 3: Insert a character
    print("\nTest Case 3: Insert Character")
    fm_index.insert('s')
    assert fm_index.text == "bananas$", "Text after insertion failed."
    assert "s" in fm_index.bwt, "BWT after insertion failed."
    print("Character insertion successful!")

    # Test Case 4: Delete a character
    print("\nTest Case 4: Delete Character")
    fm_index.delete(1)  # Remove 'a' at index 1
    assert fm_index.text == "bnanas$", "Text after deletion failed."
    assert "a" in fm_index.bwt, "BWT after deletion contains wrong data."
    print("Character deletion successful!")

    # Test Case 5: Edge Cases
    print("\nTest Case 5: Edge Cases")
    # Empty initialization
    try:
        FMIndex("")
    except ValueError as e:
        assert str(e) == "Input text cannot be empty.", "Empty input edge case failed."

    # Empty pattern search
    try:
        fm_index.search("")
    except ValueError as e:
        assert str(e) == "Search pattern cannot be empty.", "Empty pattern search failed."

    # Insert invalid input
    try:
        fm_index.insert("ab")
    except ValueError as e:
        assert str(e) == "Only single characters can be inserted.", "Multi-character insert edge case failed."

    # Delete out-of-range index
    try:
        fm_index.delete(10)
    except ValueError as e:
        assert str(e) == "Index out of range.", "Out-of-range delete edge case failed."

    print("All edge cases handled correctly!")

    print("\nAll test cases passed!")


if __name__ == "__main__":
    run_tests()
