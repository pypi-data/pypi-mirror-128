import requests

class XenForoAPI:
	def __init__(self, key, domain):
		self.api_key = key
		self.headers = {
			"XF-Api-Key": self.api_key
		}
		self.domain = domain

	def GetMe(self):
		"""
		Gets information about the current API user
		"""
		res = requests.get(f'https://{self.domain}/api/me/', headers=self.headers)
		return res.json()

	def GetForumByID(self, forum_id):
		"""
		Gets information about the specified forum
		"""
		res = requests.get(f'https://{self.domain}/api/forums/{forum_id}/', headers=self.headers)
		return res.json()

	def GetNodes(self):
		"""
		Gets the node tree.
		"""
		res = requests.get(f'https://{self.domain}/api/nodes/', headers=self.headers)
		return res.json()


	def GetPostByID(self, post_id):
		"""
		Gets information about the specified post
		"""
		res = requests.get(f'https://{self.domain}/api/posts/{post_id}/', headers=self.headers)
		return res.json()
		
	def DeletePost(self, post_id, reason):	
		"""
		Deletes the specified post. Default to soft deletion.
		"""
		res = requests.delete(
			f'https://{self.domain}/api/posts/{post_id}/', 
			headers = self.headers,
			data = {
				'reason': reason
			}
		)
		return res.json()
