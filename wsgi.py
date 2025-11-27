#!/usr/bin/env python

# This file is the entry point in production mode

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
