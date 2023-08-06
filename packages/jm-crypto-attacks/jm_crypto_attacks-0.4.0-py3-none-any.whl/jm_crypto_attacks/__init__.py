__version__ = '0.4.0'

class MyAttacks:

  def engProbDist(self):
    prob_dist = {'A': 0.082, 'B': 0.015,
                 'C': 0.028, 'D': 0.043,
                 'E': 0.127, 'F': 0.022,
                 'G': 0.020, 'H': 0.061,
                 'I': 0.070, 'J': 0.002,
                 'K': 0.008, 'L': 0.040,
                 'M': 0.024, 'N': 0.067,
                 'O': 0.075, 'P': 0.019,
                 'Q': 0.001, 'R': 0.060,
                 'S': 0.063, 'T': 0.091,
                 'U': 0.028, 'V': 0.010,
                 'W': 0.023, 'X': 0.001,
                 'Y': 0.020, 'Z': 0.001}
    return prob_dist

  def bruteCaesarDec(self, ct, key):
    print("Now trying key: ", key)
    pt = ""
    for letter in ct:
      o = ord(letter)
      if letter.isupper():
        idx = ord(letter) - ord("A")
        pos = (idx - key) % 26 + ord("A")
        pt += chr(pos)
      elif letter.islower():
        idx = o - ord("a")
        pos = (idx - key) % 26 + ord("a")
        pt += chr(pos)
      elif letter.isdigit():
        pos = (int(letter) - key) % 10
        pt += str(pos)
      else:
        print("Not recognized")
    print("Plaintext: " + pt)
  
  def bruteVigenereDec(self, ct, keyLen):
    import collections

    n = len(ct)
    ct = ct.upper()

    # Get the English letter probability distribution
    prob_dist = self.engProbDist()
  
    # Calculate number streams given ciphertext and key_length
    nStreams = keyLen
    print("Number of streams: " + str(nStreams))

    # Initialize an array to hold the key digits
    key_digits = [0] * nStreams

    for i in range(0, nStreams):
      # Extract the stream
      stream = ct[i:n:keyLen]
      len_stream = len(stream)
      print()
      print("Stream #" + repr(i+1) + " = " + stream)
      print()
      freqs = collections.Counter(stream)
      print(freqs)
      # Loop through 'j' to test each key in the current stream
      for j in range(0,26):
        sum = 0.0
        # Loop through 'k' to test each character in the stream
        for k in range(0,26):
          orig = chr(ord('A') + k)
          shifted = chr(ord('A') + (k + j) % 26)
          sum += prob_dist[orig] * (float(freqs[shifted]) / len_stream)
        if sum >= 0.060:
          key_digits[i] = j
          print("----------------------------------------------")
          print("Key = " + str(j) + " -> " + chr(ord('A') + j))
          print("IC = " + str(sum))
          print("----------------------------------------------")
    return key_digits