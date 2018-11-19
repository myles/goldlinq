class HObject:
    """HObject base class."""

    @classmethod
    def parse(cls, data):
        model = cls()

        for key, value in data.items():
            setattr(model, key, value)

        return model

    def to_h_object(self):
        h_object = {
            'type': self.h_type,
            'properties': {}
        }

        for key, value in self.__dict__.items():
            if isinstance(value, (HAdr, HCard, HEvent, HGeo)):
                h_object['properties'][key] = [value.to_h_object(), ]
            else:
                h_object['properties'][key] = [value, ]

        return h_object


class HGeo(HObject):

    h_type = 'h-geo'

    def __repr__(self):
        return f"HGeo({self.latitude}, {self.longitude})"


class HAdr(HObject):

    h_type = 'h-adr'

    def __repr__(self):
        return f"HAdr({self.name})"


class HCard(HObject):

    h_type = 'h-card'

    def __repr__(self):
        return f"HCard({self.name})"


class HEvent(HObject):

    h_type = 'h-event'

    def __repr__(self):
        return f"HEvent({self.name})"
