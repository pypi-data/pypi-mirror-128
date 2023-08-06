from marshmallow import Schema, fields, post_load


class Character:
    def __init__(
        self,
        url,
        name,
        gender,
        culture,
        born,
        died,
        titles,
        aliases,
        father,
        mother,
        spouse,
        allegiances,
        books,
        povBooks,
        tvSeries,
        playedBy,
    ) -> None:
        self.url = url
        self.name = name
        self.gender = gender
        self.culture = culture
        self.born = born
        self.died = died
        self.titles = titles
        self.aliases = aliases
        self.father = father
        self.mother = mother
        self.spouse = spouse
        self.allegiances = allegiances
        self.books = books
        self.povBooks = povBooks
        self.tvSeries = tvSeries
        self.playedBy = playedBy

    def __repr__(self):
        return "<Character(name={self.name!r})>".format(self=self)


class CharacterSchema(Schema):
    url = fields.Str()
    name = fields.Str()
    gender = fields.Str()
    culture = fields.Str()
    born = fields.Str()
    died = fields.Str()
    titles = fields.List(fields.Str())
    aliases = fields.List(fields.Str())
    father = fields.Str()
    mother = fields.Str()
    spouse = fields.Str()
    allegiances = fields.List(fields.Str())
    books = fields.List(fields.Str())
    povBooks = fields.List(fields.Str())
    tvSeries = fields.List(fields.Str())
    playedBy = fields.List(fields.Str())

    @post_load
    def make_character(self, data, **kwargs):
        return Character(**data)
