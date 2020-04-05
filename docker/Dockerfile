FROM python:3.7-slim-buster AS production

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
  apt-get install -y nodejs

ADD web /web

RUN cd /web/frontend && \
    node --version && \
    npm --version && \
	npm install --save

FROM python:3.7-buster AS builder

# Become root
USER root

# Install some base packages for building certain pip modules
RUN apt-get update && \
	apt-get -y install cmake build-essential && \
	apt-get autoclean -y && apt-get autoremove -y && \
	rm -rf /var/lib/apt

# Create a venv to work in
RUN python3 -m venv /venv

# Install fred python requirements
ADD requirements.txt /requirements.txt
RUN /venv/bin/pip3 install -r /requirements.txt

# Copy the current repo into the container
ADD fred /fred
ADD bin /bin

ADD setup.py /setup.py
ADD MANIFEST.in /MANIFEST.in
ADD LICENCE /LICENCE


# Setup environment variables as an env var
ARG SOURCE_COMMIT='unkn'
ARG SOURCE_BRANCH='unkn'

ENV FRED_GIT_SHA=${SOURCE_COMMIT}
ENV FRED_GIT_BRANCH=${SOURCE_BRANCH}

# Build and install fred
RUN /venv/bin/python3 setup.py bdist_wheel
RUN /venv/bin/pip3 install /dist/*.whl

# Switch to the production image
FROM production

COPY --from=builder /venv /venv
COPY --from=builder /fred /fred
COPY --from=builder /bin /bin

RUN /venv/bin/jupyter contrib nbextension install --user && \
	/venv/bin/jupyter nbextension enable init_cell/main

# Setup environment variables as an env var
ARG SOURCE_COMMIT='unkn'
ARG SOURCE_BRANCH='unkn'

ENV FRED_GIT_SHA=${SOURCE_COMMIT}
ENV FRED_GIT_BRANCH=${SOURCE_BRANCH}

# Expose the port for the main HTTP server
EXPOSE 3000

# Expose the port for auxiliary flask based applications
EXPOSE 5000-5100

# Expose the port for the main notebook server
EXPOSE 8888

CMD []
