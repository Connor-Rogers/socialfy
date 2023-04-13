from app import app_factory
application = app_factory()
if __name__ == "__main__":
    application.run('0.0.0.0', 8000, threaded=True)
