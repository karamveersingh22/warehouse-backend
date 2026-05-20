from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database.mongodb import connect_db, close_db
from app.routes import auth, products


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="Warehouse Inventory Management API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    # NOTE: CORS must match the browser Origin exactly (no trailing slash).
    # Keep explicit local dev origins, and allow Vercel preview/prod domains via regex.
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://godown-frontend-rust.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)


@app.get("/")
async def root():
    return {"message": "Warehouse API is running"}
