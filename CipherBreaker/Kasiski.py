import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import factor

class Kasiski:
  def __init__(self, text: str):
    self.text = text

  def _clean_text(self) -> str:
    """
    Remove all non-alphabetic characters from the text and convert to lowercase.

    :return: A cleaned string containing only lowercase alphabetic characters.
    """
    result = ""

    for ch in self.text:
      if ch.isalpha():
        result += ch.lower()

    return result

  def _get_substrings(self, clean_text: str, length: int) -> list[str]:
    """
    Generate all substrings of a given length from the cleaned text.

    :param clean_text: The processed text containing only lowercase letters.
    :param length: Length of each substring.
    :return: A list of substrings.
    """
    substrings = []
    for i in range(len(clean_text) - length + 1):
      substrings.append(clean_text[i:i+length])

    return substrings

  def _substring_count(self, substrings: list[str]) -> dict[str, int]:
    """
    Count how many times each substring appears.

    :param substrings: List of substrings.
    :return: Dictionary mapping substring -> occurrence count.
    """
    substrings_count = {}

    for substring in substrings:
      if substring in substrings_count:
        substrings_count[substring] += 1
      else:
        substrings_count[substring] = 1

    return substrings_count

  def _repeated_substrings_positions(self, clean_text: str, substrings_count: dict[str, int]) -> dict[str, list[int]]:
    """
    Find positions of substrings that appear more than once.

    :param clean_text: The cleaned text.
    :param substrings_count: Dictionary of substring counts.
    :return: Dictionary mapping substring -> list of positions.
    """
    result = {} 

    for substring, count in substrings_count.items():
      if count > 1:

        positions = []
        start_index = 0
        while True:
          position = clean_text.find(substring, start_index)

          if position == -1:
            break
          else: 
            positions.append(position)
            start_index = position + 1
        
        result[substring] = positions # Add entry to the dictionary
    
    return result

  def _repeated_substrings_distances(self, substrings_positions: dict[str, list[int]]) -> dict[str, list[int]]:
    """
    Compute distances between consecutive occurrences of repeated substrings.

    :param substrings_positions: Dictionary mapping substring -> positions.
    :return: Dictionary mapping substring -> list of distances.
    """
    distances = {} 

    for substring, positions in substrings_positions.items():
      substring_distances = []
      for i in range(len(positions) - 1):
        distance = positions[i+1] - positions[i]
        substring_distances.append(distance)
      
      distances[substring] = substring_distances

    return distances

  def _factor_distances(self, distances: dict[str, list[int]]) -> list[int]:
    """
    Factor all distances of repeated substrings into their divisors.

    :param distances: Dictionary mapping substring -> list of distances.
    :return: A list containing all factors from all distances (may contain duplicates).
    """
    all_factors = []

    for dist_list in distances.values():
      for distance in dist_list:
        all_factors.extend(factor(distance)) # factor() comes from utils.py

    return [f for f in all_factors if f >= 3] # Filter out factors less than 3 -> unlikely key lengths


  def _likely_key_lengths(self, all_factors: list[int]) -> list[int]:
    """
    Rank candidate key lengths by frequency of occurrence among all distance factors.

    :param all_factors: List of all factors from distances.
    :return: List of likely key lengths, sorted by most frequent first.
             Returns an empty list if no repeated substrings were found.
    """
    freq = {}  

    for factor in all_factors:
      if factor in freq:
        freq[factor] += 1
      else:
        freq[factor] = 1

    if not freq:
      return []
      
    sorted_keys = sorted(freq, key=freq.get, reverse=True)
    return sorted_keys

  def find_key_lengths(self, substring_length: int) -> list[int]:
    """
    Perform the full Kasiski examination to generate candidate key lengths.

    :param substring_length: Length of substrings to analyze (typically 3 or more).
    :return: List of likely key lengths, ranked by frequency of occurrence.
    """

    clean = self._clean_text()
    substrings = self._get_substrings(clean, substring_length)
    counts = self._substring_count(substrings)
    positions = self._repeated_substrings_positions(clean, counts)
    distances = self._repeated_substrings_distances(positions)
    all_factors = self._factor_distances(distances)
    key_lengths = self._likely_key_lengths(all_factors)

    return key_lengths



if __name__ == "__main__":  
  true_key_length = 5
  true_key = "hello"

  true_message = """In the quiet village of Eldenwood, the townspeople gathered every evening
                    to share stories by the fire. Children listened with wide eyes as elders
                    recounted tales of ancient forests, hidden treasures, and heroic deeds.
                    The wind whispered through the trees, carrying secrets of the past,
                    while the stars above twinkled like distant lanterns. Life moved gently,
                    yet mysteries lingered, waiting for someone brave enough to uncover them.
                    Each night brought hope and curiosity in equal measure."""
  

  cipher_text = """Pr ess xytph cmwwoni zq Sshpykvso, evl xzhbztpzdsi rlhoicpr lzpcm lzpywuk
                    ez goecp gasctsz fj evl jtcs. Jltwryiy wwzxpysk atev dmop sfid lg lpopfz
                    vpncbrepr aewpg vj lyqpiye tvvpdhz, ltorlr ecshwfcsz, eyo vlvztq kipog.
                    Alp hwuh hswztpcsk xsccbks evl xcpsz, glcffmyr glgcphz sq evl tldh,
                    dltws alp dhhvd lpvzp ekprvwsk ptvs kmdeoux wlbaicyg. Smqp avzpo ulrewm,
                    fie xmzxpcwlw wtbnicpr, detewuk qzf zsxpcui mcoci pycbks ec brnzjlv esst.
                    Ilnv umrsh ivzfuox szdl eyo qbvtzgpxj tb luflz tildiyi."""  

  k = Kasiski(cipher_text)
  sequence_length = 4
  prob_key_lengths = k.find_key_lengths(sequence_length)
  print(f"Likely key lengths for sequence length {sequence_length}:")
  print(prob_key_lengths)
  