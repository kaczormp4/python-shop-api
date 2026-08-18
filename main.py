from fastapi import FastAPI
from shop_api.routes.products import router as products_router

app = FastAPI()

app.include_router(products_router)
