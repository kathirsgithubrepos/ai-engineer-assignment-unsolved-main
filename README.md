## Submission Report

### Project: AI Engineer Assignment

All tasks completed with evidence screenshots attached.

---

## 🧠 Task 1: Code Optimization Improvements

| Area              | Improvement      | Effect                    |
| ----------------- | ---------------- | ------------------------- |
| Embedding Loop    | Batched          | 8–10× faster              |
| Cosine Similarity | Vectorized dot   | 2–3× faster               |
| Candidate Loop    | Neighbors only   | 50–200× fewer comparisons |
| Common Neighbors  | Set intersection | 3–5× faster               |
| Regex             | Simplified       | Slight gain               |
| Normalization     | Precomputed      | Consistent speed          |
| Timing            | Added            | Easier profiling          |

#### 📎 Evidence 

##### Baseline Timings (Before Code Changes)
The image below shows the runtime of the original script without optimizations.

![Baseline Timings](submission_files/task1/Baseline%20Timings%20without%20Any%20Code%20Changes.jpg)

---

##### Optimized Timings (After Code Changes)
The following image shows the improved runtime after applying Task 1 optimizations.

![After Code Changes](submission_files/task1/After%20the%20code%20changes.jpg)


## ⚙️ Task 2: API Performance Optimization

| Optimization             | Before                   | After                                         | Why                                |
| ------------------------ | ------------------------ | --------------------------------------------- | ---------------------------------- |
| Preload model once       | Load model every request | `MODEL = SentenceTransformer(...)` at startup | Removes repeated heavy loading     |
| Predict in-process       | `subprocess.run(...)`    | Direct Python calls                           | Avoids spawning new Python process |
| In-process visualization | `subprocess.run(...)`    | Direct visualization call                     | Faster, cleaner                    |
| Safe temp handling       | Manual temp cleanup      | `with tempfile.TemporaryDirectory()`          | No leftover tmp files              |

#### 📎 Evidence

##### Before Optimization

**Performance Before: Total Time : 44 Seconds**

![Before Code Changes](submission_files/task2/Before%20Code%20Changes.jpg)

---

#####  After Optimization

**Performance After Total Time : 16 Seconds**

![After Code Changes](submission_files/task2/After%20Code%20Changes.jpg)

---

### ✅ Test Evidence

**Unit Tests Passed**

![Test cases passed](submission_files/task2/Test%20cases%20passed.jpg)

## 🐳 Task 3: Containerization & Local Serving

| Requirement                | Solution                                      |
| -------------------------- | --------------------------------------------- |
| Use multi-stage Dockerfile | ✅ Two-stage (`builder` + `runtime`)           |
| Avoid copying `.venv`      | ✅ `.dockerignore` updated                     |
| CPU-only image             | ✅ Lightweight CPU PyTorch                     |
| Entrypoint                 | ✅ `ENTRYPOINT ["python", "serving/serve.py"]` |
| Port Exposed               | ✅ `EXPOSE 5001`                               |
| Local test                 | ✅ Successful run & response via curl          |

##### Container Running

![Container Running](submission_files/task3/container%20running.jpg)

##### Local Test Execution Success

![Test Executed Locally](submission_files/task3/test%20executed%20locally%20.jpg)


## Task 4: PR-based CI Model Evaluation

### Summary

Two PRs created to simulate improvement vs regression detection:

| Branch                       | Change                          | Expected Outcome  | Purpose                |
| ---------------------------- | ------------------------------- | ----------------- | ---------------------- |
| `location_match_tweak`       | Location weight ↑               | ❌ Lower accuracy  | Regression test        |
| `embedding_similarity_tweak` | Embedding & neighbors weights ↑ | ✅ Higher accuracy | Improvement validation |

CI successfully

* Detected regresion
* Approved improvement
* Posted results on PR
* Protected main branch

#### 🔗 PR Evidence

| Scenario       | Link                                                                                                                                                                   |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Improvement PR | [https://github.com/kathirsgithubrepos/ai-engineer-assignment-unsolved-main/pull/5](https://github.com/kathirsgithubrepos/ai-engineer-assignment-unsolved-main/pull/5) |
| Regression PR  | [https://github.com/kathirsgithubrepos/ai-engineer-assignment-unsolved-main/pull/4](https://github.com/kathirsgithubrepos/ai-engineer-assignment-unsolved-main/pull/4) |

#### 📎 Screenshots


![Pull request with verdict1](submission_files/task4/Pull%20request%20with%20verdict%201.jpg) 
![Pull request with verdict2](submission_files/task4/Pull%20request%20with%20verdict%202.jpg)


## Task 5: Deployment

| Step                      | Status |
| ------------------------- | ------ |
| Packaged & built Docker   | ✅      |
| Pushed to GitHub Packages | ✅      |
| Deployment Verified       | ✅      |

#### 🔗 Build Pipeline Run

[https://github.com/kathirsgithubrepos/ai-engineer-assignment-unsolved-main/actions/runs/18948401158/job/54106098553](https://github.com/kathirsgithubrepos/ai-engineer-assignment-unsolved-main/actions/runs/18948401158/job/54106098553)

#### 📎 Evidence

![Deployment ](submission_files/task5/Deployment.jpg)
![Docker Image ](submission_files/task5/Pacakaged.jpg)

## 🎯 Final Status

| Task                   | Status |
| ---------------------- | ------ |
| Optimization           | ✅      |
| API Improvements       | ✅      |
| Docker & Local Serving | ✅      |
| CI/PR Evaluation       | ✅      |
| Deployment             | ✅      |

Every task completed with proof and performance improvements.

