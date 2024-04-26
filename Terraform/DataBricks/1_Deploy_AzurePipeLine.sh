#!/bin/bash

# Install Databricks CLI
#pip install --upgrade databricks-cli

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

(echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> /home/vsts/.bashrc

eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

sudo apt-get install build-essential

brew install gcc

brew tap databricks/tap
brew install databricks


# Configure Databricks CLI
#databricks configure --token

# Copy your PySpark script to DBFS
#databricks fs cp --overwrite /Users/hbhadra/PycharmProjects/cardiovascular_disease_prediction/src/Test_PYSPARK.py dbfs:/cdp/src/dbfs/app.py

# Create the job and get the job ID
JOB_ID=$(databricks jobs create --json cdp-app-create-job.json | jq -r '.job_id') 

echo $JOB_ID

# Generate JSON with the variable value
cat <<EOF > cdp-app-run-job.json
{
  "job_id": $JOB_ID,
    "creator_user_name": "himanshu.bhadra@bayareala8s.com",
    "run_as_user_name": "himanshu.bhadra@bayareala8s.com",
    "run_as_owner": true,
    "settings": {
      "name": "CDP new Job",
      "email_notifications": {
        "no_alert_for_skipped_runs": false
      },
      "webhook_notifications": {},
      "timeout_seconds": 0,
      "max_concurrent_runs": 1,
      "tasks": [
        {
          "task_key": "CDP-TASK",
          "run_if": "ALL_SUCCESS",
          "spark_python_task": {
            "python_file": "dbfs:/cdp/src/dbfs/app.py"
          },
          "existing_cluster_id": "0425-120439-eric4jrf",
          "timeout_seconds": 0,
          "email_notifications": {}
        }
      ],
      "format": "MULTI_TASK"
    },
    "created_time": 1714060038057
}
EOF

# Run the job immediately
databricks jobs run-now --json cdp-app-run-job.json
