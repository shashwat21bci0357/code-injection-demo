from flask import Flask, request, render_template_string

app = Flask(__name__)

VULNERABLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Calculator</title>
</head>
<body>
    <h2>Vulnerable Expression Evaluator</h2>
    <form method="post">
        <input type="text" name="expression" placeholder="Enter an expression" required>
        <input type="submit" value="Evaluate">
    </form>
    {% if result is not none %}
        <h3>Result: {{ result }}</h3>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_input = request.form.get("expression", "")
        try:
            # ⚠️ ALLOWING DANGEROUS CODE EXECUTION
            result = eval(user_input, {"__builtins__": {"open": open}}, {})  
        except Exception as e:
            result = f"Error: {e}"

    return render_template_string(VULNERABLE_HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
