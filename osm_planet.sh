#!/bin/bash

cd /mnt/staging 
curl -O http://planet.osm.org/pbf/planet-130620.osm.pbf
hadoop fs -mkdir /staging 
hadoop fs -copyFromLocal planet-130620.osm.pbf /staging/planet-130620.osm.pbf

