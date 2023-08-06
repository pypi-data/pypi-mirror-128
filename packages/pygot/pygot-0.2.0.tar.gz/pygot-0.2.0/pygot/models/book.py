from marshmallow import Schema, fields, post_load


class Book:
    def __init__(
        self,
        url,
        name,
        isbn,
        authors,
        numberOfPages,
        publisher,
        country,
        mediaType,
        released,
        characters,
        povCharacters,
    ) -> None:
        self.url = url
        self.name = name
        self.isbn = isbn
        self.authors = authors
        self.numberOfPages = numberOfPages
        self.publisher = publisher
        self.country = country
        self.mediaType = mediaType
        self.released = released
        self.characters = characters
        self.povCharacters = povCharacters

    def __repr__(self):
        return "<Book(name={self.name!r})>".format(self=self)


class BookSchema(Schema):
    url = fields.Str()
    name = fields.Str()
    isbn = fields.Str()
    authors = fields.List(fields.Str())
    numberOfPages = fields.Int()
    publisher = fields.Str()
    country = fields.Str()
    mediaType = fields.Str()
    released = fields.Date("%Y-%m-%dT%H:%M:%S")
    characters = fields.List(fields.Str())
    povCharacters = fields.List(fields.Str())

    @post_load
    def make_book(self, data, **kwargs):
        return Book(**data)
