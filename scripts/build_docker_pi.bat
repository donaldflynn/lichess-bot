echo.
echo Building and pushing image
echo.

REM Switch to directory with pi docker file
cd %~dp0..\docker\pi


docker buildx build --push --platform "linux/arm64/v8" -t "donaldflynn/chess-bot:pi" -f Dockerfile ../..

REM Switch to directory back
cd %~dp0\..