from injectark import FactoryBuilder
from .base_factory import BaseFactory
from .altair_factory import AltairFactory
from .check_factory import CheckFactory
from .rst_factory import RstFactory
from .json_factory import JsonFactory


factory_builder = FactoryBuilder([
    BaseFactory, CheckFactory, AltairFactory, JsonFactory, RstFactory])
