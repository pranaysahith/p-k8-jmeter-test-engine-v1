kubectl delete -n default deployment processor
kubectl delete -n default deployment output-queue
kubectl delete -n default service output-queue
<#
kubectl delete -n default service influxdb
#>
taskkill /IM "kubectl.exe" /F