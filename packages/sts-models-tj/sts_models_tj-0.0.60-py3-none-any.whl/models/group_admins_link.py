from . import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Table

# Availability class is used, so we must define it here or else it has to be definied by clients of the Group class,
# and they don't necessarily know that they need to do this
from .group import Group
from .user import User


group_admins_link = Table('association', Base.metadata,
    Column('groupId', ForeignKey('group.id')),
    Column('userId', ForeignKey('users.cognitoId'))
)
