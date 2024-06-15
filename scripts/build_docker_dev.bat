echo.
echo Building and pushing image
echo.

REM Switch to directory with pi docker file
cd %~dp0..\docker\dev


docker buildx build --load -t "donaldflynn/chess-bot:dev" -f Dockerfile ../..
