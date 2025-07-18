from search_query.constants_example import generic_search_field_set_to_syntax_set
from search_query.constants_example import map_search_field
from search_query.query import Query
from search_query.translator_base import QueryTranslator


class CustomTranslator(QueryTranslator):
    """Translator for Custom queries."""

    @classmethod
    def to_generic_syntax(cls, query: Query, *, search_field_general: str) -> Query:
        query = query.copy()
        cls.translate_search_fields_to_generic(query)
        return query

    @classmethod
    def to_specific_syntax(cls, query: Query) -> Query:
        query = query.copy()
        cls._translate_search_fields(query)
        return query

    @classmethod
    def translate_search_fields_to_generic(cls, query: Query) -> None:
        if query.search_field:
            fields = map_search_field(query.search_field.value)
            if len(fields) == 1:
                query.search_field.value = fields.pop()
            else:
                raise NotImplementedError
        for child in query.children:
            cls.translate_search_fields_to_generic(child)

    @classmethod
    def _translate_search_fields(cls, query: Query) -> None:
        if query.search_field:
            specific = generic_search_field_to_syntax_field(query.search_field.value)
            query.search_field.value = specific

        for child in query.children:
            cls._translate_search_fields(child)
