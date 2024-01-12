# cirque
* learning project with multiple goals:
    * creating embedded projects using pigweed (https://pigweed.dev/) to:
        * bootstrap our build environment based on the bazel build system (https://bazel.build/)
            * makes it reproduceable in the future or on new build machines
            * cross platform capability
        * simplifies the integration of static analysis tools
        * simplifies the integration of tools for presubmit checks
        * integration unit testing modules for embedded devices (similar to gtest)
        * C++ based
    * a study of modern control theory
        * state space design methods
        * Kalman filters
        * balance a ball on a table

# how we set up the pigweed environment
* prerequisites:
    * python virtual environments: > sudo apt install python3.10-venv
* created a third_party directory
    * added pigweed
        * > git submodule add https://pigweed.googlesource.com/pigweed/pigweed
    * pigweed uses gn to generate it's own virtual environment
    * copy bootstrap.sh into project top directory from pigweeds environment
        * boostrap.sh
            * modify the downstream project root info
    * create a symbolic link to bootstrap.sh called activate.sh
* create a tools directory
    * create a pigweed directory
    * add banner.txt
    * add env_setup.json
        * configure the environment to your liking
        * point bootstrap.sh to this file as a config file for the pw_bootstrap command
* create a build_override directory
    * add a pigweed.gni file to specify the location of pigweed