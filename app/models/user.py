"""
User model for cloudrun-init using google-cloud-ndb.
"""
from google.cloud import ndb
from datetime import datetime


class User(ndb.Model):
    """
    User model representing a Firebase-authenticated user.
    
    Properties:
        uid: Firebase user ID (unique identifier)
        email: User's email address
        display_name: User's display name
        created_at: Timestamp when user was first created
        updated_at: Timestamp when user was last updated
        email_verified: Whether the user's email is verified
        picture: URL to user's profile picture
        provider_id: OAuth provider used for authentication
    """
    uid = ndb.StringProperty(required=True, indexed=True)
    email = ndb.StringProperty(required=True, indexed=True)
    display_name = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)
    email_verified = ndb.BooleanProperty(default=False)
    picture = ndb.StringProperty()
    provider_id = ndb.StringProperty()
    
    @classmethod
    def get_by_uid(cls, uid):
        """
        Get user by Firebase UID.
        
        Args:
            uid (str): Firebase user ID
            
        Returns:
            User: User entity if found, None otherwise
        """
        return cls.query(cls.uid == uid).get()
    
    @classmethod
    def get_by_email(cls, email):
        """
        Get user by email address.
        
        Args:
            email (str): User's email address
            
        Returns:
            User: User entity if found, None otherwise
        """
        return cls.query(cls.email == email).get()
    
    def to_dict(self):
        """
        Convert user entity to dictionary.
        
        Returns:
            dict: User data as dictionary
        """
        return {
            'uid': self.uid,
            'email': self.email,
            'display_name': self.display_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'email_verified': self.email_verified,
            'picture': self.picture,
            'provider_id': self.provider_id
        }
    
    @classmethod
    def create_from_firebase_user(cls, firebase_user_info):
        """
        Create a new user from Firebase user info.
        
        Args:
            firebase_user_info (dict): User info from Firebase token
            
        Returns:
            User: Newly created user entity
        """
        user = cls(
            uid=firebase_user_info['uid'],
            email=firebase_user_info['email'],
            display_name=firebase_user_info.get('name'),
            email_verified=firebase_user_info.get('email_verified', False),
            picture=firebase_user_info.get('picture'),
            provider_id=firebase_user_info.get('provider_id')
        )
        user.put()
        return user
    
    def update_from_firebase_user(self, firebase_user_info):
        """
        Update user from Firebase user info.
        
        Args:
            firebase_user_info (dict): User info from Firebase token
            
        Returns:
            User: Updated user entity
        """
        self.email = firebase_user_info['email']
        self.display_name = firebase_user_info.get('name', self.display_name)
        self.email_verified = firebase_user_info.get('email_verified', self.email_verified)
        self.picture = firebase_user_info.get('picture', self.picture)
        self.provider_id = firebase_user_info.get('provider_id', self.provider_id)
        self.put()
        return self 