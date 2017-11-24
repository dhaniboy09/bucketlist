from user.templates import profile_user_obj


def bucketlist_obj(bucketlist_item):
    return {
      "id":             bucketlist_item.external_id,
      "name":           bucketlist_item.name,
      "user":           profile_user_obj(bucketlist_item.user),
      "created_on":     bucketlist_item.created_on,
      "modified_on":    bucketlist_item.modified_on,
      "links": [
        {"rel": "self", "href": "/items/" + bucketlist_item.external_id}
      ]
    }


def bucketlist_objs(bucketlist_items):
    items = []
    for item in bucketlist_items.items:
        items.append(bucketlist_obj(item))
    return items
