from neomodel import (
    DateProperty,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


class Exhibition(StructuredNode):
    uid = UniqueIdProperty()
    format = StringProperty()
    title = StringProperty(required=True)
    description = StringProperty()
    start_date = DateProperty()
    end_date = DateProperty()
    image_url = StringProperty()
    image_alt = StringProperty()
    location = StringProperty()


class Event(StructuredNode):
    uid = UniqueIdProperty()
    format = StringProperty()
    title = StringProperty(required=True)
    description = StringProperty()
    start_date = DateProperty()
    end_date = DateProperty()
    image_url = StringProperty()
    image_alt = StringProperty()
    location = StringProperty()
