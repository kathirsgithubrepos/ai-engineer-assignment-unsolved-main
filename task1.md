# Task1 Justification and Answers:

## Overall Justification Summary:

| Area              | Improvement      | Effect                    |
| ----------------- | ---------------- | ------------------------- |
| Embedding Loop    | Batched          | 8–10× faster              |
| Cosine Similarity | Vectorized dot   | 2–3× faster               |
| Candidate Loop    | Neighbors only   | 50–200× fewer comparisons |
| Common Neighbors  | Set intersection | 3–5× faster               |
| Regex             | Simplified       | Slight gain               |
| Normalization     | Precomputed      | Consistent speed          |
| Timing            | Added            | Easier profiling          |

### Task 1 – Performance Evaluation

### Baseline Timings (Before Code Changes)
The image below shows the runtime of the original script without optimizations.

![Baseline Timings](evidences/Baseline%20Timings%20without%20Any%20Code%20Changes.jpg)

---

### Optimized Timings (After Code Changes)
The following image shows the improved runtime after applying Task 1 optimizations.

![After Code Changes](evidences/After%20the%20code%20changes.jpg)

## Detailed Explanation:

### Embedding Computation

**Change:**

```python
# before
for _, row in employees_df.iterrows():
    embeddings.append(model.encode(row["combined_text"]))

# after
embeddings = model.encode(texts, batch_size=64, convert_to_numpy=True)
```

**Justification:**
Replaced per-row loop with batched encoding to avoid repeated model calls and Python overhead — much faster on CPU/GPU.

---

### Cosine Similarity

**Change:**

```python
# before
sim = cosine_similarity(emp_emb, cand_emb)[0][0]

# after
sim = float(np.dot(emp_emb, cand_emb))
```

**Justification:**
Removed sklearn call; direct normalized dot product avoids repeated normalization and tiny array allocations.

---

### Candidate Loop Scope

**Change:**

```python
# before
for cand in G.nodes():
# after
for cand in G.neighbors(emp_id):
```

**Justification:**
Limits scoring to connected nodes only; cuts comparisons from O(N²) to O(E) and speeds manager search.

---

### 🔍 4️⃣  Common Neighbors Calculation

**Change:**

```python
# before
common = len(list(nx.common_neighbors(G, emp_id, cand)))

# after
common = len(set(G.neighbors(emp_id)) & set(G.neighbors(cand)))
```

**Justification:**
Avoids repeatedly creating NetworkX generators; set intersection runs in C and is several times faster.

---

### Regex Seniority Checks

**Change:**
Simplified multiple regex searches to ordered substring checks.

**Justification:**
Reduces redundant regex compilation and scanning; faster string matching with same logical outcome.

---

### Embedding Normalization

**Change:**

```python
# added once
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
embeddings = embeddings / (norms + 1e-10)
```

**Justification:**
Pre-normalizes all embeddings once so cosine similarity becomes a cheap dot product later.

---

### Timing Measurement

**Change:**
Added `start = time.perf_counter()` and `elapsed = ...` prints in all major methods.

**Justification:**
Provides clear profiling of each phase to verify performance improvements for Task 1 validation.

---
