from enum import Enum


class ClaimGamertagResult(Enum):
    NotAvailable = 409
    Available = 200


class ChangeGamertagResult(Enum):
    ChangeSuccessful = 200
    NoFreeChangesAvailable = 1020
