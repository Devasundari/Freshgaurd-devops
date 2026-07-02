@echo off

echo =======================================
echo Building Docker Image...
echo =======================================

set IMAGE_NAME=freshguard
set IMAGE_TAG=v2
set REGISTRY=freshguardacr12345.azurecr.io

docker build -t %IMAGE_NAME%:%IMAGE_TAG% .

if errorlevel 1 (
    echo Docker build failed.
    exit /b 1
)

docker tag %IMAGE_NAME%:%IMAGE_TAG% %REGISTRY%/%IMAGE_NAME%:%IMAGE_TAG%

if errorlevel 1 (
    echo Docker tag failed.
    exit /b 1
)

echo.
echo Pushing image to Azure Container Registry...
docker push %REGISTRY%/%IMAGE_NAME%:%IMAGE_TAG%

if errorlevel 1 (
    echo Docker push failed.
    exit /b 1
)

echo.
echo =======================================
echo Image pushed successfully!
echo Image: %REGISTRY%/%IMAGE_NAME%:%IMAGE_TAG%
echo =======================================

pause