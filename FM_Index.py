from collections import defaultdict
from typing import List, Dict

class FMIndex:
    def __init__(self, text: str):
        """
        Initialize the FM Index for the given text.
        Adds a sentinel character '$' at the end of the text and constructs the
        suffix array, BWT, rank array, and C-table.
        """
        if not text:
            raise ValueError("Input text cannot be empty.")
        self.text = text + "$"  # Append sentinel character to the text
        self.suffix_array = self._build_suffix_array()  # Construct suffix array
        self.bwt = self._build_bwt()  # Construct Burrows-Wheeler Transform
        self.rank_array = self._build_rank_array()  # Build rank array for BWT
        self.c_table = self._build_c_table()  # Build C-table for character frequencies

    def _build_suffix_array(self) -> List[int]:
        """
        Construct the suffix array of the text.
        Each suffix is sorted lexicographically, and their starting indices
        are returned as the suffix array.
        """
        suffixes = [(self.text[i:], i) for i in range(len(self.text))]
        suffixes.sort()  # Sort suffixes lexicographically
        return [suffix[1] for suffix in suffixes]

    def _build_bwt(self) -> str:
        """
        Build the Burrows-Wheeler Transform (BWT) of the text using the suffix array.
        BWT is formed by taking the character preceding each suffix in the suffix array.
        """
        return "".join(self.text[i - 1] if i != 0 else "$" for i in self.suffix_array)

    def _build_rank_array(self) -> Dict[str, List[int]]:
        """
        Construct the rank array for the BWT.
        The rank array keeps track of the cumulative count of each character
        in the BWT up to each position.
        """
        rank = defaultdict(list)
        for char in sorted(set(self.bwt)):
            count = 0
            for c in self.bwt:
                if c == char:
                    count += 1
                rank[char].append(count)
        return rank

    def _build_c_table(self) -> Dict[str, int]:
        """
        Build the C-table for the BWT.
        The C-table stores the total number of occurrences of characters lexicographically
        less than the given character in the BWT.
        """
        sorted_chars = sorted(set(self.bwt))
        c_table = {}
        total = 0
        for char in sorted_chars:
            c_table[char] = total
            total += self.bwt.count(char)
        return c_table

    def search(self, pattern: str) -> List[int]:
        """
        Search for a pattern in the text using the FM Index.
        Returns the starting positions of all occurrences of the pattern.
        """
        if not pattern:
            raise ValueError("Search pattern cannot be empty.")

        l, r = 0, len(self.bwt) - 1  # Initialize the search range
        for char in reversed(pattern):  # Process the pattern from right to left
            if char not in self.c_table:
                return []  # Pattern character not in the text
            l = self.c_table[char] + (self.rank_array[char][l - 1] if l > 0 else 0)
            r = self.c_table[char] + self.rank_array[char][r] - 1
            if l > r:
                return []  # Pattern not found
        return sorted([self.suffix_array[i] for i in range(l, r + 1)])

    def insert(self, char: str):
        """
        Insert a single character at the end of the text.
        Rebuilds the FM Index after the insertion.
        """
        if len(char) != 1:
            raise ValueError("Only single characters can be inserted.")
        self.text = self.text[:-1] + char + "$"  # Update text with the new character
        self._rebuild()  # Rebuild the FM Index

    def delete(self, index: int):
        """
        Delete a character from the text at the specified index.
        Rebuilds the FM Index after the deletion.
        """
        if not (0 <= index < len(self.text) - 1):  # Exclude the sentinel character
            raise ValueError("Index out of range.")
        self.text = self.text[:index] + self.text[index + 1:]  # Remove character at index
        self._rebuild()  # Rebuild the FM Index

    def _rebuild(self):
        """
        Rebuild the FM Index components after an update to the text.
        """
        self.suffix_array = self._build_suffix_array()
        self.bwt = self._build_bwt()
        self.rank_array = self._build_rank_array()
        self.c_table = self._build_c_table()

# Example Usage
if __name__ == "__main__":
    text = "banana"
    fm_index = FMIndex(text)

    print("Text:", text)
    print("Suffix Array:", fm_index.suffix_array)
    print("BWT:", fm_index.bwt)
    print("Rank Array:", dict(fm_index.rank_array))
    print("C Table:", fm_index.c_table)

    # Searching for a pattern
    pattern = "ana"
    print(f"Searching for pattern '{pattern}':", fm_index.search(pattern))

    # Inserting a character
    fm_index.insert('s')
    print("After insertion:")
    print("Text:", fm_index.text)
    print("Suffix Array:", fm_index.suffix_array)
    print("BWT:", fm_index.bwt)

    # Deleting a character
    fm_index.delete(1)
    print("After deletion:")
    print("Text:", fm_index.text)
    print("Suffix Array:", fm_index.suffix_array)
    print("BWT:", fm_index.bwt)
