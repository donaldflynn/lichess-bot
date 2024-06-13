setlocal ENABLEDELAYEDEXPANSION


REM Change into the parent directory of this folder
cd %~dp0..\
REM Get the current working directory, which is now the parent directory of this folder
set FOLDER=%cd%

REM change into the directory containing this script
cd %~dp0

REM mounts code in the docker container, and starts
docker run --rm -it --entrypoint /bin/bash --gpus=all donaldflynn/chess-bot:cuda