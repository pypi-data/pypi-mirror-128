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
		
	def DeletePost(self, post_id, reason, hard_delete = 0, author_alert = 0, author_alert_reason = ""):	
		"""
		Deletes the specified post. Default to soft deletion.
		"""
		res = requests.delete(
			f'https://{self.domain}/api/posts/{post_id}/', 
			headers = self.headers,
			data = {
				'reason': reason,
				'hard_delete': hard_delete,
				'author_alert': author_alert,
				'author_alert_reason': author_alert_reason
			}
		)
		return res.json()

	def AddPost(self, thread_id, message, attachment_key = ""):
		res = requests.post(
			f'https://{self.domain}/api/posts/',
			headers = self.headers,
			data = {
				"thread_id": thread_id,
				"message": message,
				"attachment_key": attachment_key
			}
		)
		return res.json()

	def ReactPost(self, post_id, reaction_id):
		res = requests.post(
			f'https://{self.domain}/api/posts/{post_id}/react',
			headers = self.headers,
			data = {
				"reaction_id": reaction_id
			}
		)
		return res.json()

	def DeleteNode(self, node_id, delete_children = 0):
		pass