from literals.mappings import ALL_LITERALS, BaseLiterals


def get_literals_by_id(key: str):
    for literals in ALL_LITERALS:
        record: BaseLiterals = literals.objects.filter(
            id=key).first()

        if record:
            return record
    return None
