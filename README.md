# OSMCloud 

## Requirements 

### Java 

http://www.oracle.com/technetwork/java/javasebusiness/downloads/java-archive-downloads-javase6-419409.html#jdk-6u45-oth-JPR

Place jdk-6u45-linux-x64.bin in the media directory  

### rvm 

### knife-solo and knife-ec2

    # rvm install 2.0.0 
    rvm gemset create castcloud
    rvm use 2.0.0@castcloud
    gem install knife-solo 
    gem install knife-ec2 

# Amazon EC2 keypair

Create a keypair on Amazon called cloud and move to ~/.ssh 
    
### Set up knife 

Place in ~/.chef/knife.rb and update keys. 
aws_ssh_key_id is the keypair you created excluding the .pem extension 

    knife[:aws_access_key_id] = "FIXME"
    knife[:aws_secret_access_key] = "FIXME"
    knife[:aws_ssh_key_id] = "FIXME"
    knife[:chef_mode] = "solo"
 

### Set up knife plugin 

Based on https://raw.github.com/emiddleton/knife-ec2/master/lib/chef/knife/ec2_server_create.rb 
and https://raw.github.com/gist/2049991/170e0fd2a5b9c5b8532a385d990d04400b182fb4/ec2_server_create.rb 


From the castcloud base directory 
    mkdir -p ~/.chef/plugins/knife
    cp ./chef/plugins/ec2_server_create.rb ~/.chef/plugins/knife/ec2_server_create.rb
    

## Knife commands 


List out the servers you have available 

    knife ec2 server list 
    
Create an on demand server 

    knife ec2 server create --image=ami-d0f89fb9 --ssh-user=ubuntu --ssh-key=cloud --identity-file=~/.ssh/cloud.pem 


Create a spot-priced server 
Check the current rates, the rate may be too low. You will need to check the aws console if it gets stuck.

    knife ec2 server create --image=ami-d0f89fb9 --flavor=m2.2xlarge --price=0.15 --ssh-user=ubuntu --ssh-key=cloud --identity-file=~/.ssh/cloud.pem


Delete a server 
   
    knife ec2 server delete i-xxxxxxx

SSH into the machine 

    ssh -i ~/.ssh/cloud.pem ubuntu@ec2-x-x-x-x.compute-1.amazonaws.com

Install components 
    
    export CAST_HOST=ec2-x-x-x-x.compute-1.amazonaws.com
    ./cast init 
    ./cast ssh # you will now be connected to the host machine 
    sudo sh ./seed.sh 





