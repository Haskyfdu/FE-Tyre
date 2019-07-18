### Realtime Scheduling 

##### Anaconda dependencies 
```
# application dependencies
python == 3.7.3  
flask == 1.0.2  
requests == 2.21.0  
gunicorn==19.9.0

# algorithm dependencies
cython==0.29.7
numpy==1.16.3
scipy==1.2.1
pymysql==0.9.3
```

##### Service Running
```
# debug start:
$(conda env path)/gunicorn -c $(project path)/gunicorn.ini project_main:app  

# supervisor start:
sudo supervisord -c /etc/supervisord.conf

# supervisor shutdown:
sudo supervisorctl shutdown

# supervisor dashboard url:
0.0.0.0:9999

# jenkins distribution:
sudo supervisorctl stop Planned-Scheduling
cd /home/appuser/deployment
cp Planned-Scheduling/logs/running.log Logs/$(date +%Y%m%d%H%M%S)-planned-scheduling-running.log
rm -rf Planned-Scheduling
git clone -b spruce-2.0-uat http://gitlab.saicstack.com/Optimization/Project/Planned-Scheduling.git
sudo supervisorctl start Planned-Scheduling
```
