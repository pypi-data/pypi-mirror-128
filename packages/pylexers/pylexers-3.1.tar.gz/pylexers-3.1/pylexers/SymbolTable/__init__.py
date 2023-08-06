import dataclasses
from typing import Optional, Any


@dataclasses.dataclass
class SymbolTable:
    parent: Optional["SymbolTable"] = None
    identifiers: dict[str, Any] = dataclasses.field(default_factory=dict)
    user_higher_scope: bool = True

    def create_sub_scope(self):
        return SymbolTable(parent=self)

    def get_identifier(self, identifier):
        if self.does_identifier_exist(identifier):
            return self.identifiers[identifier][0]
        if self.parent and self.user_higher_scope:
            return self.parent.get_identifier(identifier)
        raise RuntimeError(f"Unknown identifier {identifier}")

    def get_identifier_type(self, identifier):
        if self.does_identifier_exist(identifier):
            return self.identifiers[identifier][1]
        if self.parent and self.user_higher_scope:
            return self.parent.get_identifier(identifier)
        raise SyntaxError(f"Unknown identifier {identifier}")

    def add_identifier(self, identifier: str, obj: Any, type: str):
        if self.does_identifier_exist(identifier):
            raise SyntaxError(f"Identifier already exists {identifier}")
        self.identifiers[identifier] = (obj, type)

    def reset_identifier(self, identifier: str, obj: Any, type: str):
        self.identifiers[identifier] = (obj, type)

    def remove_identifier(self, identifier: str):
        self.identifiers.pop(identifier)

    def does_identifier_exist(self, identifier: str):
        if identifier in self.identifiers:
            return True
        if self.parent and self.user_higher_scope:
            return self.parent.does_identifier_exist(identifier)
        return False
