import json


class Node:
    def __init__(self, label, label_type="name"):
        self.label = label
        self.label_type = label_type
        self.children = []

    def add_child(self, child, child_type="name"):
        if child == None:
            pass
        if child.__class__ == Node:
            self._add_child_node(child)
        elif type(child) == str:
            self._add_child_raw(child, child_type)
        else:
            raise ValueError(
                "Must supply an existing Node() object, or a label and "
                "label_type in order to create a new one"
            )

    def _add_child_raw(self, label, label_type):
        self.children.append(Node(label, label_type))

    def _add_child_node(self, node):
        self.children.append(node)

    def json(self):
        return json.dumps(self, default=lambda o: getattr(o, "__dict__", str(o)))
