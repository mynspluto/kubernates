#!/bin/bash
PORTS=("9870" "9867" "9864")

for PORT in "${PORTS[@]}"; do
  echo "Checking for processes on port $PORT..."
  
  # 해당 포트를 사용하는 모든 PID를 찾음
  PIDS=$(lsof -t -i :$PORT)
  
  if [ -n "$PIDS" ]; then
    echo "Processes using port $PORT: $PIDS"
    
    # 각 PID를 종료
    for PID in $PIDS; do
      echo "Terminating process $PID on port $PORT..."
      kill -9 "$PID"
      
      if [ $? -eq 0 ]; then
        echo "Successfully terminated process $PID."
      else
        echo "Failed to terminate process $PID."
      fi
    done
  else
    echo "No process is using port $PORT."
  fi
done

kubectl delete all --all -n hadoop
kubectl delete pvc --all -n hadoop
kubectl delete pv --all -n hadoop
#docker system prune -a