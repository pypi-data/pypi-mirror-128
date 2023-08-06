try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    __path__ = __import__('pkgutil').extend_path(__path__, __name__)

from naver_config import NaverConfig 
from .rules import *
from .workflow import *

class NaverBs(NaverConfig):
    def __init__(self): 
        self.rule = Rule()
        self.workflow = Workflow()

    