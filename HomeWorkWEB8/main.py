from typing import List, Any

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_tags(tags: str) -> list[str | None]:
    print(f"Find by {tags}")
    results = []
    tags = tags.split(",")
    for a in tags:
        quotes = Quote.objects(tags__iregex=a)
        result = [q.quote for q in quotes]
        results.append(result)
    return results


@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def search_quotes(command):
    parts = command.split(":", 1)
    if len(parts) != 2:
        return

    key, value = parts
    key = key.strip()
    value = value.strip()

    if key == "name":
        result = find_by_author(value)
    elif key == "tags":
        result = find_by_tags(value)
    elif key == "tag":
        result = find_by_tag(value)
    else:
        print("Invalid command format. Use 'name:', 'tag:', or 'tags:'.")
        return

    if result:
        print(f"RESULT:{result}")
    else:
        print("No value found for this query")


if __name__ == "__main__":
    while True:
        command = input(
            "Invalid command format. Use 'name:', 'tag:', or 'tags:\nEnter command 'exit' to quit:\n>>>"
        )
        if command.lower() == "exit":
            break
        search_quotes(command)
