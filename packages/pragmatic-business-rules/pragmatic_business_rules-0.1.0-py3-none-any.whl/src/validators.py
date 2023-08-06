import jsonschema
from jsonschema.exceptions import ValidationError


class CustomValidationError(Exception):

	def __init__(self, message: str):
		self.message = message
		super().__init__(self.message)


def validate_schema_with_custom_errors(data: dict, schema: dict):
	try:
		jsonschema.validate(data, schema)
	except ValidationError as e:
		error_message = e.schema.get("error_message")
		if error_message is not None:
			raise CustomValidationError(f"{error_message}: {e.message}")
		else:
			raise e


# This object will match any object with no nested properties and all items being
# either strings or numbers
plain_dictionary_schema = {
	"additionalProperties": False,
	"patternProperties": {
		".+": {
			"type": [
				"number",
				"string",
			]
		},
	},
	"type": "object",
}

rule_schema = {
	"$defs": {
		"condition": {
			"properties": {
				"name": {
					"type": "string",
				},
				"operator": {
					"enum": [
						"equal_to",
						"greater_than_or_equal_to",
						"greater_than",
						"less_than_or_equal_to",
						"less_than",
					],
					"error_message": "The provided operator for the condition is invalid",
					"type": "string",
				},
				"value": {
					"type": [
						"number",
						"string",
					],
				},
			},
			"required": [
				"name",
				"operator",
				"value",
			],
			"type": "object",
		},
		"conditional": {
			"additionalProperties": False,
			"properties": {
				"all": {
					"items": {
						"oneOf": [
							{
								"$ref": "#/$defs/condition",
							},
							{
								"$ref": "#/$defs/conditional",
							},
						],
					},
					"type": "array",
				},
				"any": {
					"items": {
						"oneOf": [
							{
								"$ref": "#/$defs/condition",
							},
							{
								"$ref": "#/$defs/conditional",
							},
						],
					},
					"type": "array",
				},
			},
			"type": "object"
		},
	},
	"items": {
		"additionalProperties": False,
		"properties": {
			"actions": {
				"additionalProperties": False,
				"patternProperties": {
					".+": {
						"additionalProperties": False,
						"patternProperties": {
							".+": {
								"error_message": "The provided type for the action is invalid",
								"type": [
									"number",
									"string",
								],
							},
						},
						"type": "object",
					},
				},
				"type": "object",
			},
			"conditions": {
				"$ref": "#/$defs/conditional",
			},
		},
		"required": [
			"actions",
			"conditions",
		],
		"type": "object",
	},
	"type": "array",
}
