import uuid

def generate_unique_random_key():
    unique_value = uuid.uuid4().hex
    return unique_value