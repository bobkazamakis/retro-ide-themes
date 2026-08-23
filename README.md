# Retro IDE themes

Eighteen classic and enhanced editor themes for Sublime Text, Xcode, JetBrains
IDEs, and Zed.

## Themes

- Visual Studio 2012 Light
- Visual Studio Enhanced Light
- Visual Studio Enhanced (Globals vs. Members) Light
- Visual Studio 2012 Dark
- Visual C++ 6
- Visual Basic 6
- Borland Delphi VB6++
- Xcode Classic
- IntelliJ IDEA Default
- Eclipse Classic
- CodeWarrior
- Delphi Classic
- Borland C++ Builder
- Turbo Pascal
- Turbo C++ 3.0
- Emacs 21
- Vim Light
- Notepad++ Default

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
