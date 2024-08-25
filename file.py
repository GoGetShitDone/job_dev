import csv


def save_to_file(file_name, jobs):
    with open(f"{file_name}.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Position", "Company", "Location", "URL"])

        for job in jobs:
            writer.writerow([
                job['position'], job['company'], job['location'], job['link']
            ])

    print(f"Saved {len(jobs)} jobs to {file_name}.csv")
