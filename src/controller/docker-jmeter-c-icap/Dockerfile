FROM openjdk:8-jre

# Install c-icap
RUN apt-get update && \
    apt-get -y install c-icap

RUN apt install -y python3
RUN apt install -y python3-pip

# Set variables
ARG JMETER_VERSION="5.3"
ENV JMETER_HOME /usr/local/apache-jmeter-${JMETER_VERSION}
ENV JMETER_BIN ${JMETER_HOME}/bin

# Install Apache JMeter
RUN wget http://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz && \
    tar zxvf apache-jmeter-${JMETER_VERSION}.tgz && \
    rm -f apache-jmeter-${JMETER_VERSION}.tgz && \
    mv apache-jmeter-${JMETER_VERSION} ${JMETER_HOME}

EXPOSE 1344

ENV PATH $PATH:${JMETER_BIN}
COPY ./Test /usr/share/Test/
COPY ./icap.jmx /etc/conf/jmeter-conf.jmx

RUN chmod -R +x /usr/share/Test
#ENTRYPOINT ["/usr/share/Test/launch.sh"]

COPY requirement.txt .

RUN pip3 install -r requirement.txt --user

COPY processor.py .

COPY logging.conf .

CMD ["python3", "processor.py"]