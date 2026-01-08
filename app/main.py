from fastapi import FastAPI
from app.api.routes import router
from app.core.database import Base, engine

# Import models so SQLAlchemy knows them
from app.models import page, post, comment, employee

#app = FastAPI(title="LinkedIn Insights Microservice")
#from fastapi import FastAPI
#from app.api.routes import router

app = FastAPI(
    title="LinkedIn Insights Microservice",
    description="""
    A backend service to fetch, store, and analyze LinkedIn Page insights.

    Features:
    - Scrape LinkedIn company pages
    - Store structured data in MySQL
    - Search & filter pages
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

#app.include_router(router)

#Base.metadata.create_all(bind=engine)

app.include_router(router)
