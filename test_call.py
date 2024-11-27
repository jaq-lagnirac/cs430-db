# Justin Caringal
# A small test file to test the import of a Flask app into another file
import webbrowser as wb
from access_spotify import app
wb.open('http://127.0.0.1:5000/')
app.run()