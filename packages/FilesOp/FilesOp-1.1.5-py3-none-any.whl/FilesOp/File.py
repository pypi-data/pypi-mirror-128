from os.path import exists
import json

class FFile:
	"""Gestionale dei file"""
	nomeFile: str
	"""Nome del file da leggere"""

	json_: dict
	"""Contenuto del file decodificato in JSON"""

	string_: str
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
				self.string_ = fr.read()
			return self.string_
		else:
			print("File not exists")

	def read_json(self) -> None:
		"""Legge il JSON e lo decodifica"""
		if self.__file_exists():
			self.read_file()
			self.json_ = json.loads(self.string_)
			return self.json_
		else:
			print("File not exists")

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
		else:
			print("File not exists")