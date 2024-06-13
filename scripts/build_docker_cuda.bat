echo.
echo Building and pushing image
echo.

REM Switch to directory with cuda docker file
cd %~dp0..\docker\cuda


docker buildx build --push -t "donaldflynn/chess-bot:cuda" -f Dockerfile ../..

REM Switch to directory back
cd %~dp0\..