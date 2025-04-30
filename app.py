from flask import Flask, request, render_template_string
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        resume = request.form["resume"]
        jd = request.form["jd"]
        res_doc = nlp(resume)
        jd_doc = nlp(jd)
        res_keywords = set([token.lemma_.lower() for token in res_doc if not token.is_stop and token.is_alpha])
        jd_keywords = set([token.lemma_.lower() for token in jd_doc if not token.is_stop and token.is_alpha])
        match = res_keywords.intersection(jd_keywords)
        result = f"Match Score: {len(match)} / {len(jd_keywords)}\\nMatched Skills: {', '.join(match)}"
    return render_template_string('''
        <h2>AI Resume Analyzer</h2>
        <form method="POST">
            Resume:<br><textarea name="resume" rows="10" cols="50"></textarea><br><br>
            Job Description:<br><textarea name="jd" rows="10" cols="50"></textarea><br><br>
            <input type="submit" value="Analyze">
        </form>
        <pre>{{ result }}</pre>
    ''', result=result)

if __name__ == "__main__":
    app.run(debug=True)
