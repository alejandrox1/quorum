FROM alejandrox1/ubuntu_miniconda
MAINTAINER Jorge Alarcon Ochoa


RUN apt-get update -y && apt-get install -y software-properties-common  
RUN add-apt-repository -y ppa:webupd8team/java && apt-get update -y && \
    echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
    echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections && \
    apt-get install -y oracle-java8-installer 
RUN curl http://apache.spinellicreations.com/kafka/0.10.2.0/kafka_2.11-0.10.2.0.tgz | tar xz
RUN mv kafka_2.11-0.10.2.0 /kafka/

