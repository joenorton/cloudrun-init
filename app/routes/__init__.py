"""
Routes package for cloudrun-init.
"""
from app.routes.auth import auth_bp
from app.routes.profile import profile_bp

__all__ = ['auth_bp', 'profile_bp'] 