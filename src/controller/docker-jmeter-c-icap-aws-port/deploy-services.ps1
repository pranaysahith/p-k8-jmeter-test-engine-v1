kubectl apply -f minio.yaml
kubectl apply -f influxdb.yaml
Start-Sleep -Seconds 5
Start-Process -FilePath "kubectl" -ArgumentList "port-forward --address 0.0.0.0 service/output-queue 9000:9000"
Start-Process -FilePath "kubectl" -ArgumentList "port-forward --address 0.0.0.0 service/influxdb 8086"
