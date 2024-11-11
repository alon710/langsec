from typing import Optional
from sqlglot import exp
from ..schema.security_schema import SecuritySchema
from abc import ABC, abstractmethod


class BaseQueryValidator(ABC):
    def __init__(self, schema: Optional[SecuritySchema] = None):
        self.schema = schema or SecuritySchema()

    @abstractmethod
    def validate(self, parsed: exp.Expression) -> None:
        """Validates the given SQL query."""

    def _get_default_table(
        self, parsed: exp.Expression, column: exp.Column
    ) -> Optional[str]:
        """Gets the default table when column table is not specified."""
        parent = column.parent

        if parsed.parent_select is None:
            while parent:
                if isinstance(parent, exp.From):
                    if isinstance(parent.this, exp.Table):
                        return str(parent.this.name).lower()
                    break
                parent = parent.parent

            tables = list(parsed.find_all(exp.Table))
            if len(tables) == 1:
                return str(tables[0].name).lower()
            return None
        
        parent_select = parsed.parent_select
        
        from_exp: exp.From = parent_select.args['from']
        table: exp.Table = from_exp.this
        return table.name.lower()
        
       
