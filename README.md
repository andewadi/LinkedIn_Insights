# LinkedIn Insights Microservice

A backend microservice built using **FastAPI** and **MySQL** to fetch, store, and retrieve insights of LinkedIn company pages using a given **Page ID**.

This project was developed as part of a **GenAI Developer Intern assignment**, focusing on clean backend architecture, RESTful API design, and maintainable code practices.

---

## 🚀 Features

- Fetch LinkedIn Page insights using Page ID
- Scrape public LinkedIn page metadata (best-effort)
- Store structured data in MySQL
- REST APIs to retrieve:
  - Page details
  - Search pages with filters
  - Recent posts
  - Employees (best-effort)
- Pagination support
- Swagger UI for API documentation
- Postman collection support
- Clean separation of concerns (Scraper, Service, API layers)

---

## 🧱 Tech Stack

| Layer | Technology |
|-----|------------|
| Language | Python 3.10+ |
| Backend Framework | FastAPI |
| Database | MySQL |
| ORM | SQLAlchemy |
| Scraping | Requests + BeautifulSoup |
| API Docs | Swagger UI (FastAPI) |
| Testing Tool | Postman |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

linkedin_insights/
│
├── app/
│ ├── main.py
│ ├── api/
│ │ └── routes.py
│ ├── core/
│ │ ├── database.py
│ │ └── config.py
│ ├── models/
│ │ ├── page.py
│ │ ├── post.py
│ │ ├── comment.py
│ │ └── employee.py
│ ├── services/
│ │ ├── scraper.py
│ │ └── page_service.py
│ └── schemas/
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env

🧪 Testing with Postman

All APIs are tested using Postman

A Postman collection can be exported and shared

Environment variables are used for base URL

⚠️ Scraping Disclaimer

LinkedIn pages are mostly client-side rendered, so scraping is implemented as best-effort using public metadata.
Some pages may return partial or limited data.

This approach is acceptable for backend demonstration and learning purposes.

🧠 Design Principles Followed

SOLID principles

Single Responsibility Principle

Clean code practices

RESTful API standards

Separation of concerns

🔮 Future Enhancements

AI-generated page summaries

Async scraping & DB operations

Redis caching

Dockerization

Frontend dashboard

Authentication & rate limiting

👨‍💻 Author
Pragati Andewadi
