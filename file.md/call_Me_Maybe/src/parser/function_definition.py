class FunctionDefn:
    def __init__(self, name: str, description: str, parameters: dict):
        self.name = name
        self.description = description
        self.parameters = parameters

    def __repr__(self):
        return f"FunctionDefn(name={self.name}, description={self.description}, parameters={self.parameters})"