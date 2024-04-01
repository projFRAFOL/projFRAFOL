FROM node:14

# Install OpenJDK (Java Development Kit)
RUN apt-get update && apt-get install -y openjdk-11-jdk

# Set environment variable for JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

WORKDIR /usr/src/app
COPY package*.json app.js ./

# Install Node.js dependencies
RUN npm install
RUN npm install cors

# Expose the port your app runs on
EXPOSE 3000

# Run the Node.js server
CMD ["node", "app.js"]