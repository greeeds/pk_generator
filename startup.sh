#!/bin/bash
CURRENT_DIR=$(cd $(dirname $0); pwd)

docker-compose -f $CURRENT_DIR/docker-compose.yml run -it --rm pk_generator
