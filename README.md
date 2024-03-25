# verify-markdown-archive
A command-line interface to verify ACDC-based Markdown Archives using KERIpy

I've only run this on macOS. You probably need to install `libsodium` for this to work:

```sh
brew install libsodium
```

## Example:

After sodium is installed, make dependencies and you should be able to run the script.
For an example archive, check out [tbd]().

```sh
make deps
./verify.py <path-to-acdc-markdown-archive>
```
