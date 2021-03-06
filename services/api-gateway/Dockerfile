ARG PYTHON_VERSION="3.6.10"
FROM python:${PYTHON_VERSION}-slim as base
#
#  USAGE:
#     cd sercices/api-gateway
#     docker build -f Dockerfile -t api-gateway:prod --target production ../../
#     docker run api-gateway:prod
#
#  REQUIRED: context expected at ``osparc-simcore/`` folder because we need access to osparc-simcore/packages

LABEL maintainer=pcrespov

# simcore-user uid=8004(scu) gid=8004(scu) groups=8004(scu)
ENV SC_USER_ID=8004 \
    SC_USER_NAME=scu \
    SC_BUILD_TARGET=base \
    SC_BOOT_MODE=default

RUN adduser \
    --uid ${SC_USER_ID} \
    --disabled-password \
    --gecos "" \
    --shell /bin/sh \
    --home /home/${SC_USER_NAME} \
    ${SC_USER_NAME}


# Sets utf-8 encoding for Python et al
ENV LANG=C.UTF-8

# Turns off writing .pyc files; superfluous on an ephemeral container.
ENV PYTHONDONTWRITEBYTECODE=1 \
    VIRTUAL_ENV=/home/scu/.venv

# Ensures that the python and pip executables used in the image will be
# those from our virtualenv.
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

EXPOSE 8000
EXPOSE 3000

# -------------------------- Build stage -------------------
# Installs build/package management tools and third party dependencies
#
# + /build             WORKDIR
#
FROM base as build

ENV SC_BUILD_TARGET=build

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    build-essential \
    gcc

RUN python -m venv ${VIRTUAL_ENV}

RUN pip install --upgrade --no-cache-dir \
    pip~=20.0.2  \
    wheel \
    setuptools

WORKDIR /build

# install base 3rd party dependencies
# NOTE: copies to /build to avoid overwriting later which would invalidate this layer
COPY  --chown=scu:scu services/api-gateway/requirements/_base.txt .
RUN pip --no-cache-dir install -r _base.txt


# --------------------------Cache stage -------------------
# CI in master buils & pushes this target to speed-up image build
#
#  + /build
#    + services/api-gateway [scu:scu] WORKDIR
#
FROM build as cache

ENV SC_BUILD_TARGET cache

COPY --chown=scu:scu packages /build/packages
COPY --chown=scu:scu services/api-gateway /build/services/api-gateway

WORKDIR /build/services/api-gateway

RUN pip --no-cache-dir install -r requirements/prod.txt &&\
    pip --no-cache-dir list -v


# --------------------------Production stage -------------------
# Final cleanup up to reduce image size and startup setup
# Runs as scu (non-root user)
#
#  + /home/scu     $HOME = WORKDIR
#    + services/api-gateway [scu:scu]
#
FROM base as production

ENV SC_BUILD_TARGET=production \
    SC_BOOT_MODE=production

ENV PYTHONOPTIMIZE=TRUE

WORKDIR /home/scu

COPY --chown=scu:scu --from=cache  ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --chown=scu:scu services/api-gateway/docker services/api-gateway/docker


HEALTHCHECK --interval=30s \
    --timeout=20s \
    --start-period=30s \
    --retries=3 \
    CMD ["python3", "services/api-gateway/docker/healthcheck.py", "http://localhost:8000/"]

ENTRYPOINT [ "/bin/sh", "services/api-gateway/docker/entrypoint.sh" ]
CMD ["/bin/sh", "services/api-gateway/docker/boot.sh"]


# --------------------------Development stage -------------------
# Source code accessible in host but runs in container
# Runs as myu with same gid/uid as host
# Placed at the end to speed-up the build if images targeting production
#
#  + /devel         WORKDIR
#    + services  (mounted volume)
#
FROM build as development

ENV SC_BUILD_TARGET=development

WORKDIR /devel

ENTRYPOINT ["/bin/sh", "services/api-gateway/docker/entrypoint.sh"]
CMD ["/bin/sh", "services/api-gateway/docker/boot.sh"]
