"""
NDB client configuration for cloudrun-init.
"""
import os
from google.cloud import ndb
from flask import current_app


def init_ndb_client():
    """
    Initialize NDB client for the application.
    
    Returns:
        ndb.Client: Configured NDB client
    """
    # Get project ID from environment or config
    project_id = os.environ.get('DATASTORE_PROJECT_ID') or \
                 os.environ.get('GOOGLE_CLOUD_PROJECT') or \
                 current_app.config.get('GOOGLE_CLOUD_PROJECT')
    
    # For local development with emulator
    if os.environ.get('DATASTORE_EMULATOR_HOST'):
        # Use emulator settings
        client = ndb.Client(project=project_id or 'fake-project')
        current_app.logger.info(f"Using Datastore emulator at {os.environ.get('DATASTORE_EMULATOR_HOST')}")
    else:
        # Use production settings
        if project_id:
            client = ndb.Client(project=project_id)
            current_app.logger.info(f"Using Datastore project: {project_id}")
        else:
            # Fallback for local development without emulator
            client = ndb.Client()
            current_app.logger.warning("No project ID specified, using default NDB client")
    
    return client


def get_ndb_context():
    """
    Get NDB context for database operations.
    
    Returns:
        ndb.Context: Active NDB context
    """
    client = init_ndb_client()
    return client.context()


def with_ndb_context(func):
    """
    Decorator to provide NDB context for database operations.
    
    Usage:
        @with_ndb_context
        def my_database_function():
            user = User.get_by_uid('some_uid')
            return user
    """
    def wrapper(*args, **kwargs):
        context = get_ndb_context()
        with context:
            return func(*args, **kwargs)
    return wrapper 