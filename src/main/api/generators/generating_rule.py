class GeneratingRule:
    def __init__(self, regex: str):
        self.regex = regex

    def __repr__(self):
        return f"GeneratingRule(regex={self.regex})"
