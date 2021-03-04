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

* The [dotfile](.gn). Conventionally, the dotfile lives in the source root, 
  known as "//", i.e., "//.gn". The dotfile can set up some project
  specific settings for GN, but most importantly tells GN where to
  file the buildconfig file.
* The [buildconfig file](buildconfig.gn), which tell GN what toolchain 
  to use by default. It can also set up other global variables.
* A [BUILD.gn](BUILD.gn) file containing the actual targets to build 
  and the toolchain definitions to use to build them.

Good style (and maintenance in practice) would usually separate out the
toolchain definitions into its own file, but this project keeps them all
together for simplicity.

This (almost) minimal project will build two executables, one written in C and
one written in C++.

GN generates a set of Ninja files to run the build (hence the name,
Generate Ninja). You cannot generate the files into the source root, but any
other directory should be fine. By convention, GN uses `//out` or a
subdirectory of `//out`, but you can also build into a directory outside of
the source root just fine.

Ninja generates multiple files:

* A top-level `build.ninja` file, which includes all the others.
* A `build.ninja.d` file containing the dependencies of the build.ninja file itself;
  changing any of these dependencies will cause Ninja to re-run GN to regenerate
  (update) the build files and then reload them before going on to build things.
* A `toolchain.ninja` file for the rules the default toolchain will use.
* A file for each additional GN target

For example:

```
$ gn gen out
Done. Made 2 targets from 2 files in 3ms
$ find out -type f | sort
out/args.gn
out/build.ninja
out/build.ninja.d
out/obj/hello_c.ninja
out/obj/hello_cpp.ninja
out/toolchain.ninja
$ ninja -C out -j 1 -v
Running `gn gen out` produces:
ninja: Entering directory `out'
[1/4] clang++ -MMD -MF obj/hello_cpp.o.d -o obj/hello_cpp.o -c ../hello_cpp.cpp
[2/4] clang -MMD -MF obj/hello_c.o.d -o obj/hello_c.o -c ../hello_c.c
[3/4] clang obj/hello_c.o  -o hello_c
[4/4] clang obj/hello_cpp.o -lc++ -o hello_cpp
$ out/hello
Hello, world!
$ out/hello_cpp
Hello, world!
$
```

That's all there is to it!

[GN]: https://gn.googlesource.com/gn
[Ninja]: https://ninja-build.org/
