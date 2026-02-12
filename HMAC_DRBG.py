import hashlib
import hmac
import os


class HMAC_DRBG ():
	"""
	Générateur de Nombres Pseudo-Aléatoires Déterministe basé sur HMAC (HMAC-DRBG).
	
	Implémente le Deterministic Random Bit Generator spécifié dans NIST SP 800-90A,
	utilisant HMAC-SHA256 comme base cryptographique pour générer des nombres aléatoires
	de haute qualité à partir d'une entropie initiale.
	"""
	def __init__ (self, entropy, security_strength=256):
		"""
		Initialise le générateur HMAC-DRBG avec une entropie.
		
		Args:
			entropy (bytes): Entropie initiale pour initialiser le générateur
			security_strength (int): Niveau de force de sécurité en bits (par défaut 256)
		"""
		
		self.security_strength = security_strength
		self._instantiate (entropy)
	
	def _hmac (self, key, data):
		"""
		Calcule le HMAC-SHA256 d'une donnée avec une clé.
		
		Args:
			key (bytes): Clé HMAC
			data (bytes): Données à authentifier
		
		Returns:
			bytes: Digest HMAC-SHA256 (32 bytes)
		"""
		return hmac.new (key, data, hashlib.sha256).digest ()
	

	def _update (self, provided_data=None):
		"""
		Met à jour l'état interne Key et Value du générateur.
		
		Processus de mise à jour DRBG pour intégrer des données optionnelles
		dans l'état interne du générateur.
		
		Args:
			provided_data (bytes, optional): Données supplémentaires à intégrer (None par défaut)
		
		Returns:
			None
		"""
		self.Key = self._hmac (self.Key, self.Value + b"\x00" + (b"" if provided_data is None else provided_data))
		self.Value = self._hmac (self.Key, self.Value)

		if provided_data is not None:
			self.Key = self._hmac (self.Key, self.Value + b"\x01" + provided_data)
			self.Value = self._hmac (self.Key, self.Value)
	

	def _instantiate (self, entropy):
		"""
		Initialise l'état interne du générateur avec l'entropie fournie.
		
		Configure les valeurs initiales Key et Value, puis effectue la mise à jour
		avec l'entropie pour établir l'état initial.
		
		Args:
			entropy (bytes): Entropie pour l'initialisation
		
		Returns:
			None
		"""
		seed_material = entropy

		self.Key = b"\x00" * 32
		self.Value = b"\x01" * 32

		self._update (seed_material)
		self.reseed_counter = 1
	
	
	def reseed (self, entropy):
		"""
		Re-initialise l'état interne du générateur avec une nouvelle entropie.
		
		Utile pour rafraîchir l'aléatoire du générateur avec une nouvelle entropie
		et pour respecter les recommandations de reseed périodique.
		
		Args:
			entropy (bytes): Nouvelle entropie pour le reseed
		
		Returns:
			None
		"""
		self._update (entropy)
		self.reseed_counter = 1
	

	def generate (self, num_bytes):
		"""
		Génère des nombres aléatoires de longueur spécifiée.
		
		Produit une séquence de num_bytes octets aléatoires en utilisant l'état
		interne du générateur, puis met à jour l'état pour la prochaine génération.
		
		Args:
			num_bytes (int): Nombre d'octets aléatoires à générer
		
		Returns:
			bytes: Séquence de num_bytes octets aléatoires
		"""
		temp = b""

		while len (temp) < num_bytes:
			self.Value = self._hmac (self.Key, self.Value)
			temp += self.Value

		self._update (None)
		self.reseed_counter += 1

		return temp[:num_bytes]

if __name__ == "__main__":
	drbg = HMAC_DRBG (entropy=os.urandom (64))
	secret = drbg.generate (1000)


	print(secret)
