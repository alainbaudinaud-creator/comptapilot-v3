
def paginate(rows, page=1, size=50):

    start = (page - 1) * size
    end = start + size

    return rows[start:end]


