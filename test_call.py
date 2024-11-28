#!/.venv/bin/python3

# Justin Caringal
# A small test file to test the import of a Flask app into another file
import webbrowser as wb
from multiprocessing import Process
from access_spotify import app
if __name__ == '__main__':
    server = Process(target=app.run)
    server.start()
    wb.open('http://127.0.0.1:5000/')
