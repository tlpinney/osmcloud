# Prototype Python Hadoop "split" maker 

## Requirements 

Protobuf compilter 
protobuf python package 


## Usage 

    protoc --python_out=. fileformat.proto
    protoc --python_out=. osmformat.proto 

    wget http://download.geofabrik.de/north-america/us/district-of-columbia-latest.osm.pbf

    python splitosm.py > splits.tsv
    


