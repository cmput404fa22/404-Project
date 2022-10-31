from uuid import UUID, uuid4


class UUIDConverter:
    regex = "[0-9a-f]{8}[0-9a-f]{4}[0-9a-f]{4}[0-9a-f]{4}[0-9a-f]{12}"

    def to_python(self, value):
        return UUID(value, version=4)

    def to_url(self, value: uuid4):
        return value.hex
