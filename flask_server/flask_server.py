"""
Based on some things I've seen online, it's cleaner to use the application to just run the application. If we do this,
then we can use __init__.py for all the imports and object initializations, which helps avoid circular imports.
"""

from app import app

if __name__ == '__main__':
    app.run(debug=True)