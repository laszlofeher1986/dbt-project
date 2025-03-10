# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.11"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

import subprocess

# Function to run dbt
def run_dbt():
    # Define the dbt command as a list
    command = ["dbt", "run"]

    # Execute the dbt run command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the command executed successfully
    if result.returncode == 0:
        print("dbt run completed successfully")
    else:
        print(f"dbt run failed with error: {result.stderr}")

# Execute the dbt run
run_dbt()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
