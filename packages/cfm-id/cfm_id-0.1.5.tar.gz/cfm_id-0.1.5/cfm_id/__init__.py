import pkg_resources
from .cfm_id import CfmId, CfmIdDocker, CfmIdTCP

__version__ = pkg_resources.get_distribution("cfm_id").version
__all__ = ["CfmId", "CfmIdDocker", "CfmIdTCP"]
