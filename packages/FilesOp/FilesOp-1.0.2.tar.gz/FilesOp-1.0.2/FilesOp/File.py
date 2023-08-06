from os.path import exists
import json

class File:
	"""Gestionale dei file"""
	nomeFile: str
	"""Nome del file da leggere"""

	_json: dict
	"""Contenuto del file decodificato in JSON"""

	_string: str
	"""Contenuto del file in Stringa"""

	def __init__(self, nomeFile) -> None:
		self.nomeFile = nomeFile

	def __file_exists(self) -> bool:
		"""Verifica se il file esiste"""
		if exists(self.nomeFile):
			return True
		else:
			return False

	def read_file(self) -> None:
		"""Legge il file"""
		if self.__file_exists():
			with open(self.nomeFile, 'r') as fr:
				self._string = fr.read()

	def read_json(self) -> None:
		"""Legge il JSON e lo decodifica"""
		if self.__file_exists():
			self._json = json.loads(self.read_file())

	def create_file(self, content, override=True) -> None:
		"""Scrive un nuovo file"""
		if override:
			with open(self.nomeFile, "w") as fw:
				fw.write(content)
		else:
			with open(self.nomeFile, "x") as fw:
				fw.write(content)

	def append_to_file(self, content) -> None:
		"""Aggiungi alla fine del file il contenuto"""
		if self.__file_exists():
			with open(self.nomeFile, "a") as fa:
				fa.write(content)


def main():
	NomeFile = input("Nome del file: ")
	F = File(NomeFile)