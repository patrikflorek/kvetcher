
def generate_id():
    id = 1
    while True:
        yield id
        id += 1

id_gen = generate_id()

def get_new_id():
    return next(id_gen)
    