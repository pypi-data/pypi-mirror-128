class MystAPIError(Exception):
    pass

class TopUpError(Exception):
    pass

class InternalServerError(MystAPIError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class BadRequestError(MystAPIError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ParameterValidationError(MystAPIError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
class RegistrationAlreadyInProgressError(MystAPIError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ServiceUnavailableError(MystAPIError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MinimumAmountError(TopUpError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)