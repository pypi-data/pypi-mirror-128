
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.admin_api import AdminApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from identity.api.admin_api import AdminApi
from identity.api.authentication_api import AuthenticationApi
from identity.api.client_applications_api import ClientApplicationsApi
from identity.api.delegation_api import DelegationApi
from identity.api.invitations_api import InvitationsApi
from identity.api.me_api import MeApi
from identity.api.members_api import MembersApi
from identity.api.registration_api import RegistrationApi
from identity.api.tenants_api import TenantsApi
from identity.api.users_api import UsersApi
