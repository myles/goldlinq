class HObject:
    """HObject base class."""

    @classmethod
    def parse(cls, data):
        model = cls()

        for key, value in data.items():
            setattr(model, key, value)

        return model


class HGeo(HObject):
    def __repr__(self):
        return f"HGeo({self.latitude}, {self.longitude})"


class HAdr(HObject):
    def __repr__(self):
        return f"HAdr({self.name})"


class HCard(HObject):
    def __repr__(self):
        return f"HCard({self.name})"


class HEvent(HObject):
    def __repr__(self):
        return f"HEvent({self.name})"
