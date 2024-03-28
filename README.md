# verify-markdown-archive
A command-line interface to verify ACDC-based Markdown Archives using KERIpy

First, the compacted ACDC and associated events are ingested into KERIpy to ensure they are valid.

Next, the expanded ACDC is compacted and compared to the signed version.

Finally, all files in the `assets` directory and all top level `.md` files are verified by digest
comparison with the expanded ACDC attributes section.

I've only run this on macOS. You probably need to install `libsodium` for this to work:

```sh
brew install libsodium
```

## Example:

After sodium is installed, make dependencies and you should be able to run the script.
For an example archive, check out [tbd]().

```sh
make verify archive=<path-to-acdc-markdown-archive>
```

and you should receive the output:

```
No further output indicates success!
```
