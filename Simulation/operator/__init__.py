# Init of Operator module

# Import modules
from .operator_base import Operator
from .kernel import BlOpenCLKernelOperator
from .kernel_test import BlKernelTestOperator
from .script import BlPythonScriptOperator
from .import_geo import BlImportGeoOperator
from .export_geo import BlExportGeoOperator
from .simulation import BlSimInputOperator, BlSimOutputOperator
from .create_float import BlCreateFloatOperator
from .create_integer import BlCreateIntegerOperator
from .create_vector import BlCreateVectorOperator
from .kernel_copy import BlKernelCopyOperator
from .create_attribute import BlCreateAttributeOperator
from .import_oct import BlImportOctOperator

__all__ = ['Operator',
           'BlOpenCLKernelOperator',
           'BlKernelTestOperator',
           'BlPythonScriptOperator',
           'BlImportGeoOperator',
           'BlExportGeoOperator',
           'BlSimInputOperator',
           'BlSimOutputOperator',
           'BlCreateFloatOperator',
           'BlCreateIntegerOperator',
           'BlCreateVectorOperator',
           'BlKernelCopyOperator',
           'BlCreateAttributeOperator',
           'BlImportOctOperator'
           ]