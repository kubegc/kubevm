FROM openjdk:8u201-jdk-alpine3.9

RUN mkdir -p /home/kubevirt-controller-manager
RUN mkdir -p /etc/kubernetes

ADD kubevirt-controller-1.7.0.jar /home/kubevirt-controller-manager
ADD admin.conf /etc/kubernetes/

WORKDIR /home/kubevirt-controller-manager

#RUN java -jar kubevirt-controller-1.3.0-jar-with-dependencies.jar
