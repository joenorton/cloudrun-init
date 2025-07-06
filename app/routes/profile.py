"""
Profile routes for cloudrun-init.
"""
from flask import Blueprint, request, jsonify, g, current_app
from app.auth.user_middleware import user_required, attach_user_to_request
from app.auth.firebase import login_required
from app.models.user import User
from app.ndb_client import with_ndb_context

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/', methods=['GET'])
@login_required
def get_profile():
    """
    Get current user's profile information.
    Requires Firebase authentication.
    """
    # Attach user model to request
    attach_user_to_request()
    
    if not g.user_model:
        return jsonify({'error': 'User not found in database'}), 500
    
    return jsonify({
        'user': g.user_model.to_dict(),
        'message': 'Profile retrieved successfully'
    }), 200


@profile_bp.route('/', methods=['PUT', 'PATCH'])
@login_required
def update_profile():
    """
    Update current user's profile information.
    Requires Firebase authentication.
    
    Expected JSON payload:
    {
        "display_name": "New Display Name"
    }
    """
    # Attach user model to request
    attach_user_to_request()
    
    if not g.user_model:
        return jsonify({'error': 'User not found in database'}), 500
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate input
        if 'display_name' in data:
            display_name = data['display_name']
            if not isinstance(display_name, str):
                return jsonify({'error': 'display_name must be a string'}), 400
            if len(display_name.strip()) == 0:
                return jsonify({'error': 'display_name cannot be empty'}), 400
            
            # Update user
            g.user_model.display_name = display_name.strip()
            g.user_model.put()
            
            current_app.logger.info(f"Updated display_name for user {g.user_model.uid}")
        
        return jsonify({
            'user': g.user_model.to_dict(),
            'message': 'Profile updated successfully'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Profile update error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@profile_bp.route('/stats', methods=['GET'])
@login_required
def get_user_stats():
    """
    Get user statistics and metadata.
    Requires Firebase authentication.
    """
    # Attach user model to request
    attach_user_to_request()
    
    if not g.user_model:
        return jsonify({'error': 'User not found in database'}), 500
    
    try:
        # Calculate some basic stats
        stats = {
            'account_age_days': None,
            'last_updated': g.user_model.updated_at.isoformat() if g.user_model.updated_at else None,
            'email_verified': g.user_model.email_verified,
            'provider': g.user_model.provider_id
        }
        
        # Calculate account age
        if g.user_model.created_at:
            from datetime import datetime
            now = datetime.utcnow()
            age_delta = now - g.user_model.created_at
            stats['account_age_days'] = age_delta.days
        
        return jsonify({
            'stats': stats,
            'message': 'User stats retrieved successfully'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"User stats error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@profile_bp.route('/sync', methods=['POST'])
@login_required
def sync_profile():
    """
    Sync user profile with latest Firebase data.
    Requires Firebase authentication.
    """
    try:
        # Attach user model to request
        attach_user_to_request()
        
        if not g.user_model:
            return jsonify({'error': 'User not found in database'}), 500
        
        # Update user with latest Firebase data
        g.user_model.update_from_firebase_user(g.user)
        
        current_app.logger.info(f"Synced profile for user {g.user_model.uid}")
        
        return jsonify({
            'user': g.user_model.to_dict(),
            'message': 'Profile synced successfully'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Profile sync error: {e}")
        return jsonify({'error': 'Internal server error'}), 500 