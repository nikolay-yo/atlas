conan profile detect
conan install .
cmake -S . -B build
cmake --build build --config Release
