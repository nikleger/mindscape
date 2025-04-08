"""
Routes package for the Mindscape API.

This package contains all the API route definitions organized by resource type.
Each module in this package represents a distinct resource or feature area.
"""

from . import mind_maps, nodes

__all__ = ['mind_maps', 'nodes'] 