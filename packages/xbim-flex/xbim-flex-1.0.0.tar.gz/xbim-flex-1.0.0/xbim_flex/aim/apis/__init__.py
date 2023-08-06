
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
from aim.api.admin_api import AdminApi
from aim.api.applications_api import ApplicationsApi
from aim.api.assemblies_api import AssembliesApi
from aim.api.assets_api import AssetsApi
from aim.api.attributes_api import AttributesApi
from aim.api.component_types_api import ComponentTypesApi
from aim.api.components_api import ComponentsApi
from aim.api.contacts_api import ContactsApi
from aim.api.diagnostics_api import DiagnosticsApi
from aim.api.document_files_api import DocumentFilesApi
from aim.api.documents_api import DocumentsApi
from aim.api.entities_api import EntitiesApi
from aim.api.facilities_api import FacilitiesApi
from aim.api.issues_api import IssuesApi
from aim.api.jobs_api import JobsApi
from aim.api.levels_api import LevelsApi
from aim.api.logs_api import LogsApi
from aim.api.model_files_api import ModelFilesApi
from aim.api.model_mapping_api import ModelMappingApi
from aim.api.models_api import ModelsApi
from aim.api.resources_api import ResourcesApi
from aim.api.schedules_api import SchedulesApi
from aim.api.sites_api import SitesApi
from aim.api.spaces_api import SpacesApi
from aim.api.spares_api import SparesApi
from aim.api.stats_api import StatsApi
from aim.api.systems_api import SystemsApi
from aim.api.thumbnails_api import ThumbnailsApi
from aim.api.wexbim_api import WexbimApi
from aim.api.zones_api import ZonesApi
