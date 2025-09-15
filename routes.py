from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os, uuid, json
from app import db
from models import SampleResult
from ai import analyze_image

bp = Blueprint("api", __name__)

ALLOWED_EXT = {"png", "jpg", "jpeg"}

def allowed_file(fname):
    return "." in fname and fname.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@bp.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    fname = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{fname}"
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
    file.save(save_path)

    counts, meta = analyze_image(save_path)

    sample = SampleResult(
        sample_id=uuid.uuid4().hex,
        image_path=save_path,
        counts_json=json.dumps({"counts": counts, "meta": meta})
    )
    db.session.add(sample)
    db.session.commit()

    return jsonify(sample.to_dict()), 201

@bp.route("/results", methods=["GET"])
def results():
    rows = SampleResult.query.order_by(SampleResult.timestamp.desc()).all()
    return jsonify([r.to_dict() for r in rows])

@bp.route("/results/<int:id>", methods=["GET"])
def get_result(id):
    r = SampleResult.query.get_or_404(id)
    return jsonify(r.to_dict())

@bp.route("/uploads/<path:filename>")
def serve_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
