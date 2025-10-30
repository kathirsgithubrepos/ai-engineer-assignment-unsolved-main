#!/usr/bin/env bash
set -euo pipefail

echo "=== Windows Manual Evaluation Script ==="

##############################################################################
# Activate venv
##############################################################################
echo ">>> Activating virtual env"
source .venv/Scripts/activate

echo "Python in use:"
which python
python -V

##############################################################################
# Task 1 — Run solution.py
##############################################################################
echo
echo ">>> Running Task 1: solution.py performance test"
time python scripts/solution.py \
  --employees_path data/employees.csv \
  --connections_path data/connections.csv \
  --output_path submission.csv

read -rp "Press ENTER to continue..."

##############################################################################
# Task 2 — Serve locally & benchmark
##############################################################################
echo
echo ">>> Running Task 2: Serve API & test curl request"

python serving/serve.py &
SERVER_PID=$!

echo "Waiting 60 seconds for app to load model..."
sleep 60

time ./tests/send_request.sh

kill $SERVER_PID
sleep 2
echo "Server stopped."

read -rp "Press ENTER to continue..."

##############################################################################
# Task 3 — Docker build + test
##############################################################################
echo
echo ">>> Running Task 3: Docker Build + Serve test"

docker build -t reporting-line-prediction-service-image .

docker stop reporting-line-prediction-service 2>/dev/null || true
docker rm reporting-line-prediction-service 2>/dev/null || true

docker run -d -p 5001:5001 --name reporting-line-prediction-service reporting-line-prediction-service-image

sleep 10

./tests/send_request.sh

docker stop reporting-line-prediction-service
docker rm reporting-line-prediction-service

read -rp "Press ENTER to continue..."

##############################################################################
# Task 4 — PR Simulation
##############################################################################
echo
echo ">>> Running Task 4: PR Simulation"

MAIN_BRANCH="main"
REMOTE="origin"

git checkout "$MAIN_BRANCH"

# cleanup
git branch -D location_match_tweak 2>/dev/null || true
git branch -D embedding_similarity_tweak 2>/dev/null || true
git push "$REMOTE" --delete location_match_tweak 2>/dev/null || true
git push "$REMOTE" --delete embedding_similarity_tweak 2>/dev/null || true

# BAD PR
git checkout -b location_match_tweak
sed -i 's/WEIGHT_LOCATION_MATCH = 0.0/WEIGHT_LOCATION_MATCH = 1.0/' scripts/solution.py
git commit -am "Regression: increase location weight"
git push -f "$REMOTE" location_match_tweak
gh pr create --base "$MAIN_BRANCH" --head location_match_tweak --title "Regression Test" --body "Expect lower accuracy"

# GOOD PR
git checkout "$MAIN_BRANCH"
sed -i 's/WEIGHT_LOCATION_MATCH = 1.0/WEIGHT_LOCATION_MATCH = 0.0/' scripts/solution.py

git checkout -b embedding_similarity_tweak
sed -i 's/WEIGHT_EMBEDDING_SIMILARITY = 1.0/WEIGHT_EMBEDDING_SIMILARITY = 2.0/' scripts/solution.py
sed -i 's/WEIGHT_COMMON_NEIGHBORS = 1.0/WEIGHT_COMMON_NEIGHBORS = 2.0/' scripts/solution.py

git commit -am "Boost embedding + neighbor weights"
git push -f "$REMOTE" embedding_similarity_tweak
gh pr create --base "$MAIN_BRANCH" --head embedding_similarity_tweak --title "Improvement Test" --body "Expect higher accuracy"

echo
echo ">>> Go to GitHub, inspect PR comments, merge improvement PR."
read -rp "Press ENTER once merged to continue..."

git checkout main

##############################################################################
# Task 5 — CD Check
##############################################################################
echo
echo ">>> Task 5: Verify CD Workflow"
echo ">>> Open GitHub Actions → ensure serve workflow executed successfully"
read -rp "Press ENTER to finish..."

echo "✅ All tasks completed successfully"
