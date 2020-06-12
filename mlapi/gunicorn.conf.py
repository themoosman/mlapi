import multiprocessing

#Only listen locally
#bind = "127.0.0.1:5000"
#Listen on all IPs
bind = "0.0.0.0:5000"

#Number of workers.  Each worker loads its own copy of the model.
#In my testing I set this to the # of Monitors 
#workers = multiprocessing.cpu_count() * 2 + 1
workers = 7

#Threads
#Warning.  Setting threads >1 could cause issues.
#Multiple threads will try to access the same model concurently.
threads = 1



