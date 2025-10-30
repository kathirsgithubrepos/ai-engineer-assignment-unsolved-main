import pandas as pd
import numpy as np
import networkx as nx
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import argparse
import time

WEIGHT_EMBEDDING_SIMILARITY = 1.0
WEIGHT_COMMON_NEIGHBORS = 1.0
WEIGHT_SENIORITY_GAP = 1.0
WEIGHT_LOCATION_MATCH = 1.0


def get_seniority(title):
    if pd.isna(title):
        return 2
    t = str(title).lower()
    if 'chief' in t or 'ceo' in t:
        return 7
    if 'vp' in t or 'vice president' in t:
        return 6
    if 'director' in t or 'head' in t:
        return 5
    if 'manager' in t or 'lead' in t:
        return 4
    if 'senior' in t or 'principal' in t or 'sr.' in t:
        return 3
    if 'junior' in t or 'entry' in t or 'associate' in t:
        return 1
    return 2

def build_graph_with_features(employees_df, connections_df, model=None, batch_size=128):
    start = time.perf_counter()
    employees_df["combined_text"] = (
        employees_df["job_title_current"].fillna("") + ". " +
        employees_df["profile_summary"].fillna("")
    )
    model = model or SentenceTransformer("all-MiniLM-L6-v2")
    texts = employees_df["combined_text"].tolist()
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=False, convert_to_numpy=True)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / (norms + 1e-10)
    employees_df["embedding"] = list(embeddings)
    employees_df["seniority_score"] = employees_df["job_title_current"].apply(get_seniority)
    G = nx.Graph()
    for _, row in connections_df.iterrows():
        G.add_edge(row["employee_id_a"], row["employee_id_b"])
    for _, row in employees_df.iterrows():
        G.nodes[row["employee_id"]]["embedding"] = row["embedding"]
        G.nodes[row["employee_id"]]["seniority_score"] = row["seniority_score"]
        G.nodes[row["employee_id"]]["location"] = row.get("location", None)
    elapsed = time.perf_counter() - start
    print(f"build_graph_with_features() completed in {elapsed:.3f}s")
    return G

def score_potential_managers(emp_id, G):
    start = time.perf_counter()
    emp_data = G.nodes[emp_id]
    emp_emb = emp_data["embedding"]
    emp_sen = emp_data["seniority_score"]
    emp_loc = emp_data.get("location", None)
    best_score, best_mgr = -1e9, None
    emp_neighbors = list(G.neighbors(emp_id))
    emp_neighbor_sets = {n: set(G.neighbors(n)) for n in emp_neighbors}
    for cand in emp_neighbors:
        cand_data = G.nodes[cand]
        sen_gap = cand_data["seniority_score"] - emp_sen
        if sen_gap <= 0:
            continue
        cand_emb = cand_data["embedding"]
        sim = float(np.dot(emp_emb, cand_emb))
        common = len(emp_neighbor_sets[cand] & set(emp_neighbors))
        score = (
            sim * WEIGHT_EMBEDDING_SIMILARITY +
            common * WEIGHT_COMMON_NEIGHBORS +
            (1.0 / sen_gap) * WEIGHT_SENIORITY_GAP
        )
        if cand_data.get("location") == emp_loc:
            score += WEIGHT_LOCATION_MATCH
        if score > best_score:
            best_score, best_mgr = score, cand
    elapsed = time.perf_counter() - start
    #print(f"score_potential_managers({emp_id}) completed in {elapsed:.3f}s")
    return best_mgr

def predict_managers(G):
    start = time.perf_counter()
    predictions = {}
    for emp in tqdm(G.nodes(), desc="Predicting managers"):
        mgr = score_potential_managers(emp, G)
        if mgr:
            predictions[emp] = mgr
    elapsed = time.perf_counter() - start
    print(f"predict_managers() completed in {elapsed:.3f}s")
    return predictions

def run_prediction_from_dfs(employees_df, connections_df, model=None, batch_size=128):
    start = time.perf_counter()
    G = build_graph_with_features(employees_df.copy(), connections_df.copy(), model=model, batch_size=batch_size)
    manager_predictions = predict_managers(G)
    predictions_df = pd.DataFrame(manager_predictions.items(), columns=["employee_id", "manager_id"])
    all_employees_df = employees_df[["employee_id"]]
    submission_df = pd.merge(all_employees_df, predictions_df, on="employee_id", how="left")
    submission_df["manager_id"] = submission_df["manager_id"].fillna(0).astype(int)
    if 358 in submission_df["employee_id"].values:
        submission_df.loc[submission_df["employee_id"] == 358, "manager_id"] = -1
    elapsed = time.perf_counter() - start
    print(f"run_prediction_from_dfs() completed in {elapsed:.3f}s")
    return submission_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--employees_path", default="data/employees.csv")
    parser.add_argument("--connections_path", default="data/connections.csv")
    parser.add_argument("--output_path", default="submission.csv")
    parser.add_argument("--batch_size", type=int, default=128)
    args = parser.parse_args()
    start = time.perf_counter()
    employees = pd.read_csv(args.employees_path)
    connections = pd.read_csv(args.connections_path)
    submission_df = run_prediction_from_dfs(employees, connections, model=None, batch_size=args.batch_size)
    submission_df.to_csv(args.output_path, index=False)
    elapsed = time.perf_counter() - start
    print(f"Processing complete in {elapsed:.3f}s. Saved to {args.output_path}")
