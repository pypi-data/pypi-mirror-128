from .TaskFactory import TaskFactory
from .AnaplanConnection import AnaplanConnection
from .Action import Action
from .Parser import Parser
from .ActionParser import ActionParser
from .util.Util import TaskParameterError


class ActionTask(TaskFactory):
	"""
	Factory to generate an Anaplan action task
	"""

	@staticmethod
	def get_action(conn: AnaplanConnection, action_id: str, retry_count: int, mapping_params: dict = None) -> Action:
		if not mapping_params:
			return Action(conn=conn, action_id=action_id, retry_count=retry_count, mapping_params=mapping_params)
		else:
			raise TaskParameterError("Only Anaplan imports accept mapping parameters.")

	@staticmethod
	def get_parser(conn: AnaplanConnection, results: dict, url: str) -> Parser:
		return ActionParser(results, url)
