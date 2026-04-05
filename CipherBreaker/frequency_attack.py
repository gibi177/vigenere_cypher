import string
from collections import Counter
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from VigenereCipher import VigenereCipher


FREQ_EN = {
  'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
  'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
  'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
  'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
  'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974,
  'z': 0.074
}


class FrequencyAttack:
  def __init__(self, ciphertext: str):
    self.ciphertext = ciphertext

  def _split_into_columns(self, key_length: int) -> list[str]:
    """
    Split ciphertext into key_length groups.
    Group i contains letters at positions i, i+key_length, i+2*key_length...
    """
    columns = ['' for _ in range(key_length)]
    index = 0

    for ch in self.ciphertext:
      if ch.isalpha():
        columns[index % key_length] += ch.lower()
        index += 1

    return columns

  def _shift_char(self, c: str, shift: int) -> str:
    """Shift a character backwards (Caesar decode) by shift."""
    return chr((ord(c) - ord('a') - shift) % 26 + ord('a'))

  def _caesar_decode(self, text: str, shift: int) -> str:
    """Decode a Caesar cipher with given shift."""
    return ''.join(self._shift_char(c, shift) for c in text)

  def _chi_square_score(self, text: str) -> float:
    """
    Chi-square test comparing observed frequencies vs expected English frequencies.
    Lower score means better match.
    """
    n = len(text)
    if n == 0:
      return float("inf")

    observed = Counter(text)
    score = 0.0

    for letter in string.ascii_lowercase:
      observed_count = observed.get(letter, 0)
      expected_count = FREQ_EN[letter] * n / 100.0
      score += ((observed_count - expected_count) ** 2) / expected_count

    return score

  def _recover_key(self, key_length: int) -> str:
    """
    Recover Vigenere key using chi-square frequency analysis.
    """
    columns = self._split_into_columns(key_length)
    recovered_key = ""

    for col in columns:
      best_shift = 0
      best_score = float("inf")

      for shift in range(26):
        decoded_col = self._caesar_decode(col, shift)
        score = self._chi_square_score(decoded_col)

        if score < best_score:
          best_score = score
          best_shift = shift

      recovered_key += chr(best_shift + ord('a'))

    return recovered_key

  def _english_word_score(self, text: str) -> int:
    """Score plaintext by counting common English words."""
    common_words = [" the ", " and ", " of ", " to ", " in ", " is ", " that ", " it "]
    t = text.lower()
    return sum(t.count(w) for w in common_words)

  def _improve_key(self, key: str) -> tuple[str, int]:
    """
    Refine key by greedy per-position substitution using word score.
    """
    best_key = key
    best_score = -1

    for i in range(len(key)):
      for c in string.ascii_lowercase:
        test_key = key[:i] + c + key[i + 1:]

        v = VigenereCipher()
        v.set_key(test_key)
        plaintext = v.decode(self.ciphertext)

        score = self._english_word_score(plaintext)

        if score > best_score:
          best_score = score
          best_key = test_key

    return best_key, best_score

  def break_cipher(self, key_length: int) -> tuple[str, str]:
    """
    Recover key and decrypt ciphertext.

    :param key_length: Estimated key length (e.g. from Kasiski).
    :return: Tuple of (recovered_key, plaintext).
    """
    key = self._recover_key(key_length)

    v = VigenereCipher()
    v.set_key(key)
    plaintext = v.decode(self.ciphertext)

    return key, plaintext

  def break_cipher_with_refinement(self, key_length: int) -> tuple[str, str, int]:
    """
    Recover key, then refine it using word score.

    :param key_length: Estimated key length.
    :return: Tuple of (improved_key, improved_plaintext, word_score).
    """
    key, _ = self.break_cipher(key_length)
    improved_key, score = self._improve_key(key)

    v = VigenereCipher()
    v.set_key(improved_key)
    improved_plaintext = v.decode(self.ciphertext)

    return improved_key, improved_plaintext, score


if __name__ == "__main__":
  cipher = """Pr ess xytph cmwwoni zq Sshpykvso, evl xzhbztpzdsi rlhoicpr lzpcm lzpywuk
              ez goecp gasctsz fj evl jtcs. Jltwryiy wwzxpysk atev dmop sfid lg lpopfz
              vpncbrepr aewpg vj lyqpiye tvvpdhz, ltorlr ecshwfcsz, eyo vlvztq kipog.
              Alp hwuh hswztpcsk xsccbks evl xcpsz, glcffmyr glgcphz sq evl tldh,
              dltws alp dhhvd lpvzp ekprvwsk ptvs kmdeoux wlbaicyg. Smqp avzpo ulrewm,
              fie xmzxpcwlw wtbnicpr, detewuk qzf zsxpcui mcoci pycbks ec brnzjlv esst.
              Ilnv umrsh ivzfuox szdl eyo qbvtzgpxj tb luflz tildiyi."""

  key_length = 5

  fa = FrequencyAttack(cipher)

  print("=== Basic Attack ===")
  key, plaintext = fa.break_cipher(key_length)
  print(f"Recovered key: {key}")
  print(f"Plaintext:\n{plaintext}")

  print("\n=== Attack with Refinement ===")
  improved_key, improved_plaintext, score = fa.break_cipher_with_refinement(key_length)
  print(f"Improved key:  {improved_key} | word score: {score}")
  print(f"Plaintext:\n{improved_plaintext}")