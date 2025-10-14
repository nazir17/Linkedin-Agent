from fastapi import FastAPI
from app.controllers import register_routers
from app.controllers.post_controller import router as post_router
from app.configs.database import test_connection, init_models


app = FastAPI(title='LinkedIn AI Agent')

register_routers(app)


@app.on_event("startup")
async def on_startup():
    await test_connection()
    await init_models()


@app.get('/')
async def root():
    return {'status': 'ok'}
