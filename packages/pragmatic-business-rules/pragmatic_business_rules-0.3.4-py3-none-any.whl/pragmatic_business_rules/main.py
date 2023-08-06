from .action import apply_actions_to_variables
from .asserts import assert_single_conditional
from .condition import evaluate_conditional
from .types import Rule
from .validators import CustomValidationError, variable_schema, rule_schema, validate_schema_with_custom_errors
from jsonschema.exceptions import ValidationError
from typing import Dict, List, Union
import jsonschema


def assert_valid_rules(rules: List[Rule]):
	"""
	This function runs a validation over the rules passed and raises a detailed message with any
	inconsistencies found
	"""
	validate_schema_with_custom_errors(rules, rule_schema)


def process_rules(
	rules: List[Rule],
	variables: Dict[str, Union[int, float, str]],
) -> Dict[str, Union[int, float, str]]:
	"""
	Process the rules and execute the result of the actions over the passed variables argument

	This function does not mutate the original variables object passed to it
	"""
	result = variables.copy()

	try:
		assert_valid_rules(rules)
	except CustomValidationError as validation_error:
		raise Exception(
			f"Invalid input for 'rules': {str(validation_error)}"
		) from validation_error
	except ValidationError as validation_error:
		raise Exception(
			f"Invalid input for 'rules': {str(validation_error)}"
		) from validation_error

	try:
		jsonschema.validate(variables, variable_schema)
	except ValidationError as validation_error:
		raise Exception(
			f"Invalid input for 'variables': {validation_error.message}"
		) from validation_error

	for rule in rules:
		actions = rule.get("actions")
		conditions = rule.get("conditions")

		# Make sure the condition has at least one usable condition
		assert_single_conditional(conditions)

		all = conditions.get("all")
		any = conditions.get("any")

		conditional = all if all is not None else any
		type = "all" if all is not None else "any"

		if evaluate_conditional(conditional, result, type):
			apply_actions_to_variables(actions, result)

	return result
