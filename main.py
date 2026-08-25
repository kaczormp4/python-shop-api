from fastapi import FastAPI
from shop_api.routes.orders import orders_router
from shop_api.routes.products import products_router
from shop_api.routes.roles import roles_router
from shop_api.routes.users import users_router

app = FastAPI()

app.include_router(products_router)
app.include_router(orders_router)
app.include_router(roles_router)
app.include_router(users_router)
