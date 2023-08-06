# pylint: skip-file
import ioc

from .decoder import JOSEPayloadDecoder
from .resolver import JOSEKeyResolver


def setup_ioc():
    if not ioc.is_satisfied('JOSEKeyResolver'):
        ioc.provide('JOSEKeyResolver', JOSEKeyResolver())
    if not ioc.is_satisfied('JOSEPayloadDecoder'):
        ioc.provide('JOSEPayloadDecoder', JOSEPayloadDecoder())
