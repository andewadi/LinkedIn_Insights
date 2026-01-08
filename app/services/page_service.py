from sqlalchemy.orm import Session
from app.models.page import Page
from app.models.post import Post
from app.models.comment import Comment
from app.models.employee import Employee
from app.services.scraper import LinkedInScraper


class PageService:
    """
    Handles business logic related to LinkedIn Pages.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_page_by_page_id(self, page_id: str) -> Page | None:
        return self.db.query(Page).filter(Page.page_id == page_id).first()

    def create_page_with_related_data(self, scraped_data: dict) -> Page:
        page_data = scraped_data["page"]

        page = Page(
            page_id=page_data["page_id"],
            name=page_data["name"],
            url=page_data["url"],
            description=page_data["description"],
            website=page_data["website"],
            industry=page_data["industry"],
            followers=page_data["followers"],
            headcount=page_data["headcount"],
            specialities=page_data["specialities"],
            profile_picture=page_data["profile_picture"],
        )

        self.db.add(page)
        self.db.flush()

        for post_data in scraped_data.get("posts", []):
            post = Post(
                page_id=page.id,
                content=post_data.get("content"),
                likes=post_data.get("likes", 0),
            )
            self.db.add(post)
            self.db.flush()

            for comment_data in post_data.get("comments", []):
                comment = Comment(
                    post_id=post.id,
                    content=comment_data.get("content"),
                )
                self.db.add(comment)

        for emp_data in scraped_data.get("employees", []):
            employee = Employee(
                page_id=page.id,
                name=emp_data.get("name"),
                title=emp_data.get("title"),
            )
            self.db.add(employee)

        self.db.commit()
        self.db.refresh(page)
        return page

    def get_or_scrape_page(self, page_id: str) -> Page:
        page_id = page_id.strip()

        page = self.get_page_by_page_id(page_id)
        if page:
            return page

        scraper = LinkedInScraper(page_id)
        scraped_data = scraper.scrape()
        return self.create_page_with_related_data(scraped_data)
