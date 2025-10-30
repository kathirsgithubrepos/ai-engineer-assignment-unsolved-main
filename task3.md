# ✅ Task 3 — Docker Containerization & Verification

## Objective

Containerize the application using a **multi-stage Docker build**, keeping the image lean and ensuring the app runs correctly when launched via Docker.

---

## 🔧 Key Implementation Highlights

| Requirement                         | Solution                                      |
| ----------------------------------- | --------------------------------------------- |
| Use multi-stage Dockerfile          | ✅ Two-stage build (`builder` + `runtime`)     |
| Avoid copying `.venv`               | ✅ `.dockerignore` updated                     |
| CPU only (no CUDA)                  | ✅ Lightweight CPU PyTorch installed           |
| Entrypoint = serve.py               | ✅ `ENTRYPOINT ["python", "serving/serve.py"]` |
| Expose correct port                 | ✅ `EXPOSE 5001`                               |
| Local test using evaluator commands | ✅ Successful run + response                   |

---

## 🧪 Local Verification Process

Commands used (aligned with evaluator script):

```bash
docker build -t reporting-line-prediction-service-image .
docker run -d -p 5001:5001 --name reporting-line-prediction-service reporting-line-prediction-service-image
sleep 10
./tests/send_request.sh
docker stop reporting-line-prediction-service
docker rm reporting-line-prediction-service
```

✅ Container built successfully
✅ Service started and responded
✅ Visualization returned via `/predict`
✅ Test request executed successfully

---

## Evidence

#### Container Running

![Container Running](evidences/task3/container%20running.jpg)

#### Local Test Execution Success

![Test Executed Locally](evidences/task3/test%20executed%20locally%20.jpg)

---

### Final Result

| Status                              | Description                    |
| ----------------------------------- | ------------------------------ |
| ✅ Multi-stage Docker build complete | Smaller & consistent image     |
| ✅ Application runs via Docker       | Ports & entrypoint verified    |
| ✅ Test request succeeds             | `curl_response.html` generated |
| ✅ Meets Task-3 evaluation criteria  | Ready for CI pipeline          |

---

### Conclusion

The application is successfully containerized using a multi-stage Docker build.
It runs correctly when launched inside Docker and responds to the test requests as expected.
