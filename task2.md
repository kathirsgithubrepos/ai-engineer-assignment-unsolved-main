## ✅ Task 2 — Serving Optimization Proof

### 🔧 Changes (Short & Simple Justification)

| Optimization             | Before                   | After                                                              | Why                                     |
| ------------------------ | ------------------------ | ------------------------------------------------------------------ | --------------------------------------- |
| Preload model once       | Load model every request | `MODEL = SentenceTransformer('all-MiniLM-L6-v2')` at app startup   | Removes repeated heavy loading          |
| Predict in-process       | `subprocess.run(...)`    | Call `build_graph_with_features()` + `predict_managers()` directly | Avoids new Python process → faster      |
| In-process visualization | `subprocess.run(...)`    | `visualize_sunburst_hierarchy(...)`                                | Removes extra process; faster & cleaner |
| Safe temp handling       | Manual temp cleanup      | `with tempfile.TemporaryDirectory()`                               | Auto cleanup; no leftover tmp folders   |

---

### 📸 Before Optimization

**Performance Before: Total Time : 44 Seconds**

![Before Code Changes](evidences/task2/Before%20Code%20Changes.jpg)

**cURL Response Before**

[View HTML Output](evidences/task2/Before%20Code%20changes%20curl_response.html)

---

### 🚀 After Optimization

**Performance After Total Time : 16 Seconds**

![After Code Changes](evidences/task2/After%20Code%20Changes.jpg)

**cURL Response After**

[View HTML Output](evidences/task2/After%20code%20changes%20curl_response.html)

---

### ✅ Test Evidence

**Unit Tests Passed**

![Test cases passed](evidences/task2/Test%20cases%20passed.jpg)

---