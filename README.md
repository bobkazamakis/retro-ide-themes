# Retro IDE themes

Twenty-one classic, enhanced, and modern editor themes for Sublime Text, Xcode,
JetBrains IDEs, and Zed.

## Themes

- R.C. - Visual Studio 2012 Light
- R.C. - Visual Studio Enhanced Light
- R.C. - Visual Studio Enhanced (Globals vs. Members) Light
- R.C. - Visual Studio 2012 Dark
- R.C. - Visual Studio Enhanced Dark
- R.C. - Visual C++ 6
- R.C. - Visual Basic 6
- R.C. - Borland Delphi VB6++
- R.C. - Xcode Classic
- R.C. - Xcode Default (Light)
- R.C. - IntelliJ IDEA Default
- R.C. - IntelliJ Light (Islands)
- R.C. - Eclipse Classic
- R.C. - CodeWarrior
- R.C. - Delphi Classic
- R.C. - Borland C++ Builder
- R.C. - Turbo Pascal
- R.C. - Turbo C++ 3.0
- R.C. - Emacs 21
- R.C. - Vim Light
- R.C. - Notepad++ Default

## Install

### Sublime Text

Copy the files from `sublime/` into the `User` package folder, then select a
theme from **Preferences > Color Scheme**.

On macOS with Sublime Text 4:

```sh
cp sublime/*.sublime-color-scheme \
  ~/Library/Application\ Support/Sublime\ Text/Packages/User/
```

### Xcode

```sh
mkdir -p ~/Library/Developer/Xcode/UserData/FontAndColorThemes
cp xcode/*.xccolortheme ~/Library/Developer/Xcode/UserData/FontAndColorThemes/
```

Restart Xcode and select a theme in **Settings > Themes**.

### JetBrains IDEs

The bundled plugin targets JetBrains IDEs 2025.3 and newer.

1. Open **Settings > Plugins**.
2. From the gear menu, choose **Install Plugin from Disk**.
3. Select `jetbrains/Retro IDE Islands Themes.zip` and restart the IDE.

To install only an editor scheme, import an `.icls` file from
`jetbrains/schemes/` in **Settings > Editor > Color Scheme**.

### Zed

```sh
mkdir -p ~/.config/zed/themes
cp zed/themes/*.json ~/.config/zed/themes/
```

Reload Zed and open the theme selector.

## Build

The generated themes share the palettes and syntax roles defined in
`build_schemes.py`.

```sh
python3 build_schemes.py
python3 build_xcode_themes.py
python3 build_jetbrains_themes.py
python3 build_zed_themes.py
```

The `Preview.swift`, `Preview.py`, `Preview.c`, and `Preview.java` files cover
common syntax elements for checking the generated themes.
