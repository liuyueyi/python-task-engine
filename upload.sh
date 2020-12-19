cd ../
tar -zcvf python-task-engine.tar.gz --exclude=python-task-engine/venv  --exclude=python-task-engine/.idea --exclude=python-task-engine/logs --exclude=python-task-engine/.git --exclude=python-task-engine/data python-task-engine

scp python-task-engine.tar.gz xx@xxx:/home/xx/workspace
