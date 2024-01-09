# run.py
import sys
print(sys.path)

from src.app import create_app
from src.app.models import db

if __name__ == '__main__':
    app = create_app()

    # Initialize extensions
    db.init_app(app)

    # Create the database tables
    with app.app_context():
        db.create_all()


from src.app import create_app
from src.app.models import db

if __name__ == '__main__':
 src = create_app()

if __name__ == '__main__':
    # Create the database tables using Flask CLI command or initialization script
    app.run(host='0.0.0.0', port=5000, debug=True)
