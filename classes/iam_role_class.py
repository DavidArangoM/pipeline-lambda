class IamRoleClass:
    def __init__(self, name, assumeRolePolicyName, customPolicyName) -> None:
        self.name = name
        self.assumeRolePolicyName = assumeRolePolicyName
        self.customPolicyName = customPolicyName
        
        