from sqlfluff.core import Linter
from sqlfluff.core.config import FluffConfig

CONFIG: FluffConfig = FluffConfig(
    {
        "core": {
            "dialect": "ansi",
            "exclude_rules": "L031",
        },
        "rules": {
            "tab_space_size": 2,
            "L010": {
                "capitalisation_policy": "upper",
            },
            "L014": {
                "extended_capitalisation_policy": "lower",
            },
            "L026": {
                "force_enable": True,
            },
            "L028": {
                "force_enable": True,
            },
            "L029": {
                "unquoted_identifiers_policy": "all",
            },
            "L030": {
                "capitalisation_policy": "upper",
            },
            "L042": {"forbid_subquery_in": "both"},
        },
    }
)


def fix(sql: str) -> str:
    """Fix a sql string or file.

    Args:
        sql: The sql to be linted.

    Returns:
        The fixed sql if possible.
    """
    linter = Linter(config=CONFIG)

    result = linter.lint_string_wrapped(sql, fix=True)
    fixed_string = result.paths[0].files[0].fix_string()[0]
    return fixed_string
