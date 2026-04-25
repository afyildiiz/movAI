import os

from waitress import serve

from movai import create_app


def main():
    app = create_app()
    port = int(os.environ.get("PORT", 8000))
    serve(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
