# ICAP+JMeter Dockerfile
## Clone Repo from Git

1. Open a Terminal Window
2. Navigate to where you'd like to store the repo
3. Clone it

## Execute Script

1. In repo folder, go to docker-jmeter-c-icap subfolder
2. Build docker image: ```docker build -t c-icap-jmeter:1.0 . ```
3. Run docker image: ```docker run -v "$(pwd):/usr/share" -p 1344:1344 jmeter-c-icap:1.0```

$(pwd) is your current working directory, in case you are using Windows, specify windows path (C:\Users\...), do not use WSL file path structure.
-v "$(pwd):/usr/share" command will share docker run output in the specified working directory.

Docker run will execute icap.jmx that is started via launch.sh.

## JMeter script

1. Runs testscript.sh using OS Process Sampler
2. Saves output to txt file
3. Needs to be refined further this is just basic implemetation. 



