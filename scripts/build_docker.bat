echo.
echo Building and pushing image
echo.

REM Switch current working directory to parent directory of this folder
cd %~dp0..\


docker buildx build --push --platform "linux/arm64/v8" -t "donaldflynn/pi-chess-bot:latest" .
