kubectl delete -n default deployment processor
kubectl delete -n default deployment output-queue
kubectl delete -n default service output-queue
taskkill /IM "kubectl.exe" /F