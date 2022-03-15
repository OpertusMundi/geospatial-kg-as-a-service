from dataclasses import dataclass

from gkgaas.fagi.config import FAGIConfig
from gkgaas.fagi.rule import FAGIRulesSpec


@dataclass
class FAGIProfile:
    config: FAGIConfig
    rules: FAGIRulesSpec
