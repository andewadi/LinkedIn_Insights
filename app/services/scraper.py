import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import re
import time


class LinkedInScraper:
    """
    Scraper responsible ONLY for fetching and parsing LinkedIn page data.
    No database logic here (Single Responsibility Principle).
    """

    BASE_URL = "https://www.linkedin.com/company/"

    def __init__(self, page_id: str):
        self.page_id = page_id
        self.page_url = f"{self.BASE_URL}{page_id}/"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        }

    # -----------------------------
    # Utility Methods
    # -----------------------------

    def _extract_followers(self, text: str) -> int:
        """
        Extract follower count from text like:
        '1,246 followers on LinkedIn'
        """
        try:
            match = re.search(r"([\d,]+)\s+followers", text.lower())
            if match:
                return int(match.group(1).replace(",", ""))
        except Exception:
            pass
        return 0

    # -----------------------------
    # Fetch HTML
    # -----------------------------

    def fetch_page_html(self) -> str:
        """
        Fetch raw HTML of the LinkedIn page.
        Returns empty string if blocked or failed.
        """
        try:
            response = requests.get(self.page_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return ""

    # -----------------------------
    # Parse Page Details
    # -----------------------------

    def parse_page_details(self, soup: BeautifulSoup) -> Dict:
        """
        Parse basic LinkedIn page information.
        Always returns a dictionary (never None).
        """
        data = {
            "page_id": self.page_id,
            "url": self.page_url,
            "name": self.page_id,
            "description": None,
            "website": None,
            "industry": None,
            "followers": 0,
            "headcount": None,
            "specialities": None,
            "profile_picture": None,
        }

        try:
            # Page title
            title = soup.find("title")
            if title:
                title_text = title.text.strip()
                data["name"] = title_text.replace(" | LinkedIn", "").strip()
                data["followers"] = self._extract_followers(title_text)

            # Meta description
            description = soup.find("meta", {"name": "description"})
            if description:
                desc_text = description.get("content", "")
                data["description"] = desc_text

                # Fallback follower extraction
                if data["followers"] == 0:
                    data["followers"] = self._extract_followers(desc_text)

        except Exception:
            pass

        return data

    # -----------------------------
    # Parse Posts (Best Effort)
    # -----------------------------

    def parse_posts(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract recent posts (best-effort).
        LinkedIn loads posts dynamically, so this is limited.
        """
        posts = []

        try:
            post_blocks = soup.find_all("div", limit=10)

            for block in post_blocks:
                content = block.get_text(strip=True)
                if content:
                    posts.append({
                        "content": content[:1000],
                        "likes": 0,
                        "comments": []
                    })
        except Exception:
            pass

        return posts

    # -----------------------------
    # Parse Employees (Best Effort)
    # -----------------------------

    def parse_employees(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract employee data (best-effort).
        """
        employees = []

        try:
            employee_blocks = soup.find_all("a", limit=5)
            for emp in employee_blocks:
                name = emp.get_text(strip=True)
                if name:
                    employees.append({
                        "name": name,
                        "title": None
                    })
        except Exception:
            pass

        return employees

    # -----------------------------
    # Main Scrape Orchestrator
    # -----------------------------

    def scrape(self) -> Dict:
        """
        Orchestrates the full scraping flow.
        ALWAYS returns safe default structures.
        """
        html = self.fetch_page_html()
        soup = BeautifulSoup(html, "html.parser")

        # Be polite to LinkedIn
        time.sleep(1)

        page_data = self.parse_page_details(soup)
        posts = self.parse_posts(soup)
        employees = self.parse_employees(soup)

        return {
            "page": page_data,
            "posts": posts,
            "employees": employees
        }
