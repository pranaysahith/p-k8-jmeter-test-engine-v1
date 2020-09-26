## Integration of p-k8-test-data with test framework (jmeter+icap)

### Run docker images
```
    docker build -t glasswallcrawler:1.0 gw_crawler

    docker build -t k8-file-distribution:1.0 file_distribution 

    docker build -t icap-jmeter:1.0 jmeter-c-icap

    docker-compose up

```

### Run jmeter script
```
    jmeter -n -t python-linux.jmx -JPATH=<PATH_TO_CLONED_REPO> -l ./test/test.jtl -j jmeter.log -e -o report/
```

### Prerequisites
1. After git clone use command: find . -type f -exec dos2unix {} \; 
2. Verify you have jmeter symbolic link set in your WSL: https://linuxize.com/post/how-to-create-symbolic-links-in-linux-using-the-ln-command/
3. Verify you have python installed and command can be used/linked as python (python --version)
4. Install test data requerments.txt, from file_distribution folder run: pip install -r requirements.txt
5. You specified the path to cloned repo, pointing to docker-icap-jmeter-testdata folder before running jmeter command













