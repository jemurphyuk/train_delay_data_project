# ingestion/__init__.py

"""
Ingestion package for UK train delay project.

Provides:
- NationalRailClient: API client for National Rail live data
- RawStorage: storage for raw departures
- DepartureIngestion: high-level ingestion job
"""

from client import NationalRailClient
from storage import RawStorage
from fetch_departures import DepartureIngestion

__all__ = [
    "NationalRailClient",
    "RawStorage",
    "DepartureIngestion",
]