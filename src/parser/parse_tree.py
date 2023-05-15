class ParseTree:
    def __init__(self, token_type, text=None, children=None):
        self.token_type = token_type
        self.text = text
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)

    def print_tree(self, level=0):
        result = "\t" * level + f"{self.token_type}"
        if self.text:
            result += f": {self.text}"
        result += "\n"
        for child in self.children:
            result += child.print_tree(level + 1)
        return result