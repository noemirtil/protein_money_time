from flask import Blueprint, render_template


# After importing Blueprint, you create an instance of it named bp.
# The first argument, "pages", is the name of your blueprint.
# You’ll use this name to identify this particular blueprint in your Flask project.
# The second argument is the blueprint’s __name__.
# You’ll use this later when you import pages into __init__.py.
bp = Blueprint("pages", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/about")
def about():
    return render_template("about.html")
