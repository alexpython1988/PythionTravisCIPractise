import os
import os.path
import facebook

class Real:
	def rm(self, file):
		os.remove(file)

	def rm1(self, file):
		if os.path.isfile(file):
			os.remove(file)

class Upload:
	def __init__(self, real):
		self.real = real

	def pre_upload(self, file):
		self.file = file

	def upload(self):
		print("uploading " + self.file)

	def post_upload(self):
		self.real.rm1(self.file)

class SimpleFacebook:
	def __init__(self, oauth_token):
		if oauth_token is not None:
			self.graph = facebook.GraphAPI(oauth_token)

	def post_msg(self, msg):
		self.graph.put_object("me", "feed", message = msg)