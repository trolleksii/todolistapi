#!/bin/sh

docker build -t trolleksii/python-base .
docker build -t trolleksii/cci-builder -f Dockerfile-builder .
# docker login -u $DOCKER_USER -p $DOCKER_PASSWORD
docker push trolleksii/python-base
docker push trolleksii/cci-builder
# docker logout