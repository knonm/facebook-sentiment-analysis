#!/bin/bash
export NEO4J_HOME="/opt/neo4j-community-3.0.6"
export PY_VIR_HOME="/home/mcanon/virtualenv/PSG-EACH-SI"

. ${PY_VIR_HOME}/bin/activate

pip install -r ./requirements.txt
