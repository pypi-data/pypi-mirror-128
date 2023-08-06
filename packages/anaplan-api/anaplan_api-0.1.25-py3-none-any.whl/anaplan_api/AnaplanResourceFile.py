# ===============================================================================
# Created:        12 Sep 2018
# @author:        Jesse Wilson (Anaplan Asia Pte Ltd)
# Description:    This library takes a JSON response and builds a key-value dictionary for easy traversal.
# Input:          A JSON dictionary object
# Output:         Key-value dictionary object, resource name, or resource ID
# ===============================================================================
import json
from .AnaplanResource import AnaplanResource
from .util.Util import ResourceNotFoundError


class AnaplanResourceFile(AnaplanResource):
	_resources: dict

	def __init__(self, response: dict):
		self._resources = {item['id']: item['chunkCount'] for item in response}

	def __str__(self):
		return json.dumps(self._resources)

	def __getitem__(self, resource_name: str) -> int:
		"""
		:param resource_name: Resource name provided by user to be looked up
		"""
		try:
			return self._resources[resource_name]
		except ResourceNotFoundError:
			raise ResourceNotFoundError(f"{resource_name} not found in dictionary")

	def __len__(self) -> int:
		return len(self._resources)

	def __contains__(self, resource_name: str) -> bool:
		if resource_name in self._resources:
			return True
		else:
			return False
