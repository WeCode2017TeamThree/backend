"""
Location objects
"""
from mongoengine import Document, fields

# from glyphs.const import features


class Location(Document):
    """
    A location object
    """
    name = fields.StringField()
    description = fields.StringField()
    lat = fields.StringField()
    lng = fields.StringField()
    submitted_by = fields.StringField()
    certified = fields.BooleanField()

    def __repr__(self): # pragma: no cover
        return "Location(name=%r)" % self.name

    def toJSType(self):
        """
        => dict of Location
        """
        return dict(
            name=self.name,
            description=self.description,
            lat=self.lat,
            lng=self.lng,
            submitted_by=self.submitted_by,
            certified=self.certified,
            id=str(self.id)
        )
