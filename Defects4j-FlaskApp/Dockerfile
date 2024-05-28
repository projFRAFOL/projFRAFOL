FROM ubuntu:22.04

#############################################################################
# Requirements
#############################################################################

# Timezone
ENV TZ=Europe/Lisbon
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN \
  apt-get update -y && \
  apt-get install software-properties-common -y && \
  apt-get update -y && \
  apt-get install -y openjdk-8-jdk \
                git-all \
                build-essential \
                subversion \
                perl \
                python3-pip \
                curl \
                unzip \
                cpanminus \
                make \
                && \
  rm -rf /var/lib/apt/lists/*

# Java version
ARG TARGETARCH

# Set JAVA_HOME based on the architecture and write it to /etc/environment
RUN if [ "$TARGETARCH" = "arm64" ]; then \
        echo "Running on ARM architecture" && \
        echo "JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64" >> /etc/environment; \
    else \
        echo "Running on AMD architecture" && \
        echo "JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> /etc/environment; \
    fi

# Use the dot command to source /etc/environment to set the environment variables
RUN set -a && . /etc/environment && set +a

# Ensure JAVA_HOME is correctly set by the previous steps
RUN echo "JAVA_HOME: $JAVA_HOME"

#############################################################################
# Setup Defects4J
#############################################################################

# ----------- Step 1. Clone defects4j from github --------------
WORKDIR /
RUN git clone https://github.com/PedroTav/defects4j.git defects4j

# ----------- Step 2. Initialize Defects4J ---------------------
WORKDIR /defects4j
RUN cpanm --installdeps .
RUN ./init.sh
RUN pip install pandas==2.1.1

# ----------- Step 3. Add Defects4J's executables to PATH: ------
ENV PATH="/defects4j/framework/bin:${PATH}"  
#--------------

#############################################################################
# Setup Defects4JGUI
#############################################################################

WORKDIR /app
COPY . /app
RUN pip install -U Flask
RUN pip install flask-cors
EXPOSE 8000

CMD python3 ./defects4jUI.py