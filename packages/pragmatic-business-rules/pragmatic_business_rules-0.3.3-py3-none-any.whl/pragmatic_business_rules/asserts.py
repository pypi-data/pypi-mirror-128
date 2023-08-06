from .types import Conditional
from typing import Any


def assert_single_conditional(conditional: Conditional):
	all = conditional.get("all")
	any = conditional.get("any")

	if all is not None and any is not None:
		raise Exception(
			"'all' and 'any' properties can't be specified for the same conditional"
		)
	elif all is None and any is None:
		raise Exception(
			"'all' or 'any' properties were not found in the conditional"
		)


def assert_comparable_type(value: Any, variable_name: str, variable_value: Any):
	# None is comparable to string and None
	if (value is None and variable_value is None) or (
		type(value) == str and variable_value is None
	) or (value is None and type(variable_value) == str):
		return

	# Ints and floats are comparable
	if type(value) in [int, float] and type(variable_value) in [int, float]:
		return

	if type(value) != type(variable_value):
		raise Exception(
			"The value '{}' to compare for variable '{}' doesn't match the defined type of '{}'"
			.format(
				value,
				variable_name,
				type(variable_value).__name__,
			)
		)
