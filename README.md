# SHA256 From Scratch

This is a from scratch implementation of the SHA256 (Secure Hash Algorithm 256-bit) algorithm. The algorithm takes an input text and produces a 64-character hexadecimal hash value.

## Features

- Converts input text into a binary array
- Adds padding zeroes to the binary array
- Splits the binary array into 512-bit chunks
- Divides each chunk into 16 32-bit words
- Adds 48 more words initialized to zero to the end of the list
- Modifies the zeroed indexes using specific formulas
- Compresses the words through iteration
- Converts the final values into a hash string

## Code Example

```python
import math
from hashlib import sha256

# Initialize 64 round constants
roundConstants = [0x428a2f98, 0x71374491, 0xb5c0fbcf, ...]

# Functions for each step of the algorithm...

def runHash(inputText):
    # Step 1: Convert input text into binary array
    shaInput = step1(inputText)

    # Step 2: Split binary array into 512-bit chunks
    chunks = step2(shaInput)

    # Hash Constants
    hVals = ['01101010000010011110011001100111', ...]

    # Process each chunk
    for chunk in chunks:
        wordsPart = step3(chunk)
        wordsFull = step4(wordsPart)
        words = step5(wordsFull)
        varsList = step6(words, hVals)
        hVals = step7(varsList, hVals)

    # Step 8: Convert the hash to a 32-character hexadecimal string
    hash = step8(hVals)
    return hash.zfill(64)

# Run the algorithm
inputText = "..."  # Your input text here
print(runHash(inputText))
```

## Usage

1. Import the necessary modules:

```python
import math
from hashlib import sha256
```

2. Copy the functions for each step of the algorithm.

3. Use the `runHash(inputText)` function to calculate the hash value of your input text:

```python
inputText = "..."  # Your input text here
print(runHash(inputText))
```

The output will be a 64-character hexadecimal hash value.
