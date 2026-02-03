import hashlib
import hmac
import os


# Implements an HMAC_DRBG (NIST SP 800-90A) based on HMAC_SHA256.
# Supports security strengths up to 256 bits.
# Parameters are based on recommendations provided by Appendix D of NIST SP 800-90A.
class HMAC_DRBG ():
	def __init__ (self, entropy, requested_security_strength=256, personalization_string=b""):
		
		self.security_strength = requested_security_strength
		self._instantiate (entropy, personalization_string)
	

	# Just for convenience and succinctness
	def _hmac (self, key, data):
		return hmac.new (key, data, hashlib.sha256).digest ()
	

	def _update (self, provided_data=None):
		self.K = self._hmac (self.K, self.V + b"\x00" + (b"" if provided_data is None else provided_data))
		self.V = self._hmac (self.K, self.V)

		if provided_data is not None:
			self.K = self._hmac (self.K, self.V + b"\x01" + provided_data)
			self.V = self._hmac (self.K, self.V)
	

	def _instantiate (self, entropy, personalization_string):
		seed_material = entropy + personalization_string

		self.K = b"\x00" * 32
		self.V = b"\x01" * 32

		self._update (seed_material)
		self.reseed_counter = 1
	
	
	def reseed (self, entropy):
		if (len (entropy) * 8) < self.security_strength:
			raise RuntimeError ("entropy must be at least %f bits." % (self.security_strength))

		if len (entropy) * 8 > 1000:
			raise RuntimeError ("entropy cannot exceed 1000 bits.")

		self._update (entropy)
		self.reseed_counter = 1
	

	def generate (self, num_bytes, requested_security_strength=256):
		if (num_bytes * 8) > 7500:
			raise RuntimeError ("generate cannot generate more than 7500 bits in a single call.")

		if requested_security_strength > self.security_strength:
			raise RuntimeError ("requested_security_strength exceeds this instance's security_strength (%d)" % self.security_strength)

		if self.reseed_counter >= 10000:
			return None

		temp = b""

		while len (temp) < num_bytes:
			self.V = self._hmac (self.K, self.V)
			temp += self.V

		self._update (None)
		self.reseed_counter += 1

		return temp[:num_bytes]
	
drbg = HMAC_DRBG (entropy=os.urandom (64))


secret = drbg.generate (10)
print(secret)

