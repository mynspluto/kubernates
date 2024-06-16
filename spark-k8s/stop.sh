#!/bin/bash

# Delete all resources defined in YAML files

# List of YAML files
yaml_files=("spark-master-svc.yml" "spark-worker-svc.yml" "spark-master-deployment.yml" "spark-master-svc.yml")

for file in "${yaml_files[@]}"
do
    echo "Deleting resources from $file ..."
    kubectl delete -f "$file"
done
