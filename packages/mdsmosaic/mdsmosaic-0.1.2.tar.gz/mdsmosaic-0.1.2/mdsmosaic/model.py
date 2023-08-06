from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Contact:
    city: Optional[str] = None
    """City of residence (e.g. Berlin)"""
    country: Optional[str] = None
    """Country of residence (e.g. Germany)"""
    country_code: Optional[str] = None
    """Country code (e.g. DE)"""
    district: Optional[str] = None
    """District (e.g. Spandau)"""
    email: Optional[str] = None
    """Email address (e.g. anna.schmidt@beispiel.de)"""
    external_date: Optional[datetime] = field(default=None)
    """Custom external date (e.g. 2019-06-27)"""
    municipality_key: Optional[str] = None
    """Municipality key (e.g. 11000000)"""
    phone: Optional[str] = None
    """Phone number (e.g. 030/123456789)"""
    state: Optional[str] = None
    """State (e.g. Berlin)"""
    street: Optional[str] = None
    """Street (e.g. Spandauer Damm)"""
    zip_code: Optional[str] = None
    """Zip Code (e.g. 13593)"""

@dataclass
class Identity:
    birth_date: datetime = field(default=None)
    """Birth date (e.g. 2019-04-30)"""
    birth_place: Optional[str] = None
    """Birth place (e.g. Berlin)"""
    civil_status: Optional[str] = None
    """Civil status (e.g. Single)"""
    degree: Optional[str] = None
    """Degree (e.g. Higher Education)"""
    external_date: Optional[datetime] = field(default=None)
    """Custom external date (e.g. 2019-06-27)"""
    first_name: Optional[str] = None
    """First name (e.g. Anna)"""
    gender: Optional[str] = None
    """Gender (M = male, F = female, O = other, U = unknown, X = divers)"""
    last_name: Optional[str] = None
    """Last name (e.g. Lea)"""
    middle_name: Optional[str] = None
    """Middle name(s) (e.g. Schmidt)"""
    mother_tongue: Optional[str] = None
    """Mother tongue (e.g. German)"""
    mothers_maiden_name: Optional[str] = None
    """Mothers' maiden name (e.g. Müller)"""
    nationality: Optional[str] = None
    """Nationality (e.g. German)"""
    prefix: Optional[str] = None
    """Prefix (e.g. of)"""
    race: Optional[str] = None
    """Race (e.g. Caucasian)"""
    religion: Optional[str] = None
    """Religion (e.g. Christianity)"""
    suffix: Optional[str] = None
    """Suffix (e.g. B.Sc.)"""
    # custom fields
    value1: Optional[str] = None
    """Custom field (up to 50 chars)"""
    value2: Optional[str] = None
    """Custom field (up to 50 chars)"""
    value3: Optional[str] = None
    """Custom field (up to 50 chars)"""
    value4: Optional[str] = None
    """Custom field (up to 50 chars)"""
    value5: Optional[str] = None
    """Custom field (up to 50 chars)"""
    value6: Optional[str] = None
    """Custom field (up to 255 chars)"""
    value7: Optional[str] = None
    """Custom field (up to 255 chars)"""
    value8: Optional[str] = None
    """Custom field (up to 1.000 chars)"""
    value9: Optional[str] = None
    """Custom field (up to 1.000 chars)"""
    value10: Optional[str] = None
    """Custom field (up to 10.000 chars)"""
    contacts: List[Contact] = field(default_factory=list)
    """List of contact information"""
