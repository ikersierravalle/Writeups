
# Optimistic

## 📌 Descripción
**Categoría:** Cryptography 

**Dificultad:** Very easy

**Enunciado:** In Tinselwick's first magical mishap, Lottie Thimblewhisk discovers a strange peppermint-coded message 
whose enchanted structure hides something far more important. This challenge explores a festive ciphering mechanism 
and a seasonally wrapped secret. Your first step in uncovering what happened to the wandering Starshard.

## 🛠️ Análisis del código
Lo primero que hice fue analizar los dos archivos que nos daban, **source.py** y **output.txt**. En el archivo de texto nos 
dan 3 cosas: **PEPPERMINT_KEYWORD**, **PEPPERMINT_CIPHERTEXT** y **WRAPPED_STARSHARD**. Estos nos van a ser de ayuda para encontrar 
la flag. En el archivo de python vemos que función tiene lo que nos han dado.

```python
FESTIVE_WHISPER_CLEAN = re.sub(r'[^a-zA-Z0-9]', '', FESTIVE_WHISPER_CLEAN).upper()
CANDYCANE_ALPHABET = string.ascii_uppercase + string.digits
SZ = 6
L = SZ**2

def weave_peppermint_square():
    peppermint_square_flat = CANDYCANE_ALPHABET
    for c in PEPPERMINT_KEYWORD:
        peppermint_square_flat = peppermint_square_flat.replace(c, '')
    peppermint_square_flat = PEPPERMINT_KEYWORD + peppermint_square_flat
    return [list(peppermint_square_flat[i:i+SZ]) for i in range(0, len(peppermint_square_flat), SZ)]

peppermint_square = weave_peppermint_square()
```

En este fragmento de código podemos ver que se crea un **CANDYCANE_ALPHABET**, que es un string con las letras del abecedario
en mayúsucla (sin la ñ) y los números del 0 al 9, por lo que tendrá una longitud de 36 carácteres. Después se crea 
**peppermint_square** con una función que devuelve una matriz 6x6 con esta información:

```python
peppermint_square = [
    ['A', 'R', '4', 'N', 'D', '0'],
    ['M', 'K', '3', 'Y', 'B', 'C'],
    ['E', 'F', 'G', 'H', 'I', 'J'],
    ['L', 'O', 'P', 'Q', 'S', 'T'],
    ['U', 'V', 'W', 'X', 'Z', '1'],
    ['2', '5', '6', '7', '8', '9']
]
```

Después vemos como se encripta la información con estas funciones:

```python
BAUBLE_COORDS = {
    peppermint_square[i][j]: f'{i+1}{j+1}'
    for j in range(SZ)
    for i in range(SZ)
}

def swirl_encrypt(starstream_key, starlit_plaintext):
    twinkling_ct = []
    for i in range(len(starlit_plaintext)):
        key_off = int(BAUBLE_COORDS[starstream_key[i % len(starstream_key)]])
        pt_off = int(BAUBLE_COORDS[starlit_plaintext[i]])
        twinkling_ct.append(key_off + pt_off)
    return twinkling_ct

STARSTREAM_KEY = ''.join(random.sample(CANDYCANE_ALPHABET, k=L))
PEPPERMINT_CIPHERTEXT = swirl_encrypt(STARSTREAM_KEY, FESTIVE_WHISPER_CLEAN)
```

BAUBLE_CORDS es simplemente un diccionario con las coordenadas para cada elemento de la matriz. Estas coordenadas van 
desde el 11 (Para la primera letra de la primera fila) hasta el 66 (para la sexta letra de la sexta fila). Después vemos
cómo se genera **STARSTREAM_KEY**, que será un string con una combinación aleatoria de nuestro **CANDYCANE_ALPHABET**. 
Esta vez no sabemos que KEY se ha usado para cifrar nuestro mensaje. Después se usa **swirl_encrypt** para encriptar
el mensaje. Esta función crea **key_off** y **pt_off** y devuelve la suma. Veamos como se crea cada una. 

Para calcular **key_off** se calcula la coordenada de la letra que hay en la posición i%len(starstream_key), es decir,
una y otra vez del 1 al 36. Esto nos dice que esta variable será la misma cada 36 posiciones. 

Para calcular **pt_off** se calcula la coordenada de la letra del texto que se quiere encriptar.

```python
COCOA_AES_KEY = hashlib.sha256(FESTIVE_WHISPER_CLEAN.encode()).digest()
WRAPPED_STARSHARD = AES.new(COCOA_AES_KEY, AES.MODE_ECB).encrypt(pad(STARSHARD_SCROLL, 16)).hex()

open('output.txt', 'w').write(f'{PEPPERMINT_KEYWORD = }\n{PEPPERMINT_CIPHERTEXT = }\n{WRAPPED_STARSHARD = }')
```

Por último, vemos cómo se obtiene el **WRAPPED_STARSHARD**. Primero se genera una clave AES a partir del hash SHA‑256 
del texto limpio FESTIVE_WHISPER_CLEAN, lo que garantiza una longitud fija y segura para la clave (32 bytes). Después, 
se cifra el contenido **STARSHARD_SCROLL** usando AES en modo ECB, aplicando padding para ajustarlo al tamaño de bloque y 
finalmente convirtiendo el resultado a hexadecimal. Con esto, si conseguimos el texto limpio, podremos sacar **STARSHARD_SCROLL**.

## Enfoque del resultado
El primer paso va a ser pasar toda la información del archivo de texto a nuestro programa. Después, intentaremos calcular cual ha sido
la el orden del alfabeto correcto mediante una función. Esta función es la siguiente:

```python
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
```

Esta función prueba todas las letras y comprueba primero si el valor que obtenemos es uno de las coordenadas. Después, le daremos
una puntuación a cada letra candidata, dándole más valor a las letras que a los números, porque suponemos que el mensaje son 
mayoritariamente letras. 

Después de esto, conseguiremos el valor de best_key = "['N', 'M', '8', 'Y', '7', 'J', 'W', 'L', '1', 'T', 'S', 'E', 'P', '3', '9', 'U',
'X', 'C', '6', 'R', '5', 'O', 'A', '2', 'G', '0', 'H', '4', 'I', 'D', 'Z', 'B', 'V', 'Q', 'K', 'F']". Una vez tenemos la clave que se
ha utilizado para cifrar y vemos que ningún valor se repite, que con esta función podría ser, podemos descifrar el texto completo. 

Una vez tenemos el texto plano o plaintext, podemos conseguir la bandera.

```python
COCOA_AES_KEY = hashlib.sha256(plaintext.encode()).digest()
cipher = AES.new(COCOA_AES_KEY, AES.MODE_ECB)
decrypted = unpad(cipher.decrypt(bytes.fromhex(WRAPPED_STARSHARD)), 16)
```

Este fragmento descifra el contenido cifrado **WRAPPED_STARSHARD** utilizando AES. Primero se deriva la clave simétrica calculando el 
hash SHA‑256 del texto original (plaintext), lo que garantiza una longitud segura de 256 bits para AES. Luego se crea un objeto 
cifrador en modo ECB, que cifra y descifra bloques de 16 bytes sin usar IV (Vector de Inicialización) y se aplica la operación 
inversa sobre el texto cifrado convertido desde hexadecimal. Finalmente, se elimina el padding PKCS#7 (por defecto) para recuperar el 
**STARSHARD_SCROLL**. Comprender este proceso es clave porque muestra cómo se genera la clave, cómo funciona el cifrado y por qué el 
modo ECB, al no añadir aleatoriedad, permite revertir el cifrado si se conoce la clave. 

## 🎯 Flag
`HTB{ejemplo_de_flag}`


