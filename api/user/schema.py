schema = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string", "pattern": "^[^@]+@[^@]+\.[^@]+"},
        "password": {"type": "string", "pattern": "^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,}$"}
    },
    "required": ["first_name", "last_name", "email", "password"]
}
update_schema = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string", "pattern": "^[^@]+@[^@]+\.[^@]+"}
    },
    "required": ["first_name", "last_name", "email"]
}
password_schema = {
    "type": "object",
    "properties": {
        "password": {"type": "string", "pattern": "^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,}$"}
    },
    "required": ["password"]
}
