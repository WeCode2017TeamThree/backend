"""
Location objects
"""
from bson import json_util
import json
from datetime import datetime

from pytz import utc

from mongoengine import Document, fields, EmbeddedDocument

# from glyphs.const import features


class Rating(EmbeddedDocument):
    upvotes = fields.IntField(default=0)
    downvotes = fields.IntField(default=0)


class FeatureSet(EmbeddedDocument):
    """
    """
    bathroom = fields.EmbeddedDocumentField(Rating)
    wifi = fields.EmbeddedDocumentField(Rating)
    shower = fields.EmbeddedDocumentField(Rating)
    charge_phone = fields.EmbeddedDocumentField(Rating)
    camp = fields.EmbeddedDocumentField(Rating)

    def toJSType(self):
        ret = {}
        for f in self._fields:
            feature = getattr(self, f, None)
            if feature:
                ret[f] = {'upvotes': feature.upvotes, 'downvotes': feature.downvotes}
        return ret


class Comment(EmbeddedDocument):
    """
    """
    name = fields.StringField()
    comment = fields.StringField()
    timestamp = fields.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc))
    helpfulRating = fields.IntField(default=0)
    reported = fields.IntField(default=0)

    def toJSType(self):
        return dict(
            name=self.name,
            comment=self.comment,
            timestamp=json.dumps(self.timestamp, default=json_util.default),
            helpfulRating=self.helpfulRating,
            reported=self.reported
        )


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
    feature_set = fields.EmbeddedDocumentField(FeatureSet, default=FeatureSet())
    comments = fields.EmbeddedDocumentListField(Comment)

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
            id=str(self.id),
            comments=[c.toJSType() for c in self.comments],
            feature_set=self.feature_set.toJSType()
        )
