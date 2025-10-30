from flask import Flask, request, jsonify, Response
import base64
import io
import pandas as pd
import tempfile
import os
import time
import traceback
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, request, jsonify, Response
from sentence_transformers import SentenceTransformer
from dependencies.visualize_sunburst import visualize_sunburst_hierarchy
from scripts import solution
app = Flask(__name__)
MODEL = SentenceTransformer("all-MiniLM-L6-v2")
try:
    _ = MODEL.encode(["warmup"], convert_to_numpy=True)
except Exception:
    pass

def df_from_b64(b64):
    return pd.read_csv(io.BytesIO(base64.b64decode(b64)))

@app.route("/predict", methods=["POST"])
def predict():
    t0 = time.perf_counter()
    try:
        data = request.get_json(force=True)
        if not data or "employees_csv_base64" not in data or "connections_csv_base64" not in data:
            return jsonify({"error": "missing fields"}), 400
        employees_df = df_from_b64(data["employees_csv_base64"])
        connections_df = df_from_b64(data["connections_csv_base64"])
        t1 = time.perf_counter()
        submission_df = solution.run_prediction_from_dfs(employees_df, connections_df, model=MODEL, batch_size=128)
        t2 = time.perf_counter()
        with tempfile.TemporaryDirectory() as tmpdir:
            employees_path = os.path.join(tmpdir, "employees.csv")
            submission_path = os.path.join(tmpdir, "submission.csv")
            out_html = os.path.join(tmpdir, "employee_sunburst.html")
            employees_df.to_csv(employees_path, index=False)
            submission_df.to_csv(submission_path, index=False)
            visualize_sunburst_hierarchy(employees_path, submission_path, out_html)
            with open(out_html, "rb") as f:
                html_bytes = f.read()
        t3 = time.perf_counter()
        headers = {
            "X-Time-Decode": f"{t1 - t0:.3f}s",
            "X-Time-Predict": f"{t2 - t1:.3f}s",
            "X-Time-Visualize": f"{t3 - t2:.3f}s",
            "X-Time-Total": f"{t3 - t0:.3f}s"
        }
        return Response(html_bytes, status=200, mimetype="text/html", headers=headers)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001, threaded=True)