import datetime
from typing import Any, Optional, Mapping, Dict

from marshmallow import Schema, fields, post_load, EXCLUDE, ValidationError

from .model import Identity, Contact


class DateTimeObjField(fields.Field):

    def _serialize(self, value: Any, attr: str, obj: Any, **kwargs):
        if value is None:
            return None

        return value

    def _deserialize(self, value: Any, attr: Optional[str], data: Optional[Mapping[str, Any]], **kwargs):
        if not isinstance(value, datetime.datetime):
            raise ValidationError("Date time object must be an instance of datetime.datetime")

        return value


class ContactSchema(Schema):
    city = fields.Str(missing=None)
    country = fields.Str(missing=None)
    country_code = fields.Str(data_key="countryCode", missing=None)
    district = fields.Str(missing=None)
    email = fields.Str(missing=None)
    external_date = DateTimeObjField(data_key="externalDate", missing=None)
    municipality_key = fields.Str(data_key="municipalityKey", missing=None)
    phone = fields.Str(missing=None)
    state = fields.Str(missing=None)
    street = fields.Str(missing=None)
    zip_code = fields.Str(data_key="zipCode", missing=None)

    @post_load
    def make_contact(self, data, **kwargs):
        return Contact(**data)

    class Meta:
        unknown = EXCLUDE


class IdentitySchema(Schema):
    first_name = fields.Str(data_key="firstName", missing=None)
    last_name = fields.Str(data_key="lastName", missing=None)
    gender = fields.Str(missing=None)
    birth_date = DateTimeObjField(data_key="birthDate", missing=None)
    birth_place = fields.Str(data_key="birthPlace", missing=None)
    civil_status = fields.Str(data_key="civilStatus", missing=None)
    degree = fields.Str(missing=None)
    external_date = DateTimeObjField(data_key="externalDate", missing=None)
    middle_name = fields.Str(data_key="middleName", missing=None)
    mother_tongue = fields.Str(data_key="motherTongue", missing=None)
    mothers_maiden_name = fields.Str(data_key="mothersMaidenName", missing=None)
    nationality = fields.Str(missing=None)
    prefix = fields.Str(missing=None)
    race = fields.Str(missing=None)
    religion = fields.Str(missing=None)
    suffix = fields.Str(missing=None)
    value1 = fields.Str(missing=None)
    value2 = fields.Str(missing=None)
    value3 = fields.Str(missing=None)
    value4 = fields.Str(missing=None)
    value5 = fields.Str(missing=None)
    value6 = fields.Str(missing=None)
    value7 = fields.Str(missing=None)
    value8 = fields.Str(missing=None)
    value9 = fields.Str(missing=None)
    value10 = fields.Str(missing=None)
    contacts = fields.List(fields.Nested(ContactSchema), missing=[])

    @post_load
    def make_identity(self, data, **kwargs):
        return Identity(**data)

    class Meta:
        unknown = EXCLUDE


def load_identity(data: Dict[str, Any]) -> Identity:
    return IdentitySchema().load(data)


def dump_identity(identity: Identity) -> Dict[str, Any]:
    return IdentitySchema().dump(identity)


def load_contact(data: Dict[str, Any]) -> Identity:
    return ContactSchema().load(data)


def dump_contact(contact: Contact) -> Dict[str, Any]:
    return ContactSchema().dump(contact)
