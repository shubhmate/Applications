from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)

# CONFIGURATION
# Replace <password> and <cluster_url> with your real Atlas details
MONGO_URI = ""
client = MongoClient(MONGO_URI)
db = client['my_database']
collection = db['submissions']

# TASK: FORM SUBMISSION
@app.route('/', methods=['GET', 'POST'])
def handle_form():
    error = None
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            # Insert into MongoDB Atlas
            collection.insert_one({"name": name, "email": email})
            return redirect(url_for('success_page'))
        except PyMongoError as e:
            # Display error on same page without redirecting
            error = f"Database error: {str(e)}"
    return render_template('form.html', error=error)

@app.route('/success')
def success_page():
    return "<h1>Data submitted successfully</h1>"

if __name__ == '__main__':
    app.run(debug=True)
