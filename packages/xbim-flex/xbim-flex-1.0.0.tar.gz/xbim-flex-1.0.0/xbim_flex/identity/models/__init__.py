# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from identity.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from identity.model.application_type import ApplicationType
from identity.model.client_app import ClientApp
from identity.model.client_app_endpoint import ClientAppEndpoint
from identity.model.draft_invitation import DraftInvitation
from identity.model.invitation import Invitation
from identity.model.invitation_create import InvitationCreate
from identity.model.invitation_edit import InvitationEdit
from identity.model.invite_status import InviteStatus
from identity.model.master import Master
from identity.model.master_base import MasterBase
from identity.model.master_subscription import MasterSubscription
from identity.model.o_data_boolean import ODataBoolean
from identity.model.o_data_client_app_endpoint_list import ODataClientAppEndpointList
from identity.model.o_data_client_app_list import ODataClientAppList
from identity.model.o_data_int32 import ODataInt32
from identity.model.o_data_invitation_list import ODataInvitationList
from identity.model.o_data_string import ODataString
from identity.model.o_data_tenant_list import ODataTenantList
from identity.model.o_data_tenant_user_list import ODataTenantUserList
from identity.model.o_data_user_list import ODataUserList
from identity.model.problem_details import ProblemDetails
from identity.model.region import Region
from identity.model.region_info import RegionInfo
from identity.model.subscription import Subscription
from identity.model.team_member_create import TeamMemberCreate
from identity.model.team_member_edit import TeamMemberEdit
from identity.model.tenancy_type import TenancyType
from identity.model.tenant import Tenant
from identity.model.tenant_create import TenantCreate
from identity.model.tenant_edit import TenantEdit
from identity.model.tenant_role import TenantRole
from identity.model.tenant_user import TenantUser
from identity.model.token_err_response import TokenErrResponse
from identity.model.token_response import TokenResponse
from identity.model.user import User
from identity.model.user_create import UserCreate
from identity.model.user_tenant import UserTenant
