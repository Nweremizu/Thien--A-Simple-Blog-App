from app import app,db
import os

@app.shell_context_processor
def make_shell_context():
    return {'app': app}


if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG', False))
