from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/members')
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

if __name__ == "__main__":
    app.run(debug=True)