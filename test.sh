ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no -i "alexgre1.pem" ubuntu@ec2-34-201-172-56.compute-1.amazonaws.com /bin/bash << 'EOT'
sudo docker stop $(docker ps -q --filter ancestor=$REPO/$IMAGE:latest)
$(aws ecr get-login --no-include-email --region us-east-1)
sudo docker pull alexgre/aapp
sudo docker run -d --rm -p 80:80 alexgre/aapp
EOT