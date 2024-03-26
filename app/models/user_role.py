from enum import IntEnum


class UserRole(IntEnum):
    VISITOR = 0
    CLIENT = 1
    STAKEHOLDER = 2
    ASSOCIATE = 3
    MANAGER = 4
    ADMIN = 5
