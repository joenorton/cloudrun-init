"""
User middleware for cloudrun-init.
Handles user persistence and attaches User model to Flask's g object.
"""
import functools
from flask import g, current_app, jsonify
from app.models.user import User
from app.ndb_client import with_ndb_context


@with_ndb_context
def get_or_create_user(firebase_user_info):
    """
    Get existing user or create new one from Firebase user info.
    
    Args:
        firebase_user_info (dict): User info from Firebase token
        
    Returns:
        User: User entity from database
    """
    # Try to get existing user
    user = User.get_by_uid(firebase_user_info['uid'])
    
    if user:
        # Update user info from Firebase (in case it changed)
        user.update_from_firebase_user(firebase_user_info)
        current_app.logger.debug(f"Updated existing user: {user.uid}")
    else:
        # Create new user
        user = User.create_from_firebase_user(firebase_user_info)
        current_app.logger.info(f"Created new user: {user.uid}")
    
    return user


def attach_user_to_request():
    """
    Middleware function to attach User model to Flask's g object.
    This should be called after Firebase authentication.
    """
    # Check if NDB is available
    if not current_app.config.get('NDB_AVAILABLE', True):
        current_app.logger.warning("NDB not available, skipping user model attachment")
        g.user_model = None
        return
    
    if hasattr(g, 'user') and g.user:
        try:
            # Get or create user in database
            user_model = get_or_create_user(g.user)
            g.user_model = user_model
            current_app.logger.debug(f"Attached user model to request: {user_model.uid}")
        except Exception as e:
            current_app.logger.error(f"Failed to attach user model: {e}")
            g.user_model = None
    else:
        g.user_model = None


def user_required(f):
    """
    Decorator to require both Firebase authentication and user persistence.
    
    Usage:
        @app.route('/protected')
        @user_required
        def protected_route():
            return jsonify({'user': g.user_model.to_dict()})
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated via Firebase
        if not hasattr(g, 'user') or not g.user:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Attach user model to request
        attach_user_to_request()
        
        if not g.user_model:
            return jsonify({'error': 'User not found in database'}), 500
        
        return f(*args, **kwargs)
    
    return decorated_function 