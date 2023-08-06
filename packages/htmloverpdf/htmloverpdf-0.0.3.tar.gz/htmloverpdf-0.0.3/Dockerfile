# Pip install some binary some source wheels over python base image.
FROM python:3
RUN apt-get -q -o=Dpkg::Use-Pty=0 update \
    && DEBIAN_FRONTEND=noninteractive DEBCONF_NOWARNINGS=yes \
       apt-get -q -o=Dpkg::Use-Pty=0 install --no-install-recommends --yes \
        libgirepository1.0-dev \
        gir1.2-poppler-0.18 \
    && rm -rf /var/lib/apt/lists \
    && adduser --disabled-password --gecos "" htmloverpdf
USER htmloverpdf
COPY --chown=htmloverpdf pyproject.toml setup.cfg /src/
COPY --chown=htmloverpdf htmloverpdf /src/htmloverpdf/
RUN SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0 python3 -m pip \
        --disable-pip-version-check \
        --no-python-version-warning \
        --use-feature=in-tree-build \
        --no-cache-dir \
        install \
            --user \
            --no-warn-script-location \
            /src/
CMD ["python3", "-m", "htmloverpdf"]
