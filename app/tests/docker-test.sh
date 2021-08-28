# Script for testing the flask service on a remote machine

git_dir=proyecto-ati-2021

addr="$1"

ssh_s(){
  ssh $addr "cd $git_dir && $@";
}

ssh $addr git clone https://github.com/diegosanchezp/proyecto-ati-2021.git

ssh_s cp .env.example .env && \
ssh_s 'echo SECRET_KEY=\"testing secret key\" >> .env' && \
ssh_s 'chmod +x build.sh && ./build.sh'
ssh_s 'docker-compose logs flask'

if [ "$?" -ne "0" ]; then
    echo "Test Failed"
    return 1

