"""
API Routers Package
===================
Versioned API routers for clean endpoint organization.
"""

from .v1 import router as v1_router

__all__ = ["v1_router"]
