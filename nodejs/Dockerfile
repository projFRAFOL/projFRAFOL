FROM amazoncorretto:8 AS jdk8

FROM node:14

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
  apt-get install -y git-all \
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

# Copy JDK 8 from the Corretto stage
COPY --from=jdk8 /usr/lib/jvm/java-1.8.0-amazon-corretto /usr/lib/jvm/java-1.8.0-amazon-corretto

# Define JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-amazon-corretto

# Update PATH environment variable
ENV PATH $JAVA_HOME/bin:$PATH

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

# ----------- Step 3. Add Defects4J's executables to PATH: ------
ENV PATH="/defects4j/framework/bin:${PATH}"  
#--------------

WORKDIR /usr/src/app
COPY package*.json app.js ./

# Install Node.js dependencies
RUN npm install
RUN npm install cors

# Expose the port your app runs on
EXPOSE 3000

# Run the Node.js server
CMD ["node", "app.js"]