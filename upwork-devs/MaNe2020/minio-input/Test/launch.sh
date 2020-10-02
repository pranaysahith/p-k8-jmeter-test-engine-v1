#!/bin/bash
# Inspired from https://github.com/hhcordero/docker-jmeter-client
# Basically runs jmeter, assuming the PATH is set to point to JMeter bin-dir (see Dockerfile)
#
# This script expects the standdard JMeter command parameters.
#
set -e
freeMem=`awk '/MemFree/ { print int($2/1024) }' /proc/meminfo`
s=$(($freeMem/10*8))
x=$(($freeMem/10*8))
n=$(($freeMem/10*2))
export JVM_ARGS="-Xmn${n}m -Xms${s}m -Xmx${x}m"

T_DIR=/usr/share/Test
R_DIR=${T_DIR}/report
L_DIR=${T_DIR}/log
rm -rf ${R_DIR} > /dev/null 2>&1
mkdir -p ${R_DIR}

#echo "START Running Jmeter on `date`"
echo "JVM_ARGS=${JVM_ARGS}"

/usr/local/apache-jmeter-5.3/bin/jmeter -n -t ${T_DIR}/minio.jmx -l ${R_DIR}/minio.jtl -j ${L_DIR}/jmeter.log -e -o ${R_DIR}
echo "END Running Jmeter on `date`"
