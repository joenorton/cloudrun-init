"""
Authentication routes for cloudrun-init.
"""
from flask import Blueprint, request, jsonify, g, current_app
from app.auth.firebase import login_required, optional_login, verify_firebase_token, get_token_from_request

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint that verifies Firebase token.
    
    Expected JSON payload:
    {
        "idToken": "firebase_id_token_here"
    }
    """
    try:
        data = request.get_json()
        if not data or 'idToken' not in data:
            return jsonify({'error': 'Missing idToken in request body'}), 400
        
        id_token = data['idToken']
        
        # Verify the token
        user_info = verify_firebase_token(id_token)
        if not user_info:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Create response
        response = jsonify({
            'message': 'Login successful',
            'user': user_info
        })
        
        # Set token in cookie for future requests
        response.set_cookie(
            'firebase_token',
            id_token,
            httponly=True,
            secure=not current_app.debug,  # Only secure in production
            samesite='Lax',
            max_age=3600  # 1 hour
        )
        
        return response, 200
        
    except Exception as e:
        current_app.logger.error(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout endpoint that clears the authentication token."""
    response = jsonify({'message': 'Logout successful'})
    response.delete_cookie('firebase_token')
    return response, 200


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """
    Protected endpoint that returns current user information.
    Requires valid Firebase authentication token.
    """
    return jsonify({
        'user': g.user,
        'authenticated': True
    })


@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """
    Verify a Firebase token without logging in.
    
    Expected JSON payload:
    {
        "idToken": "firebase_id_token_here"
    }
    """
    try:
        data = request.get_json()
        if not data or 'idToken' not in data:
            return jsonify({'error': 'Missing idToken in request body'}), 400
        
        id_token = data['idToken']
        
        # Verify the token
        user_info = verify_firebase_token(id_token)
        if not user_info:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        return jsonify({
            'valid': True,
            'user': user_info
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Token verification error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/status', methods=['GET'])
@optional_login
def auth_status():
    """
    Check authentication status.
    Returns user info if authenticated, None if not.
    """
    return jsonify({
        'authenticated': g.user is not None,
        'user': g.user
    }) 