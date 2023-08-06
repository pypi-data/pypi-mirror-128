class BaseStep:
    """Base Class of a Pypeline Step, this should not be used alone"""

    def __init__(self, **kwargs) -> None:
        pass

    def execute(self):
        """assert inheriting class has this"""
        raise NotImplementedError("This function needs to be implemented by child step")
