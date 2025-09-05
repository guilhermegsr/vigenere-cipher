import string
from collections import Counter

class VigenereAnalyser:
    def __init__(self, ciphertext: str, language: str = "pt"):
        """
        Initialize the analyser with the ciphertext and the target language.

        Args:
            ciphertext (str): Encrypted text (only alphabetic characters will be considered).
            language (str): 'pt' for Portuguese or 'en' for English (affects frequency analysis).
        """
        # Keep only uppercase alphabetic characters from ciphertext
        self.ciphertext = ''.join([c for c in ciphertext.upper() if c.isalpha()])
        self.alphabet = string.ascii_uppercase
        self.mod = len(self.alphabet)

        # Expected letter frequencies (normalized) for Portuguese and English
        if language == "pt":
            # Source: Portuguese letter frequencies (Wikipedia)
            self.expected_freqs = {
                'A': 0.1463, 'B': 0.0104, 'C': 0.0388, 'D': 0.0499,
                'E': 0.1257, 'F': 0.0102, 'G': 0.0130, 'H': 0.0078,
                'I': 0.0618, 'J': 0.0039, 'K': 0.0002, 'L': 0.0278,
                'M': 0.0474, 'N': 0.0505, 'O': 0.1073, 'P': 0.0252,
                'Q': 0.0120, 'R': 0.0653, 'S': 0.0781, 'T': 0.0434,
                'U': 0.0463, 'V': 0.0167, 'W': 0.0001, 'X': 0.0021,
                'Y': 0.0001, 'Z': 0.0047,
            }
        else:
            # Source: English letter frequencies (Wikipedia)
            self.expected_freqs = {
                'A': 0.0817, 'B': 0.0149, 'C': 0.0278, 'D': 0.0425,
                'E': 0.1270, 'F': 0.0223, 'G': 0.0202, 'H': 0.0609,
                'I': 0.0697, 'J': 0.0015, 'K': 0.0077, 'L': 0.0403,
                'M': 0.0241, 'N': 0.0675, 'O': 0.0751, 'P': 0.0193,
                'Q': 0.0010, 'R': 0.0599, 'S': 0.0633, 'T': 0.0906,
                'U': 0.0276, 'V': 0.0098, 'W': 0.0236, 'X': 0.0015,
                'Y': 0.0197, 'Z': 0.0007,
            }

    # -------------------------------------------------------------------
    # Step 1: Estimate key length using Index of Coincidence (IC)
    # -------------------------------------------------------------------
    def _index_of_coincidence(self, text: str) -> float:
        """
        Calculate the Index of Coincidence (IC) for a given text.
        IC is higher (~0.065 for natural language) than for random text (~0.038).

        Args:
            text (str): Text to compute IC for.

        Returns:
            float: Index of Coincidence.
        """
        N = len(text)
        freqs = Counter(text)
        ic = sum(f * (f - 1) for f in freqs.values()) / (N * (N - 1)) if N > 1 else 0
        return ic

    def estimate_key_length(self, max_len: int = 20) -> int:
        """
        Estimate the most probable key length by calculating the IC
        for different candidate lengths.

        Args:
            max_len (int): Maximum key length to test.

        Returns:
            int: Estimated key length.
        """
        results = {}
        # For each possible key length, split ciphertext into columns
        for key_len in range(1, max_len + 1):
            ic_values = []
            for i in range(key_len):
                column = self.ciphertext[i::key_len]  # every i-th letter
                ic_values.append(self._index_of_coincidence(column))
            # Average IC for this key length
            results[key_len] = sum(ic_values) / len(ic_values)

        # Save results for reporting
        self.key_length_scores = results

        # Choose the key length with the highest average IC
        best_len = max(results, key=results.get)
        return best_len

    # -------------------------------------------------------------------
    # Step 2: Recover key using frequency analysis + chi-squared test
    # -------------------------------------------------------------------
    def _chi_squared(self, observed_freqs):
        """
        Compute chi-squared statistic between observed and expected frequencies.

        Args:
            observed_freqs (Counter): Letter frequency distribution from text.

        Returns:
            float: Chi-squared score (lower = better fit).
        """
        chi = 0
        total = sum(observed_freqs.values())
        for letter in self.alphabet:
            expected = self.expected_freqs.get(letter, 0) * total
            observed = observed_freqs.get(letter, 0)
            chi += (observed - expected) ** 2 / expected if expected > 0 else 0
        return chi

    def recover_key(self, key_len: int) -> str:
        """
        Recover the key by analyzing each column separately.
        Each column corresponds to Caesar cipher with unknown shift.

        Args:
            key_len (int): Estimated key length.

        Returns:
            str: Recovered key (uppercase).
        """
        key = []
        # For each position in the key
        for i in range(key_len):
            column = self.ciphertext[i::key_len]
            best_shift = None
            best_score = float('inf')

            # Try all possible shifts (A-Z)
            for shift in range(self.mod):
                shifted_text = ''.join(
                    self.alphabet[(ord(c) - ord('A') - shift) % self.mod] for c in column
                )
                freqs = Counter(shifted_text)
                score = self._chi_squared(freqs)

                if score < best_score:
                    best_score = score
                    best_shift = shift

            # The best shift corresponds to the key letter
            key.append(self.alphabet[best_shift])
        return ''.join(key)

    # -------------------------------------------------------------------
    # Step 3: Full attack (estimate key length + recover key)
    # -------------------------------------------------------------------
    def analyse(self, max_len: int = 20) -> str:
        """
        Perform the full attack:
        - Estimate key length
        - Recover the key

        Args:
            max_len (int): Maximum key length to test.

        Returns:
            str: Recovered key.
        """
        est_len = self.estimate_key_length(max_len)
        key = self.recover_key(est_len)
        return key
