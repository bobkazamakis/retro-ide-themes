#!/usr/bin/env python3
"""Write the same eighteen retro schemes as Xcode themes (.xccolortheme).

The palettes come from build_schemes.py. That file stays the one source of the
colors, therefore a Sublime Text scheme and its Xcode theme cannot disagree.

Xcode has a smaller model than the 101 TextMate rules: 33 syntax keys. This
script maps each Xcode key onto one role of the shared palette. The key names
and the file format come from the themes that Xcode ships; see
~/Library/Developer/Xcode/UserData/FontAndColorThemes for examples.
"""

import os
import plistlib

from build_schemes import SCHEMES, check_all

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xcode")

SIZE = 14.0

# SF Mono only. Keywords and attributes use Semibold; all other syntax keeps
# the Regular weight. The schemes that slant comments in Sublime Text keep the
# slant here, because a slant is not a weight. Therefore "bold italic" in a
# scheme becomes the regular italic face.
REGULAR = "SFMono-Regular - %.1f" % SIZE
ITALIC = "SFMono-RegularItalic - %.1f" % SIZE
SEMIBOLD = "SFMono-Semibold - %.1f" % SIZE

FONT = {
    None: REGULAR,
    "bold": REGULAR,
    "italic": ITALIC,
    "bold italic": ITALIC,
}

# These syntax categories need stronger emphasis in every Xcode theme.
SEMIBOLD_KEYS = {
    "xcode.syntax.attribute",
    "xcode.syntax.keyword",
}

# Keep every font in the Xcode themes at one consistent size.
HEAD_1 = REGULAR
HEAD_2 = REGULAR
HEAD_3 = REGULAR

# Xcode syntax key -> (color role, style role or None).
# A ".system" key is for a symbol of the SDK. A key without it is for a symbol
# of your own project.
#
# Keywords and attributes use the same semibold face in every theme, regardless
# of the style used by the source editor being reproduced.
SYNTAX = [
    ("xcode.syntax.plain",                     "g_fg",        None),
    ("xcode.syntax.comment",                   "comment",     "comment"),
    ("xcode.syntax.comment.doc",               "doc",         "doc"),
    ("xcode.syntax.comment.doc.keyword",       "doc_key",     "doc_key"),
    ("xcode.syntax.mark",                      "codetag",     "codetag"),
    ("xcode.syntax.markup.aside.kind",         "doc_key",     "doc_key"),
    ("xcode.syntax.string",                    "string",      None),
    ("xcode.syntax.character",                 "char",        None),
    ("xcode.syntax.number",                    "number",      None),
    ("xcode.syntax.keyword",                   "keyword",     None),
    ("xcode.syntax.preprocessor",              "preproc",     "preproc"),
    ("xcode.syntax.attribute",                 "attribute",   "attribute"),
    ("xcode.syntax.declaration.type",          "type",        "type"),
    ("xcode.syntax.declaration.other",         "func_decl",   "func_decl"),
    ("xcode.syntax.identifier.type",           "type",        "type"),
    ("xcode.syntax.identifier.type.system",    "type_lib",    "type"),
    ("xcode.syntax.identifier.class",          "type",        "type"),
    ("xcode.syntax.identifier.class.system",   "type_lib",    "type"),
    ("xcode.syntax.identifier.constant",       "const_other", None),
    ("xcode.syntax.identifier.constant.system", "const_lang", None),
    ("xcode.syntax.identifier.function",       "func_call",   "func_call"),
    ("xcode.syntax.identifier.function.system", "func_builtin", "func_call"),
    ("xcode.syntax.identifier.macro",          "macro",       "preproc"),
    ("xcode.syntax.identifier.macro.system",   "macro",       "preproc"),
    ("xcode.syntax.identifier.variable",       "var_project", None),
    ("xcode.syntax.identifier.variable.system", "const_other", None),
    ("xcode.syntax.markup.code",               "raw",         None),
    ("xcode.syntax.url",                       "link",        None),
    ("xcode.syntax.regex",                     "regexp",      None),
    ("xcode.syntax.regex.capturename",         "arg_label",   None),
    ("xcode.syntax.regex.charname",            "escape",      None),
    ("xcode.syntax.regex.number",              "number",      None),
    ("xcode.syntax.regex.other",               "regexp_op",   None),
]

# Top-level key -> color role.
SURFACES = [
    ("DVTSourceTextBackground",                  "g_bg"),
    ("DVTSourceTextSelectionColor",              "g_sel"),
    ("DVTSourceTextInsertionPointColor",         "g_caret"),
    ("DVTSourceTextInvisiblesColor",             "g_invisibles"),
    ("DVTSourceTextCurrentLineHighlightColor",   "g_line_hl"),
    ("DVTSourceTextBlockDimBackgroundColor",     "preproc_inactive"),
    ("DVTDebuggerInstructionPointerColor",       "g_highlight"),
    ("DVTConsoleTextBackgroundColor",            "g_bg"),
    ("DVTConsoleTextSelectionColor",             "g_sel"),
    ("DVTConsoleTextInsertionPointColor",        "g_caret"),
    ("DVTConsoleDebuggerInputTextColor",         "g_fg"),
    ("DVTConsoleDebuggerOutputTextColor",        "g_fg"),
    ("DVTConsoleDebuggerPromptTextColor",        "reg_green"),
    ("DVTConsoleExectuableInputTextColor",       "g_fg"),
    ("DVTConsoleExectuableOutputTextColor",      "g_fg"),
    ("DVTMarkupTextBackgroundColor",             "raw_bg"),
    ("DVTMarkupTextBorderColor",                 "g_guide"),
    ("DVTMarkupTextNormalColor",                 "g_fg"),
    ("DVTMarkupTextPrimaryHeadingColor",         "head"),
    ("DVTMarkupTextSecondaryHeadingColor",       "head"),
    ("DVTMarkupTextOtherHeadingColor",           "head"),
    ("DVTMarkupTextStrongColor",                 "bold"),
    ("DVTMarkupTextEmphasisColor",               "italic"),
    ("DVTMarkupTextLinkColor",                   "link"),
    ("DVTMarkupTextInlineCodeColor",             "raw"),
    ("DVTScrollbarMarkerErrorColor",             "reg_red"),
    ("DVTScrollbarMarkerWarningColor",           "reg_yellow"),
    ("DVTScrollbarMarkerAnalyzerColor",          "reg_purple"),
    ("DVTScrollbarMarkerBreakpointColor",        "reg_blue"),
    ("DVTScrollbarMarkerDiffColor",              "reg_orange"),
    ("DVTScrollbarMarkerDiffConflictColor",      "reg_red"),
    ("DVTScrollbarMarkerRuntimeIssueColor",      "reg_purple"),
]

# The fonts of the markup view. Xcode uses the system font (.SFNS) for the
# prose here. These themes use SF Mono for every font, therefore the headings
# and the body text are monospaced too. The headings keep their display sizes.
MARKUP_FONTS = {
    "DVTMarkupTextNormalFont": REGULAR,
    "DVTMarkupTextStrongFont": REGULAR,
    "DVTMarkupTextEmphasisFont": ITALIC,
    "DVTMarkupTextLinkFont": REGULAR,
    "DVTMarkupTextCodeFont": REGULAR,
    "DVTMarkupTextPrimaryHeadingFont": HEAD_1,
    "DVTMarkupTextSecondaryHeadingFont": HEAD_2,
    "DVTMarkupTextOtherHeadingFont": HEAD_3,
}

CONSOLE_FONTS = [
    "DVTConsoleDebuggerInputTextFont", "DVTConsoleDebuggerOutputTextFont",
    "DVTConsoleDebuggerPromptTextFont", "DVTConsoleExectuableInputTextFont",
    "DVTConsoleExectuableOutputTextFont",
]


def rgba(hex_color):
    """#RRGGBB or #RRGGBBAA -> the "R G B A" string that Xcode expects."""
    h = hex_color.lstrip("#")
    if len(h) not in (6, 8):
        raise SystemExit("cannot read the color %r" % hex_color)
    parts = [int(h[i:i + 2], 16) / 255.0 for i in range(0, len(h), 2)]
    if len(parts) == 3:
        parts.append(1.0)
    return " ".join("%g" % round(p, 6) for p in parts)


def check_mapping(scheme):
    """Every role that this script names must be in the palette, with a color."""
    colors, styles = scheme["colors"], scheme["styles"]
    for key, role, style in SYNTAX:
        if role not in colors or colors[role] is None:
            raise SystemExit("%s: no color for role %r (Xcode key %r)"
                             % (scheme["name"], role, key))
        if style is not None and style not in styles:
            raise SystemExit("%s: no style for role %r (Xcode key %r)"
                             % (scheme["name"], style, key))
    for key, role in SURFACES:
        if role not in colors or colors[role] is None:
            raise SystemExit("%s: no color for role %r (Xcode key %r)"
                             % (scheme["name"], role, key))


# Turbo Pascal and Turbo C++ 3.0 have no free readable EGA color for variables.
# Visual Studio 2012 Light historically left project variables as plain text;
# the Win32 Polyglot remix deliberately does the same for its local-variable
# layer.
FLAT_VARIABLES = {
    "Turbo Pascal",
    "Turbo C++ 3.0",
    "Visual Studio 2012 Light",
    "Borland Delphi VB6++",
}


def report_variables():
    """Say which schemes give the project variables a color of their own.

    Xcode has one key for the variables of your project. If it holds the same
    color as the plain text, the variables cannot be told apart. This report
    makes that visible instead of quiet.
    """
    for scheme in SCHEMES:
        colors = scheme["colors"]
        same = colors["var_project"].upper() == colors["g_fg"].upper()
        if same and scheme["name"] not in FLAT_VARIABLES:
            raise SystemExit(
                "%s: var_project %s is the same as the plain text. Give the "
                "project variables their own color, or add the scheme to "
                "FLAT_VARIABLES." % (scheme["name"], colors["var_project"]))
        print("  %-26s project variables %s %s"
              % (scheme["name"], colors["var_project"],
                 "(same as plain text by design)" if same else ""))


def build(scheme):
    colors, styles = scheme["colors"], scheme["styles"]
    theme = {
        "DVTFontAndColorVersion": 1,
        "DVTFontSizeModifier": 1,
        "DVTLineSpacing": 1.1,
    }
    for key, role in SURFACES:
        theme[key] = rgba(colors[role])
    theme.update(MARKUP_FONTS)
    for key in CONSOLE_FONTS:
        theme[key] = FONT[None]

    syntax_colors, syntax_fonts = {}, {}
    for key, role, style in SYNTAX:
        syntax_colors[key] = rgba(colors[role])
        face = FONT[styles[style] if style else None]
        if key in SEMIBOLD_KEYS:
            face = SEMIBOLD
        syntax_fonts[key] = face
    theme["DVTSourceTextSyntaxColors"] = syntax_colors
    theme["DVTSourceTextSyntaxFonts"] = syntax_fonts
    return theme


def check_faces(theme, name):
    """Only the configured SF Mono faces at the common size may pass."""
    allowed = {REGULAR, ITALIC, SEMIBOLD}
    faces = set(theme["DVTSourceTextSyntaxFonts"].values())
    faces |= {v for k, v in theme.items()
              if k.endswith("Font") and isinstance(v, str)}
    for face in sorted(faces):
        if face not in allowed:
            raise SystemExit("%s: the face %r is not allowed. Allowed: %s"
                             % (name, face, ", ".join(sorted(allowed))))
    syntax_fonts = theme["DVTSourceTextSyntaxFonts"]
    for key in SEMIBOLD_KEYS:
        if syntax_fonts[key] != SEMIBOLD:
            raise SystemExit("%s: %s must use %s"
                             % (name, key, SEMIBOLD))


def main():
    # The shared checks first: no point writing Xcode themes from a rule set
    # that does not hold together.
    check_all()
    report_variables()
    os.makedirs(OUT, exist_ok=True)
    for scheme in SCHEMES:
        check_mapping(scheme)
        path = os.path.join(OUT, scheme["name"] + ".xccolortheme")
        theme = build(scheme)
        check_faces(theme, scheme["name"])
        with open(path, "wb") as fh:
            plistlib.dump(theme, fh, sort_keys=True)
        print("wrote %s (%d syntax keys)" % (path, len(SYNTAX)))


if __name__ == "__main__":
    main()
