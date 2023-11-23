# Imports modules from packages
from website import create_app

# Creating the Flask application
app = create_app()

if __name__ == '__main__':
    app.run(port=5001, debug=True)
