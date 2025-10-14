from . import(
    post_controller
)

def register_routers(app):
    app.include_router(
        post_controller.router, prefix="/api", tags=["Linkedin Posts"]
    )