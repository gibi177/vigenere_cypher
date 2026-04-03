class VigenereCipher:

  def __init__(self):
    self.key = None

  def set_key(self, key: str):
    """Public method to set the key, which is used for both encoding and decoding"""

    if not key.isalpha():
      raise ValueError("Key must be a string of alphabetic characters")
    self.key = key.lower()

  forward_mapping = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
    'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
    'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14,
    'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19,
    'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24,
    'z': 25
}
  reverse_mapping = {v: k for k, v in forward_mapping.items()}
  
  def _get_new_char(self, text_char: str, key_char: str, mode: str) -> str:
    """Helper method to get the new character based on the mode (encode or decode)"""

    text_char_value = self.forward_mapping.get(text_char) # May be the message char or the key char, depending on the mode
    key_char_value = self.forward_mapping.get(key_char)

    if mode == 'encode':
      new_char_value = (text_char_value + key_char_value) % 26 
      new_char = self.reverse_mapping.get(new_char_value)
    elif mode == 'decode':
      new_char_value = (text_char_value - key_char_value) % 26
      new_char = self.reverse_mapping.get(new_char_value)

    return new_char

  def _transform(self, message: str, mode: str) -> str:
    """Main method used to transform the message based on the mode"""

    # Check mode and key before processing
    if mode not in ['encode', 'decode']:
      raise ValueError("Mode must be either 'encode' or 'decode'")
    if self.key is None:
      raise ValueError("Key must be set before encoding")

    result = ""
    key_index = 0
    for ch in message:

      if ch.lower() not in self.forward_mapping:
        result += ch
        continue

      is_upper = ch.isupper()
      if is_upper:
        ch = ch.lower()

      key_char = self.key[key_index]
      new_character = self._get_new_char(ch, key_char, mode)

      key_index += 1
      if key_index >= len(self.key):
        key_index = 0

      if is_upper:
        new_character = new_character.upper()

      result += new_character 

    return result
  
  def encode(self, message: str) -> str:
    """Encodes the message using the Vigenere cipher"""
    return self._transform(message, mode = 'encode')

  def decode(self, message: str) -> str:
    """Decodes the message using the Vigenere cipher"""
    return self._transform(message, mode = 'decode')


if __name__ == "__main__":

  encoder_decoder = VigenereCipher()
  encoder_decoder.set_key("abc")

  message = "abczz"
  encoded_message = encoder_decoder.encode(message)
  assert (encoded_message == "aceza")
  print(f"Encoded message: {encoded_message}")

  decoded_message = encoder_decoder.decode(encoded_message)
  assert (decoded_message == message)
  print(f"Decoded message: {decoded_message}")

  assert message == decoded_message


  # Additional test with a longer message

  encoder_decoder.set_key("hello")
  message = """In the quiet village of Eldenwood, the townspeople gathered every evening
                    to share stories by the fire. Children listened with wide eyes as elders
                    recounted tales of ancient forests, hidden treasures, and heroic deeds.
                    The wind whispered through the trees, carrying secrets of the past,
                    while the stars above twinkled like distant lanterns. Life moved gently,
                    yet mysteries lingered, waiting for someone brave enough to uncover them.
                    Each night brought hope and curiosity in equal measure."""

  encoded_message = encoder_decoder.encode(message)
  print(f"Encoded message: {encoded_message}")
  decoded_message = encoder_decoder.decode(encoded_message)
  print(f"Decoded message: {decoded_message}")
  assert message == decoded_message