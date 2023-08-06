from __future__ import annotations
from typing import Dict, List, Literal, Optional, TypedDict, Union


class Action(TypedDict):
	set: Optional[Union[int, float, str]]


class Condition(TypedDict):
	name: str
	operator: Literal["equal_to", "greater_than_or_equal_to", "greater_than",
										"less_than_or_equal_to", "less_than"]
	value: Union[int, float, str]


class Conditional(TypedDict):
	all: Optional[List[Union[Conditional, Condition]]]
	any: Optional[List[Union[Conditional, Condition]]]


class Rule(TypedDict):
	actions: Dict[str, Action]
	conditions: Conditional
