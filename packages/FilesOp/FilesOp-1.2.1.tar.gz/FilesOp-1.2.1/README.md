# FilesOp

Questo modulo permette di gestire i file come creali, leggerli e aggiornarli.
Utilizzabile **solo con il Python** e non ha dipendenze di altri moduli.

## Utilizzo
In python il modulo si importa così:
```python
from FilesOp import FFile

my_file = FFile("Nome.txt")
my_file.read_json() # Ritorna il JSON e lo salva dentro _json
print(my_file._json) # Si trova il JSON
# Se si legge il JSON automaticamente si ha anche il formato stringato del testo, non è necessario utilizzare la funzione read_file()
print(my_file._string) # Il contenuto del file formato stringa
```
### Links
Per avere ulteriori informazioni andare sul sito e vedere la documentazione completa del modulo.