import strawberry

# Token
from models.tokens import Token


@strawberry.experimental.pydantic.type(model=Token, all_fields=True)
class TokenType:
    pass
