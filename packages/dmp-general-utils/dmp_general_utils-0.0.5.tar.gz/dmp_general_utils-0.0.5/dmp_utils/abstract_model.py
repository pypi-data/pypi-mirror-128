from sqlalchemy import Column, Integer

from dmp_utils import get_timestamp_now


class BaseModal:
    created_at = Column(Integer, server_default=str(get_timestamp_now()))
    updated_at = Column(Integer, server_default=str(get_timestamp_now()))
