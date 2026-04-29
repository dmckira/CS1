FROM jenkins/jenkins:2.555.1-lts

# Cambiamos a root para poder instalar paquetes del sistema
USER root

# Instalamos Python3, pip y dependencias necesarias para sonar-scanner
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Permite instalar paquetes pip en un entorno Debian externally-managed
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# Instalamos sonar-scanner CLI
RUN curl -sSLo /tmp/sonar-scanner.zip \
    https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-6.2.1.4610-linux-x64.zip \
    && unzip /tmp/sonar-scanner.zip -d /opt \
    && mv /opt/sonar-scanner-6.2.1.4610-linux-x64 /opt/sonar-scanner \
    && ln -s /opt/sonar-scanner/bin/sonar-scanner /usr/local/bin/sonar-scanner \
    && rm /tmp/sonar-scanner.zip

# Volvemos al usuario jenkins por seguridad
USER jenkins

# EXPOSE: documenta los puertos que Jenkins usará.
# Puerto 8080: interfaz web de Jenkins.
# Puerto 50000: comunicación con agentes Jenkins (workers).
EXPOSE 8080
EXPOSE 50000

# Las variables de entorno como JENKINS_USERNAME y JENKINS_PASSWORD
# NO van aquí en el Dockerfile porque contienen credenciales.
# Se pasan con -e al ejecutar el contenedor (más seguro y flexible).
