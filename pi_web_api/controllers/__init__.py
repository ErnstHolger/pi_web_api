"""Convenience imports for controller classes."""

from __future__ import annotations

from .system import (
    HomeController,
    SystemController,
    ConfigurationController,
)

from .asset import (
    AssetServerController,
    AssetDatabaseController,
    ElementController,
    ElementCategoryController,
    ElementTemplateController,
)

from .attribute import (
    AttributeController,
    AttributeCategoryController,
    AttributeTemplateController,
)

from .data import (
    DataServerController,
    PointController,
)

from .analysis import (
    AnalysisController,
    AnalysisCategoryController,
    AnalysisRuleController,
    AnalysisTemplateController,
)

from .batch import (
    BatchController,
    CalculationController,
    ChannelController,
)

from .enumeration import (
    EnumerationSetController,
    EnumerationValueController,
)

from .event import EventFrameController

from .stream import (
    StreamController,
    StreamSetController,
)

from .table import TableController

__all__ = [
    'HomeController',
    'SystemController',
    'ConfigurationController',
    'AssetServerController',
    'AssetDatabaseController',
    'ElementController',
    'ElementCategoryController',
    'ElementTemplateController',
    'AttributeController',
    'AttributeCategoryController',
    'AttributeTemplateController',
    'DataServerController',
    'PointController',
    'AnalysisController',
    'AnalysisCategoryController',
    'AnalysisRuleController',
    'AnalysisTemplateController',
    'BatchController',
    'CalculationController',
    'ChannelController',
    'EnumerationSetController',
    'EnumerationValueController',
    'EventFrameController',
    'StreamController',
    'StreamSetController',
    'TableController',
]
