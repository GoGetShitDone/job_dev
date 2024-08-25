from flask import Flask, render_template, request, send_file
from werkzeug.utils import redirect
from extractors.berlinstart import extract_berlinstart_jobs
from extractors.web3career import extract_web3_jobs
from file import save_to_file

app = Flask("Job_Dev")


@app.route("/")
def home():
    return render_template("home.html", name="David")


db = {}


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        web3_jobs = extract_web3_jobs(keyword)
        berlin_jobs = extract_berlinstart_jobs(keyword)
        jobs = web3_jobs + berlin_jobs
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)


app.run("0.0.0.0")
#app.run("0.0.0.0", port=8000) 또한 고려 가능