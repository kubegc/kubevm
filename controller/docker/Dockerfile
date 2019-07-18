FROM openjdk:8u201-jdk-alpine3.9

RUN mkdir -p /home/kubevirt-controller-manager
RUN mkdir -p /etc/kubernetes

ADD kubevirt-controller-2.1.0-jar-with-dependencies.jar /home/kubevirt-controller-manager
ADD admin.conf /etc/kubernetes/

WORKDIR /home/kubevirt-controller-manager

RUN java -jar kubevirt-controller-2.1.0-jar-with-dependencies.jar
