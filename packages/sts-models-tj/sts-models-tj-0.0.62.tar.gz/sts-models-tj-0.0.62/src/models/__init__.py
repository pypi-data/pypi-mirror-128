from sqlalchemy.ext.declarative import declarative_base


from .user import User
from .availability import Availability
from .availability_request import AvailabilityRequest
from .availability_series import AvailabilitySeries
from .group_members_link import GroupMembersLink
from .group_admins_link import GroupAdminsLink

Base = declarative_base(class_registry={'users': User, 'availability': Availability, 'availability_request': AvailabilityRequest, 'availability_series': AvailabilitySeries, 'group': Group, 'group_members_link': GroupMembersLink, 'group_admins_link': GroupAdminsLink})
