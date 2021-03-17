"""
    HTTP argument validation
"""
from marshmallow import Schema, fields, ValidationError


class UserSchema(Schema):
    q_value = fields.String(required=True)
