class ServiceError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class EntityNotFoundError(ServiceError):
    def __init__(self, entity_name: str):
        self.entity_name = entity_name
        super().__init__(f"{entity_name} not found")


class EntityConflictError(ServiceError):
    def __init__(self, entity_name: str):
        self.entity_name = entity_name
        super().__init__(f"{entity_name} conflict")


class InvalidStateError(ServiceError):
    pass

