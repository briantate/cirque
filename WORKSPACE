workspace(
    name = "demo_uart",
)

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "platforms",
    sha256 = "5308fc1d8865406a49427ba24a9ab53087f17f5266a7aabbfc28823f3916e1ca",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/platforms/releases/download/0.0.6/platforms-0.0.6.tar.gz",
        "https://github.com/bazelbuild/platforms/releases/download/0.0.6/platforms-0.0.6.tar.gz",
    ],
)

http_archive(
    name = "cmsis",
    build_file_content = """
cc_library(
  name = "core",
  includes = [ "CMSIS/Core/Include", ],
  hdrs = [
    "CMSIS/Core/Include/cmsis_version.h",
    "CMSIS/Core/Include/cmsis_compiler.h",
    "CMSIS/Core/Include/cmsis_gcc.h",
    "CMSIS/Core/Include/mpu_armv7.h",
    "CMSIS/Core/Include/core_cm4.h", ],
  visibility = ["//visibility:public"]
)
    """,
    strip_prefix = "CMSIS_5-develop",
    url = "https://github.com/ARM-software/CMSIS_5/archive/refs/heads/develop.zip",
)

http_archive(
    name = "atsame54_device_pack",
    build_file_content = """
cc_library(
  name = "same54n20a_deps",
  deps = [ "@cmsis//:core", ],
  includes = [ "include", ],
  hdrs = glob(["include/*.h"]) +
         glob(["include/component/*.h"]) +
         glob(["include/instance/*.h"]) +
         glob(["include/pio/*.h"]),
  srcs = [ "gcc/gcc/startup_same54n20a.c" ],
  visibility = ["//visibility:public"],
  alwayslink = 1,
)

exports_files(["gcc/gcc/same54n20a_flash.ld"])
    """,
    sha256 = "3e116f672edfa97d779d8fc7f2085961ca81105c85b989d1559ad2db02290c95",
    type = "zip",
    url = "https://packs.download.microchip.com/Microchip.SAME54_DFP.3.8.234.atpack",
)

local_repository(
    name = "pigweed",
    path = "third_party/pigweed",
)

http_archive(
    name = "bazel_skylib",  # 2022-09-01
    sha256 = "4756ab3ec46d94d99e5ed685d2d24aece484015e45af303eb3a11cab3cdc2e71",
    strip_prefix = "bazel-skylib-1.3.0",
    urls = ["https://github.com/bazelbuild/bazel-skylib/archive/refs/tags/1.3.0.zip"],
)

http_archive(
    name = "rules_python",
    sha256 = "0a8003b044294d7840ac7d9d73eef05d6ceb682d7516781a4ec62eeb34702578",
    strip_prefix = "rules_python-0.24.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.24.0/rules_python-0.24.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

local_repository(
    name = "pw_toolchain",
    path = "third_party/pigweed/pw_toolchain_bazel",
)


load(
    "@pigweed//pw_env_setup/bazel/cipd_setup:cipd_rules.bzl",
    "cipd_client_repository",
    "cipd_repository",
    "pigweed_deps",
)

pigweed_deps()

load("@cipd_deps//:cipd_init.bzl", "cipd_init")

cipd_init()

cipd_client_repository()

load("@pw_toolchain//features/macos:generate_xcode_repository.bzl", "pw_xcode_command_line_tools_repository")

pw_xcode_command_line_tools_repository()

# Get the OpenOCD binary (we'll use it for flashing).
cipd_repository(
    name = "openocd",
    path = "infra/3pp/tools/openocd/${os}-${arch}",
    tag = "version:2@0.11.0-3",
)

# Fetch llvm toolchain.
cipd_repository(
    name = "llvm_toolchain",
    path = "fuchsia/third_party/clang/${os}-${arch}",
    tag = "git_revision:8475d0a2b853f6184948b428ec679edf84ed2688",
)

# Fetch linux sysroot for host builds.
cipd_repository(
    name = "linux_sysroot",
    path = "fuchsia/third_party/sysroot/linux",
    tag = "git_revision:d342388843734b6c5c50fb7e18cd3a76476b93aa",
)

# Fetch gcc-arm-none-eabi toolchain.
cipd_repository(
    name = "gcc_arm_none_eabi_toolchain",
    path = "fuchsia/third_party/armgcc/${os}-${arch}",
    tag = "version:2@12.2.mpacbti-rel1.1",
)

register_toolchains(
    "@pigweed//pw_toolchain/host_clang:host_cc_toolchain_linux",
    "@pigweed//pw_toolchain/arm_gcc:arm_gcc_cc_toolchain_cortex-m4",
)

load("@rules_python//python:repositories.bzl", "python_register_toolchains")

# Set up the Python interpreter and PyPI dependencies we'll need.
python_register_toolchains(
    name = "python3_10",
    python_version = "3.10",
)

load("@python3_10//:defs.bzl", "interpreter")
load("@rules_python//python:pip.bzl", "pip_parse")

pip_parse(
    name = "pypi",
    python_interpreter_target = interpreter,
    requirements_lock = "//:requirements_lock.txt",
)

load("@pypi//:requirements.bzl", "install_deps")

install_deps()
