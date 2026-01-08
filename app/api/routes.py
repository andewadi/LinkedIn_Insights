from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.database import get_db
from app.services.page_service import PageService
from app.models.page import Page
from app.models.post import Post
from app.models.employee import Employee

router = APIRouter(prefix="/pages", tags=["LinkedIn Pages"])
@router.get("/{page_id}")
def get_page(page_id: str, db: Session = Depends(get_db)):
    service = PageService(db)

    try:
        page = service.get_or_scrape_page(page_id)
        return page
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
@router.get("/")
def search_pages(
    name: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    min_followers: Optional[int] = Query(None),
    max_followers: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(Page)

    if name:
        query = query.filter(Page.name.ilike(f"%{name}%"))

    if industry:
        query = query.filter(Page.industry.ilike(f"%{industry}%"))

    if min_followers is not None:
        query = query.filter(Page.followers >= min_followers)

    if max_followers is not None:
        query = query.filter(Page.followers <= max_followers)

    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "results": results
    }
@router.get("/{page_id}/posts")
def get_recent_posts(
    page_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=20),
    db: Session = Depends(get_db),
):
    linked_page = db.query(Page).filter(Page.page_id == page_id).first()

    if not linked_page:
        raise HTTPException(status_code=404, detail="Page not found")

    offset = (page - 1) * limit

    posts = (
        db.query(Post)
        .filter(Post.page_id == linked_page.id)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return posts
@router.get("/{page_id}/employees")
def get_employees(
    page_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db),
):
    linked_page = db.query(Page).filter(Page.page_id == page_id).first()

    if not linked_page:
        raise HTTPException(status_code=404, detail="Page not found")

    offset = (page - 1) * limit

    employees = (
        db.query(Employee)
        .filter(Employee.page_id == linked_page.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return employees
@router.get(
    "/pages/{page_id}",
    tags=["LinkedIn Pages"],
    summary="Get LinkedIn Page Details",
    description="Fetch page details by Page ID. Scrapes data if not present in DB."
)
def get_page(page_id: str, db: Session = Depends(get_db)):
    ...
