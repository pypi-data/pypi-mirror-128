from .types import Action
from typing import Dict, List, Union
from .asserts import assert_comparable_type


# TODO
# Move type validation of actions to the top level to exit early
def apply_action_to_item(
	action: Action,
	item: str,
	value: Union[int, float, str],
) -> Union[int, float, str]:
	if len(action.keys()) > 1:
		raise Exception(
			"Too many actions '{}' were specified".format(", ".join(action.keys()))
		)

	set = action.get("set")

	# Specyfing set will replace the current value with the one passed to set
	if set is not None:
		try:
			assert_comparable_type(set, item, value)
		except Exception as e:
			raise Exception(f"'set' action type differs from variable type: {str(e)}")

		return set
	else:
		raise Exception(
			"Unexpected '{}' action was specified".format(list(action.keys())[0])
		)


def apply_actions_to_variables(
	actions: List[Action],
	variables: Dict[str, Union[int, float, str]],
):
	"""
	This function mutates the variables object passed to it
	"""
	for item in actions:
		if variables.get(item) is None:
			raise Exception(
				f"The key '{item}' is not defined in the variables object"
			)

		variables[item] = apply_action_to_item(actions[item], item, variables[item])
