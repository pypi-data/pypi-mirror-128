from marshmallow import Schema, fields, post_load


class House:
    def __init__(
        self,
        url,
        name,
        region,
        coatOfArms,
        words,
        titles,
        seats,
        currentLord,
        heir,
        overlord,
        founded,
        founder,
        diedOut,
        ancestralWeapons,
        cadetBranches,
        swornMembers,
    ) -> None:
        self.url = url
        self.name = name
        self.region = region
        self.coatOfArms = coatOfArms
        self.words = words
        self.titles = titles
        self.seats = seats
        self.currentLord = currentLord
        self.heir = heir
        self.overlord = overlord
        self.founded = founded
        self.founder = founder
        self.diedOut = diedOut
        self.ancestralWeapons = ancestralWeapons
        self.cadetBranches = cadetBranches
        self.swornMembers = swornMembers

    def __repr__(self):
        return "<House(name={self.name!r})>".format(self=self)


class HouseSchema(Schema):
    url = fields.Str()
    name = fields.Str()
    region = fields.Str()
    coatOfArms = fields.Str()
    words = fields.Str()
    titles = fields.List(fields.Str())
    seats = fields.List(fields.Str())
    currentLord = fields.Str()
    heir = fields.Str()
    overlord = fields.Str()
    founded = fields.Str()
    founder = fields.Str()
    diedOut = fields.Str()
    ancestralWeapons = fields.List(fields.Str())
    cadetBranches = fields.List(fields.Str())
    swornMembers = fields.List(fields.Str())

    @post_load
    def make_house(self, data, **kwargs):
        return House(**data)
