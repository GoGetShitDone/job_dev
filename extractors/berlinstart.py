import requests
from bs4 import BeautifulSoup


def extract_berlinstart_jobs(query):
    url = f"https://berlinstartupjobs.com/?s={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    job_listings = soup.find_all("article", class_="bjs-jlid")

    jobs = []
    for job in job_listings:
        title_element = job.find("h4", class_="bjs-jlid__h")
        title = title_element.text.strip() if title_element else "N/A"

        company_element = job.find("a", class_="bjs-jlid__b")
        company = company_element.text.strip() if company_element else "N/A"

        job_url_element = title_element.find("a") if title_element else None
        job_url = job_url_element[
            'href'] if job_url_element and 'href' in job_url_element.attrs else "N/A"

        skills = [
            skill.text.strip() for skill in job.find_all("a", class_="bjs-bl")
        ]

        jobs.append({
            "position": title,
            "company": company,
            "link": job_url,
            "skills": skills,
            "source": "Berlin Start Jobs"
        })

    print(f"Scraped {len(jobs)} jobs from Berlin Start Jobs: '{query}'")
    return jobs
