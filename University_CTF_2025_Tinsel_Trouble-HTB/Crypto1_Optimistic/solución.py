import string
import hashlib
import ast
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from collections import defaultdict

with open('ubicación del archivo de texto\\output.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith('PEPPERMINT_KEYWORD'):
            PEPPERMINT_KEYWORD = ast.literal_eval(line.split('=')[1].strip())
        elif line.startswith('PEPPERMINT_CIPHERTEXT'):
            PEPPERMINT_CIPHERTEXT = ast.literal_eval(line.split('=')[1].strip())
        elif line.startswith('WRAPPED_STARSHARD'):
            WRAPPED_STARSHARD = ast.literal_eval(line.split('=')[1].strip())

CANDYCANE_ALPHABET = string.ascii_uppercase + string.digits
SZ = 6

def weave_peppermint_square():
    peppermint_square_flat = CANDYCANE_ALPHABET
    for c in PEPPERMINT_KEYWORD:
        peppermint_square_flat = peppermint_square_flat.replace(c, '')
    peppermint_square_flat = PEPPERMINT_KEYWORD + peppermint_square_flat
    return [list(peppermint_square_flat[i:i+SZ]) for i in range(0, len(peppermint_square_flat), SZ)]

peppermint_square = weave_peppermint_square()

BAUBLE_COORDS = {
    peppermint_square[i][j]: f'{i+1}{j+1}'
    for j in range(SZ)
    for i in range(SZ)
}

ct = PEPPERMINT_CIPHERTEXT
n = len(ct)
key_len = 36

ct_by_key_pos = defaultdict(list)
for i in range(n):
    ct_by_key_pos[i % key_len].append(ct[i])

def score_plaintext_chars(chars):
    return sum(10 for c in chars if c.isalpha()) + sum(1 for c in chars if c.isdigit())

COORDS_TO_CHAR = {v: k for k, v in BAUBLE_COORDS.items()}

best_key = [''] * key_len
for key_pos in range(key_len):
    best_score = -1
    best_char = None
    for key_char in CANDYCANE_ALPHABET:
        key_val = int(BAUBLE_COORDS[key_char])
        plaintext_chars = []
        valid = True
        for ct_val in ct_by_key_pos[key_pos]:
            pt_val = ct_val - key_val
            pt_coord = str(pt_val)
            if len(pt_coord) == 2 and pt_coord in COORDS_TO_CHAR:
                plaintext_chars.append(COORDS_TO_CHAR[pt_coord])
            else:
                valid = False
                break
        if valid:
            score = score_plaintext_chars(plaintext_chars)
            if score > best_score:
                best_score = score
                best_char = key_char
    if best_char:
        best_key[key_pos] = best_char

test_key = ''.join(best_key)
plaintext_chars = []
for i in range(n):
    key_char = test_key[i % key_len]
    key_val = int(BAUBLE_COORDS[key_char])
    pt_val = ct[i] - key_val
    pt_coord = str(pt_val)
    plaintext_chars.append(COORDS_TO_CHAR[pt_coord])

plaintext = ''.join(plaintext_chars)
COCOA_AES_KEY = hashlib.sha256(plaintext.encode()).digest()
cipher = AES.new(COCOA_AES_KEY, AES.MODE_ECB)
decrypted = unpad(cipher.decrypt(bytes.fromhex(WRAPPED_STARSHARD)), 16)
print(decrypted.decode())