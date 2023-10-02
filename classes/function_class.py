from classes.trigger_in_class import TriggerInClass
class FunctionClass:
    def __init__(self, accountId, region, name, description, role, timeout, memory_size, storage_size, vpc, runtime, layers, variables, code) -> None:
        self.accountId = accountId
        self.region = region
        self.name = name
        self.description = description
        self.role = role
        self.timeout = timeout
        self.memory_size = memory_size        
        self.storage_size = storage_size
        self.vpc = vpc
        self.runtime = runtime
        self.layers = layers
        self.variables = variables
        self.code = code
