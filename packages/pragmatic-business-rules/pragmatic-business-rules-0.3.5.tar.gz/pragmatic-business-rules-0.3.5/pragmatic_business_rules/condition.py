from typing import Dict, List, Literal, Optional, Union

from .asserts import assert_comparable_type, assert_single_conditional
from .types import Condition, Conditional


# By this point, the incoming conditions and variables have to have been already validated
# for correct value types
def evaluate_condition(
	condition: Condition,
	variables: Dict[str, Union[int, float, str]],
) -> bool:
	condition_name = condition.get("name")
	condition_operator = condition.get("operator")
	condition_value = condition.get("value")

	# Validate variable exists and matches type
	if condition_name not in variables:
		raise Exception(f"Variable '{condition_name}' not defined")

	variable: Union[str, int, float] = variables.get(condition_name)

	assert_comparable_type(
		condition_value,
		condition_name,
		variables.get(condition_name),
	)

	# The only value comparable to None is string, so they can be grouped in the same category
	if type(condition_value) == str or condition_value is None:
		if condition_operator == "equal_to":
			return condition_value == variable
		else:
			raise Exception(
				f"The operator '{condition_operator}' is not valid for string operations"
			)
	elif type(condition_value) == int or type(condition_value) == float:
		if condition_operator == "equal_to":
			return variable == condition_value
		elif condition_operator == "greater_than_or_equal_to":
			return variable >= condition_value
		elif condition_operator == "greater_than":
			return variable > condition_value
		elif condition_operator == "less_than_or_equal_to":
			return variable <= condition_value
		elif condition_operator == "less_than":
			return variable < condition_value
		else:
			raise Exception(
				f"The operator '{condition_operator}' is not valid for number operations"
			)
	else:
		raise Exception(
			"The value '{}' has a type '{}' which is not valid for a condition value"
			.format(
				condition_value,
				type(condition_value).__name__,
			)
		)


def evaluate_conditional(
	conditional: Optional[List[Union[Conditional, Condition]]],
	variables: Dict[str, Union[str, int]],
	type: Literal["all", "any"],
) -> bool:
	"""
	This function will evaluate the conditionals and return the boolean result for the entire group

	The evaluation process is different depending on the type:
	- all: All conditionals must be true
	- any: At least one conditional must be true
	"""
	if type not in ["all", "any"]:
		raise Exception(
			f"The evaluation type '{type}' is not a valid conditional type"
		)

	if conditional is None:
		return False

	# Make sure that the conditional contains items that can be evaluated
	# If no items were evaluated, mark the conditional as false
	evaluated_items = 0
	# If the type is "all", the goal is to change the result to false, if it's "any"
	# we try to set it to true
	result = True if type == "all" else False
	for c in conditional:
		condition_result = None

		# If it contains a value, it's a simple condition
		if "value" in c:
			condition_result = evaluate_condition(c, variables)
		else:
			assert_single_conditional(c)

			all = c.get("all")
			any = c.get("any")

			subconditional = all if all is not None else any
			subtype = "all" if all is not None else "any"

			condition_result = evaluate_conditional(
				subconditional,
				variables,
				subtype,
			)

		# Should never happend
		if condition_result is None:
			raise Exception("The evaluation of a condition failed")

		evaluated_items += 1

		# If one of the conditions returned false and the type is set to "all", stop evaluating and return
		# There is no need to change the value otherwise
		if type == "all" and condition_result == False:
			result = condition_result
			break
		# If one of the conditions returned true and the type is set to "any", stop evaluating and return
		elif type == "any" and condition_result == True:
			result = condition_result
			break

	return result if evaluated_items > 0 else False
