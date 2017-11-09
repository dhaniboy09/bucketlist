def user_obj(user):
    return {
        "id": user.external_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
        "links": [
            {"rel": "self", "href": "/users/" + user.external_id}
        ]
    }


def users_obj(users):
    users = []
    return users
