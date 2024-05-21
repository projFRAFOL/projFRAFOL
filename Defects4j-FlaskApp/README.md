# FRAFOL 

## Description
FRAFOL is an educational framework designed to introduce and teach the concepts and practices of mutation testing. It provides a comprehensive environment where learners can experiment with different mutation testing tools. The framework includes a curated collection of buggy projects provided by Defects4j, offering hands-on experience in identifying and resolving code defects.

## Installation
In order to use FRAFOL it is required to install Docker in your system. The following guidelines are instructions in the installation of Docker on both Windows and Linux machines.

### For Windows

1. Check System Requirements 

    - Windows 10 64-bit: Pro, Enterprise, or Education (Build 16299 or later).
    - Hyper-V and Containers Windows features must be enabled.

2. Download Docker Desktop 

    - Visit the Docker Desktop for Windows download page and download the installer.

3. Install Docker Desktop 

    - Run the Docker Desktop Installer executable.
    - Follow the installation wizard steps.
    - When prompted, ensure that the "Enable Hyper-V Windows Features" option is selected.

4. Start Docker Desktop 

    - Once installed, Docker Desktop will start automatically.
    - If not, you can start it from the Start menu.

5. Verify Installation 

    - Open a Command Prompt or PowerShell window.
    - Run the command:
    `docker --version`
    - You should see the Docker version installed.

### For Linux (Ubuntu as an example)

1. Update Package Information

`sudo apt-get update`

2. Install Prerequisites

```
  sudo apt-get install \
  ca-certificates \
  curl \
  gnupg \
  lsb-release
```

3. Add Docker’s Official GPG Key

```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

4. Set Up the Docker Repository

```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. Install Docker Engine

```
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

6. Start Docker

    - Start Docker service:
    `sudo systemctl start docker`
    
    - Enable Docker to start on boot:
    `sudo systemctl enable docker`

7. Verify Installation

    - Run the command:
    `docker --version`
    - You should see the Docker version installed.

## Usage
How to use the project once it’s installed.

## Contributing
Guidelines for contributing to the project.

## License
Information about the project's license.
