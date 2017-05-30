from cerberus import Validator
from cerberus.errors import ValidationError
from app.errors import InvalidParameterError


FIELDS = {
    'cart_id': {
        'type': 'string',
        'required': False
    },
    'external_id': {
        'type': 'string',
        'required': True
    },
    'name': {
        'type': 'string',
        'required': False
    },
    'value': {
        'type': 'integer',
        'required': False
    }
}


def validate_item_request(req, res, resource, params):
    schema = {
        'cart_id': FIELDS['cart_id'],
        'external_id': FIELDS['external_id'],
        'name': FIELDS['name'],
        'value': FIELDS['value']
    }

    v = Validator(schema)

    try:
        if not v.validate(req.context['data']):
            raise InvalidParameterError(v.errors)
    except ValidationError:
        raise InvalidParameterError(req.context)