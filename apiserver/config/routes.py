from fastapi import APIRouter
from controllers.request_controller import router as request_router

def setup_routes(app):
    """
    Configure all application routes
    """
    # Include product controller routes
    app.include_router(request_router, prefix="/api/requests", tags=["requests"])
    
    # Add additional controllers here as needed
    
    # Return the app instance with configured routes
    return app