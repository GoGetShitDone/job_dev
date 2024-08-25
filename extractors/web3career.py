import requests
from bs4 import BeautifulSoup


def extract_web3_jobs(query):
    base_url = f"https://web3.career/{query}-jobs"
    jobs = []
    page = 1
    last_page_html = None

    while True:
        url = f"{base_url}?page={page}" if page > 1 else base_url
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        job_listings = soup.find_all("tr", class_="table_row")

        # 만약 현재 페이지가 이전 페이지와 동일한 HTML을 가지고 있다면 중지
        current_page_html = str(job_listings)
        if current_page_html == last_page_html:
            break
        last_page_html = current_page_html

        for job in job_listings:
            title_element = job.find("h2",
                                     class_="fs-6 fs-md-5 fw-bold my-primary")
            title = title_element.text.strip() if title_element else "N/A"

            company_element = job.find("h3",
                                       style="color: white; font-size: 12px;")
            company = company_element.text.strip(
            ) if company_element else "N/A"

            job_url_element = job.find("a", href=True)
            job_url = "https://web3.career" + job_url_element[
                "href"] if job_url_element else "N/A"

            salary_element = job.find("p", class_="ps-0 mb-0 text-salary")
            salary = salary_element.text.strip() if salary_element else "N/A"

            skills = [
                skill.text.strip()
                for skill in job.find_all("a", class_="text-shadow-1px")
            ]

            # N/A 값을 포함하는 데이터는 추가하지 않음
            if title != "N/A" and company != "N/A" and job_url != "N/A":
                jobs.append({
                    "position": title,
                    "company": company,
                    "link": job_url,
                    "salary": salary,
                    "skills": skills,
                    "source": "Web3 Career"
                })

        print(
            f"Scraped {len(jobs)} jobs from page {page} of Web3 Career: '{query}'"
        )
        page += 1

    print(f"Scraped a total of {len(jobs)} jobs from Web3 Career: '{query}'")
    return jobs
