import hashlib
import hmac
import os


class HMAC_DRBG ():
	def __init__ (self, entropy, security_strength=256):
		
		self.security_strength = security_strength
		self._instantiate (entropy)
	
	def _hmac (self, key, data):
		return hmac.new (key, data, hashlib.sha256).digest ()
	

	def _update (self, provided_data=None):
		self.Key = self._hmac (self.Key, self.Value + b"\x00" + (b"" if provided_data is None else provided_data))
		self.Value = self._hmac (self.Key, self.Value)

		if provided_data is not None:
			self.Key = self._hmac (self.Key, self.Value + b"\x01" + provided_data)
			self.Value = self._hmac (self.Key, self.Value)
	

	def _instantiate (self, entropy):
		seed_material = entropy

		self.Key = b"\x00" * 32
		self.Value = b"\x01" * 32

		self._update (seed_material)
		self.reseed_counter = 1
	
	
	def reseed (self, entropy):
		self._update (entropy)
		self.reseed_counter = 1
	

	def generate (self, num_bytes):
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
