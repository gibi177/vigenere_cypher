class Kasiski:
  def __init__(self, text: str):
    self.text = text

  def _clean_text(self) -> str:
    result = ""

    for ch in self.text:
      if ch.isalpha():
        result += ch.lower()

    return result

  def _get_substrings(self, clean_text: str, length: int) -> list[str]:
    substrings = []
    for i in range(len(clean_text) - length + 1):
      substrings.append(clean_text[i:i+length])

    return substrings

  def _substring_count(self, substrings: list[str]) -> dict[str, int]:
    substrings_count = {} # Dictionary where keys are substrings and values are how many times that substring appears in the text

    for substring in substrings:
      if substring in substrings_count:
        substrings_count[substring] += 1
      else:
        substrings_count[substring] = 1

    return substrings_count

  def _repeated_substrings_positions(self, clean_text: str, substrings_count: dict[str, int]) -> dict[str, list[int]]:
    result = {} # Dictionary where keys are substrings and values are lists of positions where that substring appears in the text

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
    distances = {} # Dictionary where keys are substrings and values are lists of distances between the positions where that substring appears

    for substring, positions in substrings_positions.items():
      substring_distances = []
      for i in range(len(positions) - 1):
        distance = positions[i+1] - positions[i]
        substring_distances.append(distance)
      
      distances[substring] = substring_distances

    return distances

  def _distances_gcd(self, distances: dict[str, list[int]]) -> dict[str, int]:
    from math import gcd
    from functools import reduce
    
    gcds = {} # keys = substrings, values = GCD of distances
    for substring, substring_distances in distances.items():
      if len(substring_distances) > 0:
        gcd_value = reduce(gcd, substring_distances)
        gcds[substring] = gcd_value

    return gcds

  def _likely_key_length(self, distances_gcds: dict[str, int]) -> int:
    
    freq = {}  # key = GCD, value = count
    for gcd_value in distances_gcds.values():
      if gcd_value in freq:
        freq[gcd_value] += 1
      else:
        freq[gcd_value] = 1

    if not freq:
      return 0
      
    most_common_gcd = max(freq, key=freq.get)
    return most_common_gcd

  def find_key_length(self, substring_length: int) -> int:
    
    # 1. Clean the text
    clean = self._clean_text()

    # 2. Get all substrings of length substring_length
    substrings = self._get_substrings(clean, substring_length)

    # 3. Count how many times each substring appears
    counts = self._substring_count(substrings)

    # 4. Get positions of repeated substrings
    positions = self._repeated_substrings_positions(clean, counts)

    # 5. Calculate distances between repeated substrings
    distances = self._repeated_substrings_distances(positions)

    # 6. Compute GCDs of distances
    gcds = self._distances_gcd(distances)

    # 7. Determine most likely key length
    key_length = self._likely_key_length(gcds)

    return key_length
    


if __name__ == "__main__":  
  cipher_text = "Abcabcabc"
  k = Kasiski(cipher_text)
  prob_key = k.find_key_length(3)
  print(prob_key)
  
