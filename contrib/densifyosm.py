import fileformat_pb2 
import osmformat_pb2 
from struct import unpack
from zlib import decompress 
import sys


# Prototype Python program to create "splits" of osm for Hadoop processing 
# License: Apache 2.0, Copyright Travis L Pinney


# Keep track of file index 
index = 0

bh = fileformat_pb2.BlobHeader()
b = fileformat_pb2.Blob()
pg = osmformat_pb2.PrimitiveBlock()

f = open("district-of-columbia-latest.osm.pbf","rb")

# read the first 4 bytes to get size of the BlobHeader
bh_len = unpack("!i", f.read(4))[0]
index += 4

# read the BlobHeader 
bh.ParseFromString(f.read(bh_len))
index += bh_len 

print >> sys.stderr, bh

# Read the Blob 
b.ParseFromString(f.read(bh.datasize))
index += bh.datasize


print >> sys.stderr, b

# Assuming first "Blob" is a OSMHeader
if bh.type == "OSMHeader":
  hb = osmformat_pb2.HeaderBlock()
  hb.ParseFromString(decompress(b.zlib_data))
  print >> sys.stderr, hb 


# just care where the OSMData is for each blob, to create the splits for hadoop
# this creates a tab delimited output of start of OSMData and length of OSMData
while 1: 
  data = f.read(4)
  if data == "":
    break
  bh_len = unpack("!i", data)[0]
  index += bh_len
  bh.ParseFromString(f.read(bh_len))
  #print bh
  b.ParseFromString(f.read(bh.datasize))
  #print b.zlib_data
  pg.ParseFromString(decompress(b.zlib_data))
  #print pg

  #print "%s\t%s" % (index, bh.datasize)
  index += bh.datasize

    
  # iterate over sequence of primitive groups
   
  #print pg.lat_offset
  #print pg.lon_offset
  #print pg.granularity
  #print pg.date_granularity
 
  for p in pg.primitivegroup:

    if p.nodes:
      # process nodes 
      print >> sys.stderr, "TODO implement processing normal nodes"
      sys.exit()
    elif p.ways:
      print >> sys.stderr, "TODO implement processing ways"
    elif p.relations:
      print >> sys.stderr, "TODO implement processing relations"
    elif p.dense:
      nodes = []
      try:
        idx = p.dense.id[0]
      except:
        print >> sys.stderr, repr(p.dense)
        print >> sys.stderr, repr(p.nodes)
        print >> sys.stderr, repr(p.ways)
        sys.exit()
      nodes.append(idx)
      # extract the nodes  
      for nid in p.dense.id[1:]:
        nodes.append(idx + nid)
        idx += nid 
      
      # extract lats
      lats = []
      idx = p.dense.lat[0]
      lats.append(idx)
      for lat in p.dense.lat[1:]:
        lats.append(idx + lat)
        idx += lat
      # apply offsets and granularity to all the values
      lats = map(lambda x: .000000001 * ( pg.lat_offset + ( pg.granularity * x )), lats)

      # extracts lons 
      lons = []
      idx = p.dense.lon[0]
      lons.append(idx)
      for lon in p.dense.lon[1:]:
        lons.append(idx + lon)
        idx += lon
      # apply offsets and granularity to all the values
      lons = map(lambda x: .000000001 * ( pg.lon_offset + ( pg.granularity * x )), lons)
      

      # extract versions
      versions = []
      for ver in p.dense.denseinfo.version:
        versions.append(ver)
        
      # extract timestamps 
      timestamps = []
      idx = p.dense.denseinfo.timestamp[0]
      timestamps.append(idx)
      for ts in p.dense.denseinfo.timestamp[1:]:
        timestamps.append(idx + ts)
        idx += ts 
      # apply time offset
      timestamps = map(lambda x: pg.date_granularity * x, timestamps)
      
      # extract uids
      uids = []
      idx = p.dense.denseinfo.uid[0]
      uids.append(idx)
      for uid in p.dense.denseinfo.uid[1:]:
        uids.append(idx + uid)
        idx += uid 
      
     # extract user_sids
      user_sids = []
      idx = p.dense.denseinfo.user_sid[0]
      user_sids.append(idx)
      for usid in p.dense.denseinfo.user_sid[1:]:
        user_sids.append(idx + usid)
        idx += usid 
      # apply the strings to the list
      user_sids = map(lambda x : pg.stringtable.s[x], user_sids)
        
      # extract changesets 
      changesets = []
      idx = p.dense.denseinfo.changeset[0]
      changesets.append(idx)
      for cs in p.dense.denseinfo.changeset[1:]:
        changesets.append(idx + cs)
        idx += cs 
        
      # process the keys_vals      
      # convert to python list 
      keys_vals = list(p.dense.keys_vals)
      

      kvs = []
      s = []
      for kv in keys_vals:
        if kv == 0:
          #kv.append(None)
          # process the keyvalues on the stack 
          kvs.append(zip(s[::2], s[1::2]))
          s = []
        else:
          s.append(pg.stringtable.s[kv])
        
  
      # print out nodes in tsv and use pipe to colon to delimit keyvals, and 
      # pipe to delimit multiple key vals

      kl = []
      for i in range(len(nodes)):
        ks = ""
        if not kvs[i] == []:
          #print >> sys.stderr, kvs[i]
          for k,v in kvs[i]:
            kl.append("%s:%s" % (k, v))
          ks = "|".join(kl)
          #print >> sys.stderr, ks
        
        print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (nodes[i],versions[i],timestamps[i],uids[i],user_sids[i], changesets[i],lats[i],lons[i], ks)





