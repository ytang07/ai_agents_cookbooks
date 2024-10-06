ARG VARIANT="noble"
FROM buildpack-deps:${VARIANT}-curl

# LABEL dev.containers.features="common"

ARG VARIANT
RUN if [ "$VARIANT" = "noble" ]; then \
        if id "ubuntu" &>/dev/null; then \
            echo "Deleting user 'ubuntu'  for $VARIANT" && userdel -f -r ubuntu || echo "Failed to delete ubuntu user for $VARIANT"; \  
        else \
            echo "User 'ubuntu' does not exist for $VARIANT"; \ 
        fi; \
    fi

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends git