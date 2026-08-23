#!/usr/bin/env python3
"""Generate eighteen full Zed UI and syntax themes.

The palettes come from build_schemes.py. Each generated file is a standalone
Zed theme family with one theme, suitable for ~/.config/zed/themes. The UI
surface hierarchy adapts iccir's macOS-inspired Timeless Theme for Zed.
"""

from dataclasses import dataclass
import json
from pathlib import Path
import re

from build_schemes import SCHEMES, check_all


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "zed" / "themes"
SCHEMA = "https://zed.dev/schema/themes/v0.2.0.json"
AUTHOR = "Retro IDE Themes"

DARK_SCHEMES = {
    "Turbo Pascal",
    "Turbo C++ 3.0",
    "Visual Studio 2012 Dark",
}

TURBO_SCHEMES = {
    "Turbo Pascal",
    "Turbo C++ 3.0",
}

HEX_COLOR = re.compile(r"#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?$")


@dataclass(frozen=True)
class SyntaxSpec:
    capture: str
    color: str
    style: str | None = None
    background: str | None = None


# Zed's documented Tree-sitter captures, plus captures used by its current
# built-in One themes (namespace, markup punctuation, and diff lines).
SYNTAX_SPECS = [
    SyntaxSpec("attribute", "attribute", "attribute"),
    SyntaxSpec("boolean", "const_lang", "const_lang"),
    SyntaxSpec("comment", "comment", "comment"),
    SyntaxSpec("comment.doc", "doc", "doc"),
    SyntaxSpec("constant", "const_other"),
    SyntaxSpec("constant.builtin", "const_lang", "const_lang"),
    # Zed's constructor capture is the called constructor symbol, not the
    # constructor declaration keyword. It therefore follows function calls.
    SyntaxSpec("constructor", "func_member_call", "func_call"),
    SyntaxSpec("embedded", "interp_fg", background="interp_bg"),
    SyntaxSpec("emphasis", "italic", "italic"),
    SyntaxSpec("emphasis.strong", "bold", "bold"),
    SyntaxSpec("enum", "type", "type"),
    SyntaxSpec("function", "func_global_call", "func_call"),
    SyntaxSpec("hint", "preproc_inactive", "italic"),
    SyntaxSpec("keyword", "keyword", "keyword"),
    SyntaxSpec("label", "label"),
    SyntaxSpec("link_text", "link"),
    SyntaxSpec("link_uri", "link"),
    SyntaxSpec("namespace", "module"),
    SyntaxSpec("number", "number"),
    SyntaxSpec("operator", "operator"),
    SyntaxSpec("predictive", "preproc_inactive", "italic"),
    SyntaxSpec("preproc", "preproc", "preproc"),
    # Available to grammars and semantic-token adapters that expose macros as
    # their own capture. C/C++ grammars that use only @preproc still inherit it.
    SyntaxSpec("macro", "macro", "preproc"),
    SyntaxSpec("primary", "g_fg"),
    SyntaxSpec("property", "member"),
    SyntaxSpec("punctuation", "punct"),
    SyntaxSpec("punctuation.bracket", "brace"),
    SyntaxSpec("punctuation.delimiter", "punct"),
    SyntaxSpec("punctuation.list_marker", "list_punct"),
    SyntaxSpec("punctuation.markup", "interp_punct"),
    SyntaxSpec("punctuation.special", "interp_punct"),
    SyntaxSpec("selector", "type", "type"),
    SyntaxSpec("selector.pseudo", "attribute", "attribute"),
    SyntaxSpec("string", "string"),
    SyntaxSpec("string.escape", "escape"),
    SyntaxSpec("string.regex", "regexp"),
    SyntaxSpec("string.special", "char"),
    SyntaxSpec("string.special.symbol", "const_other"),
    SyntaxSpec("tag", "tag", "tag"),
    SyntaxSpec("tag.doctype", "preproc", "preproc"),
    SyntaxSpec("text.literal", "raw"),
    SyntaxSpec("title", "head", "head"),
    # Semantic highlighting may report even primitive C/C++ types as `type`.
    # type_fallback preserves the normal type color except in palettes such as
    # Visual C++ 6 where an uncolored `int` is worse than the broad fallback.
    SyntaxSpec("type", "type_fallback", "type"),
    # Primitive types such as C int and char are language storage types. Using
    # type_lib here made them black in the Visual C++ 6 palette.
    SyntaxSpec("type.builtin", "storage_type", "keyword"),
    SyntaxSpec("variable", "var_local"),
    SyntaxSpec("variable.parameter", "param", "param"),
    SyntaxSpec("variable.special", "self", "self"),
    SyntaxSpec("variant", "enum_member"),
    SyntaxSpec("diff.plus", "diff_add_fg"),
    SyntaxSpec("diff.minus", "diff_del_fg"),
]


def slug(name):
    value = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not value:
        raise SystemExit("cannot make a file name from %r" % name)
    return value


def rgb(color):
    if not isinstance(color, str) or not HEX_COLOR.fullmatch(color):
        raise SystemExit("invalid color %r" % color)
    value = color[1:7]
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def hex_rgb(channels):
    return "#%02X%02X%02X" % tuple(round(channel) for channel in channels)


def zed_color(color):
    if not isinstance(color, str) or not HEX_COLOR.fullmatch(color):
        raise SystemExit("invalid color %r" % color)
    value = color.upper()
    return value if len(value) == 9 else value + "FF"


def alpha(color, value):
    if not re.fullmatch(r"[0-9A-Fa-f]{2}", value):
        raise SystemExit("invalid alpha %r" % value)
    return hex_rgb(rgb(color)) + value.upper()


def mix(first, second, amount):
    if not 0 <= amount <= 1:
        raise SystemExit("invalid mix amount %r" % amount)
    a = rgb(first)
    b = rgb(second)
    return hex_rgb(tuple(x + (y - x) * amount for x, y in zip(a, b)))


def luminance(color):
    channels = []
    for value in rgb(color):
        value /= 255.0
        channels.append(value / 12.92 if value <= 0.04045
                        else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(first, second):
    a, b = sorted((luminance(first), luminance(second)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def syntax_style(scheme, spec):
    colors = scheme["colors"]
    result = {"color": zed_color(colors[spec.color])}
    if spec.background:
        result["background_color"] = zed_color(colors[spec.background])

    style = scheme["styles"].get(spec.style) if spec.style else None
    if style:
        if "italic" in style:
            result["font_style"] = "italic"
        if "bold" in style:
            result["font_weight"] = 700
    return result


def status_colors(style, prefix, foreground, background, border):
    style[prefix] = zed_color(foreground)
    style[prefix + ".background"] = zed_color(background)
    style[prefix + ".border"] = zed_color(border)


def timeless_ui_palette(scheme):
    """Return the flat-color equivalent of Timeless's macOS UI hierarchy."""
    name = scheme["name"]
    colors = scheme["colors"]
    if name not in DARK_SCHEMES:
        return {
            "title": "#FFFFFF",
            "title_inactive": "#F5F5F5",
            "background": "#F0F0F0",
            "surface": "#F3F3F3",
            "elevated": "#F6F6F6",
            "panel": "#F0F0F0",
            "toolbar": "#F0F0F0",
            "tab_bar": "#E8E8E8",
            "tab_inactive": "#E4E4E4",
            "tab_active": "#F8F8F8",
            "element": "#FAFAFA",
            "element_hover": "#F0F0F0",
            "element_active": "#E4E4E4",
            "element_selected": "#E8E8E8",
            "element_disabled": "#F2F2F2",
            "border": "#D0D0D0",
            "border_variant": "#E0E0E0",
            "border_disabled": "#E4E4E4",
            "focus": "#B3CCFF",
            "border_selected": "#7FB5FF",
            "text": "#333333",
            "muted": "#808080",
            "placeholder": "#999999",
            "disabled_text": "#AAAAAA",
            "accent": "#007CFF",
            "link": "#2D64D2",
            "scrollbar": "#808080",
        }

    if name not in TURBO_SCHEMES:
        return {
            "title": "#242424",
            "title_inactive": "#202020",
            "background": "#202020",
            "surface": "#272727",
            "elevated": "#303030",
            "panel": "#202020",
            "toolbar": "#202020",
            "tab_bar": "#202020",
            "tab_inactive": "#212121",
            "tab_active": "#313131",
            "element": "#303030",
            "element_hover": "#383838",
            "element_active": "#454545",
            "element_selected": "#404040",
            "element_disabled": "#282828",
            "border": "#404040",
            "border_variant": "#303030",
            "border_disabled": "#333333",
            "focus": "#99CCFF",
            "border_selected": "#5F9DDA",
            "text": "#D9D9D9",
            "muted": "#999999",
            "placeholder": "#777777",
            "disabled_text": "#666666",
            "accent": "#99CCFF",
            "link": "#82B8FF",
            "scrollbar": "#A0A0A0",
        }

    # The DOS IDEs need more than charcoal around their saturated blue editor.
    # Tint Timeless Dark's neutral luminance steps toward Borland blue while
    # retaining its dark title bar, raised active tab, and subtle sidebars.
    def tint(neutral):
        return mix(neutral, colors["g_bg"], 0.36)

    surface = tint("#272727")
    return {
        "title": tint("#242424"),
        "title_inactive": tint("#202020"),
        "background": tint("#202020"),
        "surface": surface,
        "elevated": tint("#303030"),
        "panel": tint("#202020"),
        "toolbar": tint("#202020"),
        "tab_bar": tint("#202020"),
        "tab_inactive": tint("#212121"),
        "tab_active": tint("#313131"),
        "element": tint("#303030"),
        "element_hover": tint("#383838"),
        "element_active": tint("#454545"),
        "element_selected": tint("#404040"),
        "element_disabled": tint("#282828"),
        "border": tint("#404040"),
        "border_variant": tint("#303030"),
        "border_disabled": tint("#333333"),
        "focus": colors["g_accent"],
        "border_selected": colors["g_accent"],
        "text": colors["g_fg"],
        "muted": colors["g_gutter_fg"],
        "placeholder": mix(colors["g_fg"], surface, 0.55),
        "disabled_text": mix(colors["g_fg"], surface, 0.70),
        "accent": colors["g_accent"],
        "link": colors["link"],
        "scrollbar": colors["g_fg"],
    }


def build_theme(scheme):
    colors = scheme["colors"]
    dark = scheme["name"] in DARK_SCHEMES
    background = colors["g_bg"]
    ui = timeless_ui_palette(scheme)
    transparent = alpha(ui["background"], "00")

    style = {
        "background.appearance": "opaque",
        "border": zed_color(ui["border"]),
        "border.variant": zed_color(ui["border_variant"]),
        "border.focused": zed_color(ui["focus"]),
        "border.selected": zed_color(ui["border_selected"]),
        "border.transparent": transparent,
        "border.disabled": zed_color(ui["border_disabled"]),
        "elevated_surface.background": zed_color(ui["elevated"]),
        "surface.background": zed_color(ui["surface"]),
        "background": zed_color(ui["background"]),
        "element.background": zed_color(ui["element"]),
        "element.hover": zed_color(ui["element_hover"]),
        "element.active": zed_color(ui["element_active"]),
        "element.selected": zed_color(ui["element_selected"]),
        "element.disabled": zed_color(ui["element_disabled"]),
        "drop_target.background": alpha(ui["accent"], "4D"),
        "ghost_element.background": transparent,
        "ghost_element.hover": alpha(ui["text"], "0D"),
        "ghost_element.active": alpha(ui["text"], "18"),
        "ghost_element.selected": alpha(ui["text"], "0D"),
        "ghost_element.disabled": alpha(ui["text"], "08"),
        "text": zed_color(ui["text"]),
        "text.muted": zed_color(ui["muted"]),
        "text.placeholder": zed_color(ui["placeholder"]),
        "text.disabled": zed_color(ui["disabled_text"]),
        "text.accent": zed_color(ui["link"]),
        "icon": zed_color(ui["text"]),
        "icon.muted": zed_color(ui["muted"]),
        "icon.disabled": zed_color(ui["disabled_text"]),
        "icon.placeholder": zed_color(ui["placeholder"]),
        "icon.accent": zed_color(ui["accent"]),
        "status_bar.background": zed_color(ui["panel"]),
        "title_bar.background": zed_color(ui["title"]),
        "title_bar.inactive_background": zed_color(ui["title_inactive"]),
        "toolbar.background": zed_color(ui["toolbar"]),
        "tab_bar.background": zed_color(ui["tab_bar"]),
        "tab.inactive_background": zed_color(ui["tab_inactive"]),
        "tab.active_background": zed_color(ui["tab_active"]),
        "search.match_background": alpha(colors["g_find"], "66"),
        "search.active_match_background": alpha(colors["g_highlight"], "66"),
        "panel.background": zed_color(ui["surface"]),
        "panel.focused_border": zed_color(ui["focus"]),
        "pane.focused_border": zed_color(ui["focus"]),
        "pane_group.border": zed_color(ui["border"]),
        "panel.indent_guide": zed_color(ui["border_variant"]),
        "panel.indent_guide_active": zed_color(ui["border"]),
        "panel.indent_guide_hover": zed_color(ui["border_selected"]),
        "scrollbar.thumb.background": alpha(ui["scrollbar"], "2E"),
        "scrollbar.thumb.hover_background": alpha(ui["scrollbar"], "40"),
        "scrollbar.thumb.border": transparent,
        "scrollbar.track.background": transparent,
        "scrollbar.track.border": transparent,
        "editor.foreground": zed_color(colors["g_fg"]),
        "editor.background": zed_color(background),
        "editor.gutter.background": zed_color(colors["g_gutter"]),
        "editor.subheader.background": zed_color(ui["panel"]),
        "editor.active_line.background": zed_color(colors["g_line_hl"]),
        "editor.highlighted_line.background": zed_color(colors["g_inactive_sel"]),
        "editor.line_number": zed_color(colors["g_gutter_fg"]),
        "editor.active_line_number": zed_color(colors["g_gutter_fg_hl"]),
        "editor.hover_line_number": zed_color(colors["g_fg"]),
        "editor.invisible": zed_color(colors["g_invisibles"]),
        "editor.indent_guide": zed_color(colors["g_guide"]),
        "editor.indent_guide_active": zed_color(colors["g_active_guide"]),
        "editor.wrap_guide": zed_color(colors["g_guide"]),
        "editor.active_wrap_guide": zed_color(colors["g_active_guide"]),
        "editor.document_highlight.bracket_background": alpha(colors["g_brackets"], "28"),
        "editor.document_highlight.read_background": alpha(colors["g_find"], "66"),
        "editor.document_highlight.write_background": alpha(colors["g_highlight"], "66"),
        "link_text.hover": zed_color(ui["link"]),
        "version_control.added": zed_color(colors["diff_add_fg"]),
        "version_control.modified": zed_color(colors["diff_chg_fg"]),
        "version_control.word_added": alpha(colors["diff_add_fg"], "59"),
        "version_control.word_deleted": alpha(colors["diff_del_fg"], "80"),
        "version_control.deleted": zed_color(colors["diff_del_fg"]),
        "version_control.conflict_marker.ours": zed_color(colors["diff_add_bg"]),
        "version_control.conflict_marker.theirs": zed_color(colors["diff_chg_bg"]),
    }

    status_colors(style, "conflict", colors["diff_chg_fg"],
                  colors["diff_chg_bg"], colors["reg_yellow"])
    status_colors(style, "created", colors["diff_add_fg"],
                  colors["diff_add_bg"], colors["reg_green"])
    status_colors(style, "deleted", colors["diff_del_fg"],
                  colors["diff_del_bg"], colors["reg_red"])
    status_colors(style, "error", colors["reg_red"],
                  colors["diff_del_bg"], colors["reg_red"])
    status_colors(style, "hidden", ui["muted"], ui["surface"], ui["border"])
    status_colors(style, "hint", colors["reg_blue"],
                  colors["interp_bg"], colors["reg_blue"])
    status_colors(style, "ignored", ui["muted"], ui["surface"], ui["border"])
    status_colors(style, "info", colors["reg_blue"],
                  colors["interp_bg"], colors["reg_blue"])
    status_colors(style, "modified", colors["diff_chg_fg"],
                  colors["diff_chg_bg"], colors["reg_yellow"])
    status_colors(style, "predictive", colors["preproc_inactive"],
                  colors["raw_bg"], colors["g_guide"])
    status_colors(style, "renamed", colors["reg_blue"],
                  colors["interp_bg"], colors["reg_blue"])
    status_colors(style, "success", colors["reg_green"],
                  colors["diff_add_bg"], colors["reg_green"])
    status_colors(style, "unreachable", colors["preproc_inactive"],
                  ui["surface"], ui["border"])
    status_colors(style, "warning", colors["reg_yellow"],
                  colors["diff_chg_bg"], colors["reg_yellow"])

    ansi = {
        "black": "#000000",
        "red": colors["reg_red"],
        "green": colors["reg_green"],
        "yellow": colors["reg_yellow"],
        "blue": colors["reg_blue"],
        "magenta": colors["reg_purple"],
        "cyan": colors["g_accent"],
        "white": "#D0D0D0" if dark else "#BFBFBF",
    }
    style["terminal.background"] = zed_color(background)
    style["terminal.ansi.background"] = zed_color(background)
    style["terminal.foreground"] = zed_color(colors["g_fg"])
    style["terminal.bright_foreground"] = zed_color(colors["g_fg"])
    style["terminal.dim_foreground"] = zed_color(colors["g_gutter_fg"])
    for name, value in ansi.items():
        bright = (colors["g_gutter_fg"] if name == "black"
                  else "#FFFFFF" if name == "white"
                  else mix(value, "#FFFFFF", 0.22) if dark else value)
        style["terminal.ansi." + name] = zed_color(value)
        style["terminal.ansi.bright_" + name] = zed_color(bright)
        style["terminal.ansi.dim_" + name] = zed_color(
            mix(value, background, 0.55))

    accents = [
        colors["g_accent"],
        colors["reg_purple"],
        colors["reg_orange"],
        colors["reg_pink"],
        colors["reg_blue"],
        colors["reg_red"],
        colors["reg_yellow"],
        colors["reg_green"],
    ]
    style["accents"] = [zed_color(color) for color in accents]
    style["players"] = [{
        "cursor": zed_color(colors["g_caret"]),
        "background": zed_color(colors["g_accent"]),
        "selection": alpha(colors["g_sel"], "99"),
    }] + [
        {
            "cursor": zed_color(color),
            "background": zed_color(color),
            "selection": alpha(color, "3D"),
        }
        for color in accents[1:]
    ]
    style["syntax"] = {
        spec.capture: syntax_style(scheme, spec)
        for spec in SYNTAX_SPECS
    }

    return {
        "name": scheme["name"],
        "appearance": "dark" if dark else "light",
        "style": style,
    }


def build_family(scheme):
    return {
        "$schema": SCHEMA,
        "name": scheme["name"],
        "author": AUTHOR,
        "themes": [build_theme(scheme)],
    }


def validate():
    check_all()
    captures = [spec.capture for spec in SYNTAX_SPECS]
    duplicates = sorted(capture for capture in set(captures)
                        if captures.count(capture) > 1)
    if duplicates:
        raise SystemExit("duplicate Zed syntax captures: %s" % duplicates)

    roles = {spec.color for spec in SYNTAX_SPECS}
    roles.update(spec.background for spec in SYNTAX_SPECS if spec.background)
    style_roles = {spec.style for spec in SYNTAX_SPECS if spec.style}
    for scheme in SCHEMES:
        missing_roles = sorted(roles - set(scheme["colors"]))
        missing_styles = sorted(style_roles - set(scheme["styles"]))
        if missing_roles or missing_styles:
            raise SystemExit(
                "%s: missing roles %s or styles %s" %
                (scheme["name"], missing_roles, missing_styles))
        if contrast(scheme["colors"]["g_bg"], scheme["colors"]["g_fg"]) < 4.5:
            raise SystemExit("%s: editor foreground contrast is too low" %
                             scheme["name"])

        theme = build_theme(scheme)
        if len(theme["style"]["syntax"]) != len(SYNTAX_SPECS):
            raise SystemExit("%s: incomplete Zed syntax map" % scheme["name"])
        ui_text = theme["style"]["text"]
        if contrast(ui_text, theme["style"]["element.selected"]) < 4.5:
            raise SystemExit("%s: selected UI text contrast is too low" %
                             scheme["name"])
        if contrast(ui_text, theme["style"]["surface.background"]) < 4.5:
            raise SystemExit("%s: UI surface text contrast is too low" %
                             scheme["name"])
        for key, value in theme["style"].items():
            if key in {"accents", "players", "syntax", "background.appearance"}:
                continue
            if not isinstance(value, str) or not re.fullmatch(
                    r"#[0-9A-F]{8}", value):
                raise SystemExit("%s: invalid Zed color for %s" %
                                 (scheme["name"], key))


def main():
    validate()
    OUT.mkdir(parents=True, exist_ok=True)
    for scheme in SCHEMES:
        path = OUT / (slug(scheme["name"]) + ".json")
        path.write_text(
            json.dumps(build_family(scheme), indent=2) + "\n",
            encoding="utf-8",
        )
        print("wrote %-26s Zed UI and syntax theme" % scheme["name"])


if __name__ == "__main__":
    main()
