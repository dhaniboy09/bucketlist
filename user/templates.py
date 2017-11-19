def user_obj(user):
    return {
        "id": user.external_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "links": [
            {"rel": "self", "href": "/users/" + user.external_id},
            {"rel": "bucketlist_items", "href": "/users/%s/bucketlist_items" % user.external_id}
        ]
    }


def profile_user_obj(user):
    return {
        "id": user.external_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "links": [
            {"rel": "self", "href": "/users/" + user.external_id}
        ]
    }


def users_obj(users):
    users_obj = []
    for user in users.items:
        users_obj.append(user_obj(user))
    return users_obj
