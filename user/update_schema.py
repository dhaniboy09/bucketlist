update_schema = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string", "pattern": "^[^@]+@[^@]+\.[^@]+"}
    },
    "required": ["first_name", "last_name", "email"]
}
