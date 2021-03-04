# A Minimal GN configuration

The [GN] build tool is used by Chromium and Fuchsia in conjunction
with the [Ninja] build tool to build software.

GN is not particularly designed to be easy to use for small projects,
and it is not designed to be a "batteries included" system: you have
to provide all of the rules and toolchain definitions yourself. GN
is intended to be used for projects that are big enough that you'll
probably want to do that anyway.

That said, it's still useful to see what a minimal GN configuration
needs to be.

The smallest GN configuration needs three files:
    * a dotfile, which tells GN where the buildconfig file is. Conventionally,
      the dotfile lives in the source root, known as "//", i.e., "//.gn".
    * a buildconfig file, to tell GN what toolchain to use by default.
    * a BUILD.gn file

You can put the toolchain definition in the same file as the targets you
want to build (as this project does), but good style (and maintenance in
practice) would usually tell you to use a separate file instead.

This (almost) minimal project will build two executables, one written in C and
one written in C++.

GN generates a set of Ninja files to run the build (hence the name,
Generate Ninja). You cannot generate the files into the source root, but any
other directory should be fine. By convention, GN uses "//out" or a
subdirectory of "//out".

Running `gn gen out` produces:

    * `out/args.gn`: the GN args, if any, used to generate the file.
    * `out/build.ninja` the top-level Ninja file.
    * `out/build.ninja.d`: the dependencies of the top-level Ninja file; if
        any of these files change, Ninja will re-run GN to regenerate
        (update) the build files before trying to build anything.
    * `out/toolchain.ninja`: the rule definitions for the default toolchain.
    * `out/obj/hello_cpp.ninja`: the rules to build `//:hello_c`.
    * `out/obj/hello_cpp.ninja`: the rules to build `//:hello_cpp`.

Running `ninja -C out -j 1 -v` produces:

```
ninja: Entering directory `out'
[1/4] clang++ -MMD -MF obj/hello_cpp.o.d -o obj/hello_cpp.o -c ../hello_cpp.cpp
[2/4] clang -MMD -MF obj/hello_c.o.d -o obj/hello_c.o -c ../hello_c.c
[3/4] clang obj/hello_c.o  -o hello_c
[4/4] clang obj/hello_cpp.o -lc++ -o hello_cpp
```

and that's all there is to it!

[GN] https://gn.googlesource.com/gn
[Ninja] https://ninja-build.org/

