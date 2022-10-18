# Project in collaboration with Vikram Krishna

# Import Statements
import math
from hashlib import sha256
# Initialize 64 round constants
roundConstants = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

# First Step, set up the text for input into Secure Hashing Algorithm
def step1(inputText):
    # Step 1: Convert the input text into a list of bytes
    binaryTextArray = []
    inputText = bytearray(inputText, 'utf-8')
    for char in inputText:
        # temp = format(ord(char), '08b')
        temp = format(char, '08b')
        if len(temp) > 8:
            print(temp)
            # temp = temp[-8:]
        binaryTextArray.append(temp)
    bigEndianNumber = len(binaryTextArray) * 8

    # Step 2: Add the padding zeroes
    numZeroes = math.ceil(len(binaryTextArray)*8/512) * 512/8 - len(binaryTextArray) - 9
    binaryTextArray.append('10000000')
    for i in range(int(numZeroes)):
        binaryTextArray.append('00000000')

    # Step 3: Add the length of the message
    bigEndianBin = bin(bigEndianNumber)[2:]
    last8Bytes = str(bigEndianBin).zfill(64)

    for byte in range(8):
        binaryTextArray.append(last8Bytes[byte*8:(byte+1)*8])
    
    return binaryTextArray

def step2(binaryTextArray):
    # Step 2: Split the input text into 512-bit chunks
    chunks = []
    for i in range(0, len(binaryTextArray), 64):
        chunks.append(binaryTextArray[i:i+64])

    return chunks

def step3(chunk):
    # print()
    # print(chunk)
    # Step 3: Split the chunks into 16 32-bit words
    wordsPart = []
    for i in range(0, len(chunk), 4):
        temp = str(chunk[i]) + str(chunk[i+1]) + str(chunk[i+2]) + str(chunk[i+3])
        wordsPart.append(temp)

    return wordsPart


def step4(words):
    # Step 4: Add 48 more words initialized to zero to the end of the list
    for i in range(16, 64):
        words.append('0' * 32)
        
    return words

def rightRotate(ogString, numBits):
    # Little functions to do the right rotation
    return ogString[-numBits:] + ogString[:-numBits]

def rightShift(ogString, numBits):
    # Little functions to do the right shift
    return ('0' * numBits) + ogString[:-numBits]

def step5(words):
    # Step 5: Modify the zero'ed indexes at the end of the array using the following formula
    
    for i in range(16, 64):
        s0 = int(rightRotate(words[i-15], 7), 2) ^ int(rightRotate(words[i-15], 18), 2) ^ int(rightShift(words[i-15], 3), 2)
        s1 = int(rightRotate(words[i-2], 17), 2) ^ int(rightRotate(words[i-2], 19), 2) ^ int(rightShift(words[i-2], 10), 2)
        temp = int(words[i-16], 2) + s0 + int(words[i-7], 2) + s1
        temp = bin(temp)[2:]
        if len(temp) > 32:
            words[i] = temp[-32:]
        else:
            words[i] = temp.zfill(32)
        

    return words

def step6(words, hVals):
    # Compressing through iteration 
    a = bin(int(hVals[0], 2))[2:].zfill(32)
    b = bin(int(hVals[1], 2))[2:].zfill(32)
    c = bin(int(hVals[2], 2))[2:].zfill(32)
    d = bin(int(hVals[3], 2))[2:].zfill(32)
    e = bin(int(hVals[4], 2))[2:].zfill(32)
    f = bin(int(hVals[5], 2))[2:].zfill(32)
    g = bin(int(hVals[6], 2))[2:].zfill(32)
    h = bin(int(hVals[7], 2))[2:].zfill(32)

    for i in range(64):
        S1 = int(rightRotate(e, 6), 2) ^ int(rightRotate(e, 11), 2) ^ int(rightRotate(e, 25), 2)
        ch = (int(e, 2) & int(f, 2)) ^ ((int(e, 2) ^ 4294967295) & int(g, 2))
        temp1 = int(h, 2) + S1 + ch + int(words[i], 2) + int(roundConstants[i])
        temp1 = temp1 % (2**32)
        S0 = int(rightRotate(a, 2), 2) ^ int(rightRotate(a, 13), 2) ^ int(rightRotate(a, 22), 2)
        maj = (int(a, 2) & int(b, 2)) ^ (int(a, 2) & int(c, 2)) ^ (int(b, 2) & int(c, 2))
        temp2 = S0 + maj
        temp2 = temp2 % (2**32)
        h = g.zfill(32)
        g = f.zfill(32)
        f = e.zfill(32)
        e = bin((int(d, 2) + temp1) % (2**32))[2:].zfill(32)
        d = c.zfill(32)
        c = b.zfill(32)
        b = a.zfill(32)
        a = bin((temp1 + temp2) % (2**32))[2:].zfill(32)
    
    return [a, b, c, d, e, f, g, h]

def step7(varsList, hVals):

    h0 = bin((int(hVals[0], 2) + int(varsList[0], 2)) % (2**32))[2:].zfill(32)
    h1 = bin((int(hVals[1], 2) + int(varsList[1], 2)) % (2**32))[2:].zfill(32)
    h2 = bin((int(hVals[2], 2) + int(varsList[2], 2)) % (2**32))[2:].zfill(32)
    h3 = bin((int(hVals[3], 2) + int(varsList[3], 2)) % (2**32))[2:].zfill(32)
    h4 = bin((int(hVals[4], 2) + int(varsList[4], 2)) % (2**32))[2:].zfill(32)
    h5 = bin((int(hVals[5], 2) + int(varsList[5], 2)) % (2**32))[2:].zfill(32)
    h6 = bin((int(hVals[6], 2) + int(varsList[6], 2)) % (2**32))[2:].zfill(32)
    h7 = bin((int(hVals[7], 2) + int(varsList[7], 2)) % (2**32))[2:].zfill(32)

    return [h0, h1, h2, h3, h4, h5, h6, h7]

def step8(finalVals):
    # Step 8: Convert the hash to a 32-character hexadecimal string
    hashString = ''
    for piece in finalVals:
        hashString += hex(int(piece, 2))[2:]
    return hashString


def runHash(inputText):
    shaInput = step1(inputText)
    chunks = step2(shaInput)
    # Hash Constants
    hVals = ['01101010000010011110011001100111', '10111011011001111010111010000101', '00111100011011101111001101110010', '10100101010011111111010100111010', '01010001000011100101001001111111', '10011011000001010110100010001100', '00011111100000111101100110101011', '01011011111000001100110100011001']

    for chunk in chunks:
        wordsPart = step3(chunk)
        wordsFull = step4(wordsPart)
        words = step5(wordsFull)
        varsList = step6(words, hVals)
        hVals = step7(varsList, hVals)
    hash = step8(hVals)
    return hash.zfill(64)

# Run each step
inputText = "KRISHNA, Vikram\nAP English Literature and Composition (P6)\nMs. Sarah Wheatley\n2005 AP Lit Free-Response Questions\nThere are often various sentiments that can lead the reader to draw conclusions on their own. The way that characters are described can make or break the success in conveying the intended message to the reader. In this passage, the author uses extremely visual and evocative descriptions, a neutral tone, and minute details to portray their attitude toward McTeague as one of both awe and pity.\nIn the very beginning, the author provides a very abrupt narrative about how McTeague got into his line of work. There isn’t much description here, only that his mother died and left him some money to open his parlor. This lack of detail provides a strong contrast as to when the author begins describing McTeague’s build in line eleven. It shows that the circumstance isn’t important, but rather the current situation is something that the reader needs to recognize and understand in great depth.\nWhen the author describes McTeague though, he uses a lot of visual descriptions. For example, he says ‘shock of blonde hair’ (line 12), ‘heavy with ropes of muscle’ (line 14), and describes his hands as being ‘hard as wooden mallets, strong as vises’ (lines 16-17). Here, the authors use of metaphors becomes extremely clear. They are trying to enable the reader to visualize McTeague, showing him as this hulking figure that would, to many people, be intimidating. But quickly, the author ensures to disperse this misconception, saying ‘there was nothing vicious about the man’ (lines 23-24). This is especially important for the work that he does. Being a dentist requires a lot of precision and can turn quite painful with the wrong intentions. However, by dispelling this myth that the reader may have built up when reading McTeague’s description, he juxtaposes the idea of a giant hunkering man bending over and delicately working on his patients’ teeth. The idea has a sentiment of awe, showing through various metaphors that even though he may not be naturally suited to his line of work, and could probably earn a lot more money using his physical stature for other jobs, he is so passionate about dentistry that he continues dedicating himself to it.\nBeyond this though, the author portrays a slight sense of pity when continuing to discuss McTeague’s work. They effectively portray how McTeague’s place barely warrants being called a parlor, and how he is forced to ‘[make] it do for a bedroom as well’. It becomes immediately clear that McTeague was not well endowed. Even when it comes to the furnishing and decorations inside the parlor/bedroom, the author explains in excruciating detail how everything was either related to dentistry or gotten at a good price. All the chairs were ‘a bargain at a second-hand store’ (line 37), the figures of Lorenzo de’ Medici were bought ‘because there were a great many figures in it for the money’ (lines 40-42), and the calendar he uses was even provided to him for free as an advertisement. Aside from this, he has a table covered with the American system of dentistry, and the ‘seven volumes of “Allen’s Practical Dentist”, portraying a very bland lifestyle where McTeague indulges in nothing but his work. All these various aspects, explained in great detail, add up to portray a tone of slight condescension and pity. The author successfully manages to show McTeague as a character that conforms to the stereotype of a ‘gentle giant’ who may not be the brightest person.\nHowever, the author continues beyond this, explaining what McTeague is working towards—his goal in all this. This is where the limited-view third person narrator becomes especially important. The narrator can understand McTeague’s motivations, and what he is striving towards, which in this case is a ‘huge, gilded tooth’ (line 58) in the window of his parlor. Although seemingly materialistic, the reader knows from previous descriptions that McTeague is not one for material wealth. Rather, the gilded tooth desire acts as a representation of legitimacy. He has just started his clinic, presumably as a no-name person serving no-name people. As he continues his work and builds up his reputation, he will not only be able to afford such luxuries but will also have earned the right to display the proof of his perseverance. The ‘American Dream’ takes shape in many ways, and in the case of McTeague, it is to legitimize himself as a dentist and become successful. In the future when he does buy and put up that gilded tooth, he will know that he has made it. Through this, the author returns to a sentiment of awe. They have managed to show McTeague as this simple person with great ambitions, but also as a person who can serve as a role-model for many, guiding them to not chase material wealth but seek happiness. With the combination of metaphors and precise details, the author can successfully use their tones of inspiration and condescension to convey this message to the reader."
# inputText = inputText.replace('“','"').replace('”','"').replace("’", "'").replace("‘", "'").replace('—', '-')

print(inputText.encode())
print(runHash(inputText))
print((sha256((inputText).encode())).hexdigest())