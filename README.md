# A Minimal GN configuration

The [GN] build tool is used by the Chromium and Fuchsia projects (and others)
in conjunction with the [Ninja] build tool to build software.

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

This (almost) minimal project will build two executables, one written in C
and one written in C++.

GN generates a set of Ninja files to run the build (hence the name,
Generate Ninja). You cannot generate the files into the source root, but any
other directory should be fine. By convention, GN uses `//out` or a
subdirectory of `//out`, but you can also build into a directory outside of
the source root just fine. Running `gn gen` will create an `arg.gn` file
in the output directory if one doesn't already exist. You can use that
file to set arguments that alter how your build works.

The generated GN files include:

* A top-level `build.ninja` file, which includes all the others.
* A `build.ninja.d` file containing the dependencies of the build.ninja file
  itself; changing any of these dependencies will cause Ninja to re-run GN
  to regenerate (update) the build files and then reload them before going
  on to build things.
* A `toolchain.ninja` file for the rules the default toolchain will use
  and any `action` targets that will run in that toolchain.
* A `.ninja` file for each BUILD.gn file that contains targets that are
  compiled as part of that BUILD.gn.

Example:

```
$ gn gen out
Done. Made 2 targets from 2 files in 3ms
$ find out -type f | sort
out/.ninja_log
out/args.gn
out/build.ninja
out/build.ninja.d
out/obj/hello.ninja
out/toolchain.ninja
$ ninja -C out -j 1 -v
ninja: Entering directory `out'
[0/1] $PATH_TO_GN/gn --root=./.. -q --regeneration gen .
[1/5] python3 ../generate_world.py ./gen world.cc world.h
[2/5] touch obj/world.stamp
[3/5] clang++ -MMD -MF obj/hello.o.d -Igen -o obj/hello.o -c ../hello.cc
[4/5] clang++ -MMD -MF obj/world.o.d -Igen -o obj/world.o -c gen/world.cc
[5/5] clang++ obj/hello.o obj/world.o -lc++ -o hello
$ out/hello
Hello, world.
$
```

That's all there is to it!

[GN]: https://gn.googlesource.com/gn
[Ninja]: https://ninja-build.org/
