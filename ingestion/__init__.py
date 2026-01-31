# ingestion/__init__.py

"""
Ingestion package for UK train delay project.

Provides:
- TflClient: API client for TfL live data
- RawStorage: storage for raw departures
- DepartureIngestion: high-level ingestion job
"""

from client import TflClient
from storage import RawStorage
from fetch_departures import DepartureIngestion

__all__ = [
    "TflClient",
    "RawStorage",
    "DepartureIngestion",
]