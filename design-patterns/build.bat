@echo on
setlocal

:: Set the default build type to Release if none is provided
set BUILD_TYPE=Release

:: Check if a build type argument was provided (Release or Debug)
if "%1"=="" (
    echo No build type specified. Defaulting to Release.
) else (
    set BUILD_TYPE=%1
    echo Using build type: %BUILD_TYPE%
)

:: Create a build directory if it doesn't exist
if not exist build mkdir build

cd build
cmake .. -G "Visual Studio 17 2022" -DCMAKE_BUILD_TYPE=%BUILD_TYPE%
cmake --build . --config %BUILD_TYPE%