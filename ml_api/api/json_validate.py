from functools import wraps

from flask import current_app, jsonify, request
from jsonschema import ValidationError, validate
from werkzeug.exceptions import BadRequest


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        ctype = request.headers.get("Content-Type", "")
        method_ = request.headers.get("X-HTTP-Method-Override", request.method)

        if method_.lower() == request.method.lower() and "json" in ctype.lower():
            try:
                request.json
            except BadRequest:
                return jsonify({"error": "This is an invalid json"}), 400

        return f(*args, **kw)

    return wrapper


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.json, current_app.config[schema_name])
            except ValidationError as e:
                return jsonify({"error": e.message}), 400
            return f(*args, **kw)

        return wrapper

    return decorator
