class ConfigurationClass:
    def __init__(self, function_instance, trigger_in_instance, trigger_out_instance, role_instance) -> None:
        self.function_instance = function_instance
        self.trigger_in_instance = trigger_in_instance
        self.trigger_out_instance = trigger_out_instance
        self.role_instance = role_instance