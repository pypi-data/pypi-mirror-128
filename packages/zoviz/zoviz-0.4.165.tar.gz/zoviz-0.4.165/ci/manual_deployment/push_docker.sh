#!/bin/sh

{ \
    sudo docker login registry.gitlab.com && \
    sudo docker push registry.gitlab.com/jlogan03/daq; \
} || { echo 1; }

# Make sure to remove credentials
sudo docker logout

