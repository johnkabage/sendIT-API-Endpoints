import os
from APP.Api import create_app

app = create_app(os.getenv("APP_SETTINGS") or "development")

if __name__ == "__main__":
    app.run()