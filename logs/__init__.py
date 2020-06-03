import logging

import sqlparse


class CustomFormatter(logging.Formatter):
    def format(self, record):
        sql = record.getMessage()
        formatted_sql = sqlparse.format(sql, reindent=True, keyword_case='upper')

        try:
            import pygments
            from pygments.lexers import SqlLexer
            from pygments.formatters import TerminalTrueColorFormatter

            formatted_sql = pygments.highlight(
                formatted_sql,
                SqlLexer(),
                TerminalTrueColorFormatter(style='monokai')
            )
        except ImportError:
            pass

        return formatted_sql
