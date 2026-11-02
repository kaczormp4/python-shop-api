from fastapi import FastAPI
from mangum import Mangum
from shop_api.routes.orders import orders_router
from shop_api.routes.products import products_router
from shop_api.routes.public import public_router
from shop_api.routes.roles import roles_router
from shop_api.routes.user_roles import user_roles_router
from shop_api.routes.users import users_router

app = FastAPI(
    title="Shop API",
    version="1.0.0",
)

app.include_router(products_router)
app.include_router(orders_router)
app.include_router(roles_router)
app.include_router(users_router)
app.include_router(user_roles_router)
app.include_router(public_router)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


handler = Mangum(app, lifespan="off")
