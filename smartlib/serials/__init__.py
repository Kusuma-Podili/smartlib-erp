"""Serials Control and Continuing Resources Module.

Manages periodicals, journals, newspapers, standing orders, publication frequency
forecasting, predictive issue check-in, automated claims, routing lists, and bindery batches.
"""
from .models import (
    SerialTitle, Subscription, FrequencyPattern, IssueInstance, IssueStatus,
    ClaimNotice, BindingUnit, RoutingList
)
from .pattern_service import PatternService
from .prediction_engine import SerialsPredictionEngine
from .checkin_service import SerialsCheckinService
from .claims_service import SerialsClaimsService
from .binding_service import SerialsBindingService
