load("@rules_cc//cc:defs.bzl", "cc_binary")
load("//:platform_transition.bzl", "device_cc_binary")

package(default_visibility = ["//visibility:public"])

device_cc_binary(
    name = "app.elf",
    binary = "//src:device_application",
)

# This target is currently not funcitoning and is set as a placeholder.
cc_binary(
    name = "host_build",
    deps = ["//src:main"],
)
