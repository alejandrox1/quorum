#!/bin/bash

export PS4='$(tput setaf 1)$(tput setab 7) + $(tput sgr 0)'                     
clear                                                                           
set -x  

sudo rm -f test*                                                                
sudo rm -f mydatabase.db                                                        
sudo docker-compose down --remove-orphans --volumes                             
sudo docker-compose up --build -d
