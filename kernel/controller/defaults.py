from enum import IntEnum


class StatusCode(IntEnum):
    UNAUTHORIZATION = 401
    BAD_REQUEST_ARGUMENTS = 422


STATUS_TEXT = {
    StatusCode.UNAUTHORIZATION.value: 'unauthorization',
    StatusCode.BAD_REQUEST_ARGUMENTS.value: 'bad request arguments',
}
