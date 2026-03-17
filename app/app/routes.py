from flask import Blueprint
bp = Blueprint("main", __name__)

@bp.route("/health")
def health():
    return "ok"
