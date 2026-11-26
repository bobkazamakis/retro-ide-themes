#!/usr/bin/env python3
"""Generate twenty-one JetBrains editor schemes and Islands UI themes.

The palettes come from build_schemes.py. The output is a cross-product
IntelliJ Platform plugin for JetBrains IDEs 2025.3 and newer, plus standalone
.icls files that can be imported without installing the UI theme plugin.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import json
from pathlib import Path
import re
import uuid
import xml.etree.ElementTree as ET
import zipfile

from build_schemes import SCHEMES, check_all, theme_name


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "jetbrains"
PLUGIN = OUT / "plugin"
THEMES = PLUGIN / "themes"
COLOR_SCHEMES = PLUGIN / "colorSchemes"
IMPORTABLE_SCHEMES = OUT / "schemes"

PLUGIN_ID = "retro.ide.islands.themes"
PLUGIN_NAME = "Retro IDE Islands Themes"
PLUGIN_VERSION = "1.3.0"
PLUGIN_VENDOR = "Retro IDE Themes"
SINCE_BUILD = "253"
FONT_NAME = "JetBrains Mono"
FONT_SIZE = 14
LINE_SPACING = 1.1

DARK_SCHEMES = {
    "Turbo Pascal",
    "Turbo C++ 3.0",
    "Visual Studio 2012 Dark",
    "Visual Studio Enhanced Dark",
}

@dataclass(frozen=True)
class AttributeSpec:
    name: str
    foreground: str | None = None
    background: str | None = None
    style: str | None = None
    effect: str | None = None
    effect_type: int | None = None
    stripe: str | None = None


ATTRIBUTE_SPECS = []


def attributes(names, foreground=None, background=None, style=None,
               effect=None, effect_type=None, stripe=None):
    """Add one palette mapping for one or more JetBrains attribute keys."""
    if isinstance(names, str):
        names = names.split()
    for name in names:
        ATTRIBUTE_SPECS.append(AttributeSpec(
            name, foreground, background, style, effect, effect_type, stripe))


# General language defaults. Language plugins inherit most of these keys.
attributes("TEXT", "g_fg", "g_bg")
attributes(
    "DEFAULT_IDENTIFIER DEFAULT_LOCAL_VARIABLE LOCAL_VARIABLE_ATTRIBUTES "
    "IMPLICIT_ANONYMOUS_CLASS_PARAMETER_ATTRIBUTES JS.LOCAL_VARIABLE "
    "KOTLIN_MUTABLE_VARIABLE",
    "var_local")
attributes([
    "DEFAULT_INSTANCE_FIELD",
    "INSTANCE_FIELD_ATTRIBUTES",
    "KOTLIN_BACKING_FIELD_VARIABLE",
    "Static property reference ID",
], "member", style="member")
attributes(
    "DEFAULT_STATIC_FIELD STATIC_FIELD_ATTRIBUTES STATIC_FINAL_FIELD_ATTRIBUTES",
    "member_static")
attributes("JS.GLOBAL_VARIABLE TS.GLOBAL_VARIABLE", "var_global")
attributes("SQL_OUTER_QUERY_COLUMN", "const_other")
attributes(
    "DEFAULT_CONSTANT KOTLIN_ENUM_ENTRY KOTLIN_SMART_CONSTANT",
    "const_other", style="const_lang")
attributes(
    "DEFAULT_PREDEFINED_SYMBOL PY.PREDEFINED_DEFINITION PY.PREDEFINED_USAGE "
    "JSON.KEYWORD",
    "const_lang", style="const_lang")
attributes(
    "DEFAULT_KEYWORD JAVA_KEYWORD PY.KEYWORD JS.KEYWORD "
    "TS.KEYWORD CSS.KEYWORD SQL_KEYWORD JSP_DIRECTIVE_NAME",
    "keyword", style="keyword")
attributes("PY.SELF_PARAMETER", "self", style="self")
attributes(
    "DEFAULT_OPERATION_SIGN JAVA_OPERATION_SIGN "
    "JS.OPERATION_SIGN TS.OPERATION_SIGN",
    "operator")
attributes(
    "DEFAULT_BRACES DEFAULT_BRACKETS DEFAULT_PARENTHS JAVA_BRACES JAVA_BRACKETS",
    "brace")
attributes(
    "DEFAULT_COMMA DEFAULT_DOT DEFAULT_SEMICOLON JAVA_COMMA JAVA_DOT "
    "JAVA_SEMICOLON",
    "punct")
attributes("DEFAULT_LABEL KOTLIN_LABEL", "label")

# Comments and documentation.
attributes(
    "DEFAULT_LINE_COMMENT DEFAULT_BLOCK_COMMENT COMMENT JAVA_LINE_COMMENT "
    "JAVA_BLOCK_COMMENT KOTLIN_LINE_COMMENT KOTLIN_BLOCK_COMMENT "
    "PY.LINE_COMMENT JS.LINE_COMMENT JS.BLOCK_COMMENT JSON.LINE_COMMENT "
    "JSON.BLOCK_COMMENT CSS.COMMENT",
    "comment", style="comment")
attributes(
    "DEFAULT_DOC_COMMENT JAVA_DOC_COMMENT KOTLIN_DOC_COMMENT PY.DOC_COMMENT",
    "doc", style="doc")
attributes(
    "DEFAULT_DOC_COMMENT_TAG DEFAULT_DOC_COMMENT_TAG_VALUE DEFAULT_DOC_MARKUP",
    "doc_key", style="doc_key")
attributes("TODO_DEFAULT_ATTRIBUTES", "codetag", style="codetag", stripe="codetag")
attributes("DOC_CODE_BLOCK DOC_CODE_INLINE", "raw", "raw_bg")

# Strings, escapes, regular expressions, and interpolation.
attributes(
    "DEFAULT_STRING JAVA_STRING JAVA_CHAR PY.STRING PY.STRING.B "
    "JS.STRING TS.STRING JSON.STRING YAML_SCALAR_VALUE YAML_SCALAR_LIST "
    "HTML_ATTRIBUTE_VALUE XML_ATTRIBUTE_VALUE CUSTOM_STRING_ATTRIBUTES",
    "string", style="string")
attributes(
    "DEFAULT_VALID_STRING_ESCAPE CUSTOM_VALID_STRING_ESCAPE_ATTRIBUTES "
    "JAVA_VALID_STRING_ESCAPE JS.VALID_STRING_ESCAPE "
    "TS.VALID_STRING_ESCAPE REGEXP.ESC_CHARACTER",
    "escape")
attributes(
    "DEFAULT_INVALID_STRING_ESCAPE CUSTOM_INVALID_STRING_ESCAPE_ATTRIBUTES "
    "JAVA_INVALID_STRING_ESCAPE JS.INVALID_STRING_ESCAPE TS.INVALID_STRING_ESCAPE "
    "JSON.INVALID_ESCAPE PROPERTIES.INVALID_STRING_ESCAPE",
    "escape", effect="reg_red", effect_type=2, stripe="reg_red")
attributes("JS.REGEXP GHERKIN_REGEXP_PARAMETER", "regexp")
attributes(
    "REGEXP.BRACES REGEXP.BRACKETS REGEXP.CHAR_CLASS REGEXP.META "
    "REGEXP.PARENTHS REGEXP.QUOTE_CHARACTER REGEXP.REDUNDANT_ESCAPE",
    "regexp_op")
attributes("INJECTED_LANGUAGE_FRAGMENT", "interp_fg", "interp_bg")
attributes("DEFAULT_TEMPLATE_LANGUAGE_COLOR QUTE_BACKGROUND", background="interp_bg")

# Numbers, metadata, types, functions, parameters, and variables.
attributes("DEFAULT_NUMBER JAVA_NUMBER PY.NUMBER JS.NUMBER TS.NUMBER CSS.NUMBER", "number")
attributes(
    "DEFAULT_METADATA DEFAULT_ATTRIBUTE ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES "
    "ANNOTATION_NAME_ATTRIBUTES PY.ANNOTATION PY.DECORATOR JS.ATTRIBUTE",
    "attribute", style="attribute")
attributes(
    "DEFAULT_CLASS_NAME CLASS_NAME_ATTRIBUTES INTERFACE_NAME_ATTRIBUTES "
    "KOTLIN_CLASS KOTLIN_ABSTRACT_CLASS",
    "type", style="type")
attributes(
    "DEFAULT_CLASS_REFERENCE CLASS_REFERENCE TYPE_PARAMETER_NAME_ATTRIBUTES "
    "KOTLIN_TYPE_PARAMETER KOTLIN_TYPE_ALIAS TS.TYPE_PARAMETER",
    "type_lib", style="type")
attributes("DEFAULT_FUNCTION_DECLARATION", "func_global_decl", style="func_decl")
attributes("METHOD_DECLARATION_ATTRIBUTES", "func_member_decl", style="func_decl")
attributes(
    "DEFAULT_FUNCTION_CALL JS.GLOBAL_FUNCTION TS.GLOBAL_FUNCTION "
    "CSS.FUNCTION KOTLIN_VARIABLE_AS_FUNCTION "
    "KOTLIN_VARIABLE_AS_FUNCTION_LIKE",
    "func_global_call", style="func_call")
attributes(
    "DEFAULT_INSTANCE_METHOD DEFAULT_STATIC_METHOD METHOD_CALL_ATTRIBUTES "
    "CONSTRUCTOR_CALL_ATTRIBUTES STATIC_METHOD_ATTRIBUTES JS.INSTANCE_MEMBER_FUNCTION",
    "func_member_call", style="func_call")
attributes("PY.BUILTIN_NAME", "func_builtin", style="func_call")
attributes(
    "DEFAULT_PARAMETER PARAMETER_ATTRIBUTES PY.PARAMETER JS.PARAMETER TS.PARAMETER",
    "param", style="param")
attributes("PY.KEYWORD_ARGUMENT KOTLIN_NAMED_ARGUMENT", "arg_label")
attributes(
    "DEFAULT_REASSIGNED_LOCAL_VARIABLE DEFAULT_REASSIGNED_PARAMETER "
    "REASSIGNED_LOCAL_VARIABLE_ATTRIBUTES REASSIGNED_PARAMETER_ATTRIBUTES",
    "var", effect="continuation", effect_type=1)
attributes("CONDITIONALLY_NOT_COMPILED", "preproc_inactive")

# CLion's C/C++ highlighter uses OC.* keys instead of relying exclusively on
# the platform defaults. Keep these explicit so the historic C-family palettes
# survive both lexical and semantic highlighting.
attributes("OC.KEYWORD OC.CPP_KEYWORD", "keyword", style="keyword")
attributes("OC.DIRECTIVE", "preproc", style="preproc")
attributes("OC.MACRONAME", "macro", style="preproc")
attributes("OC.MACRO_PARAMETER", "param", style="param")
attributes("OC.CONDITIONALLY_NOT_COMPILED", "preproc_inactive")
attributes("OC.NUMBER", "number")
attributes("OC.LINE_COMMENT OC.BLOCK_COMMENT", "comment", style="comment")
attributes("OC.STRING OC.HEADER_PATH", "string", style="string")
attributes("OC.FORMAT_TOKEN", "escape")
attributes("OC.FUNCTION", "func_global_call", style="func_call")
attributes("OC.METHOD_DECLARATION", "func_member_decl", style="func_decl")
attributes("OC.PARAMETER", "param", style="param")
attributes("OC.LOCAL_VARIABLE", "var_local")
attributes("OC.GLOBAL_VARIABLE OC.EXTERN_VARIABLE", "var_global")
attributes("OC.IVAR OC.STRUCT_FIELD OC.PROPERTY", "member", style="member")
attributes("OC.STRUCT_LIKE OC.CLASS_REFERENCE OC.TYPEDEF", "type", style="type")
attributes("OC.ENUM_CONST", "enum_member")
attributes("OC.NAMESPACE_LIKE", "module")
attributes("OC.OVERLOADED_OPERATOR", "operator_decl", style="operator_decl")
attributes("OC.LABEL", "label")

# Markup, data files, and web languages.
attributes(
    "MARKDOWN_HEADER MARKDOWN_HEADER_LEVEL_1 MARKDOWN_HEADER_LEVEL_2 "
    "MARKDOWN_HEADER_LEVEL_3 MARKDOWN_HEADER_LEVEL_4 MARKDOWN_HEADER_LEVEL_5 "
    "MARKDOWN_HEADER_LEVEL_6",
    "head", style="head")
attributes("MARKDOWN_BOLD", "bold", style="bold")
attributes("MARKDOWN_ITALIC", "italic", style="italic")
attributes("MARKDOWN_CODE_SPAN MARKDOWN_CODE_SPAN_MARKER", "raw", "raw_bg")
attributes(
    "MARKDOWN_AUTO_LINK MARKDOWN_IMAGE MARKDOWN_LINK_TEXT MARKDOWN_LINK_TITLE "
    "MARKDOWN_REFERENCE_LINK",
    "link", style="underline", effect="link", effect_type=1)
attributes("MARKDOWN_BLOCK_QUOTE", "quote", style="quote")
attributes("MARKDOWN_TABLE_SEPARATOR MARKDOWN_LIST_MARKER", "list_punct")
attributes("JSON.PROPERTY_KEY YAML_SCALAR_KEY PROPERTIES.KEY", "key")
attributes("YAML_ANCHOR", "const_other")
attributes("HTML_TAG_NAME HTML_CUSTOM_TAG_NAME XML_TAG_NAME XML_CUSTOM_TAG_NAME", "tag", style="tag")
attributes("HTML_TAG XML_TAG", "tag")
attributes("HTML_ATTRIBUTE_NAME XML_ATTRIBUTE_NAME XML_NS_PREFIX", "tag_attr")
attributes("HTML_ENTITY_REFERENCE XML_ENTITY_REFERENCE", "escape")
attributes("XML_PROLOGUE", "preproc")
attributes("CSS.PROPERTY_NAME CSS.IDENT", "key")
attributes("CSS.PROPERTY_VALUE", "string")
attributes("CSS.TAG_NAME CSS.PSEUDO CSS.HASH", "type")
attributes("CSS.IMPORTANT", "keyword", style="keyword")
attributes("CSS.URL", "link", style="underline", effect="link", effect_type=1)

# Diff, console, editor helpers, and diagnostics.
attributes("DIFF_INSERTED", "diff_add_fg", "diff_add_bg")
attributes("DIFF_DELETED", "diff_del_fg", "diff_del_bg")
attributes("DIFF_MODIFIED DIFF_CONFLICT", "diff_chg_fg", "diff_chg_bg")
attributes("CONSOLE_NORMAL_OUTPUT CONSOLE_SYSTEM_OUTPUT", "g_fg")
attributes("CONSOLE_USER_INPUT", "reg_green")
attributes("CONSOLE_ERROR_OUTPUT LOG_ERROR_OUTPUT", "reg_red")
attributes("LOG_WARNING_OUTPUT", "reg_yellow")
attributes("LOG_INFO_OUTPUT", "reg_blue")
attributes("LOG_VERBOSE_OUTPUT", "g_gutter_fg")
attributes("HYPERLINK_ATTRIBUTES CTRL_CLICKABLE", "link", style="underline", effect="link", effect_type=1)
attributes("FOLLOWED_HYPERLINK_ATTRIBUTES INACTIVE_HYPERLINK_ATTRIBUTES", "quote", style="underline", effect="quote", effect_type=1)
attributes("SEARCH_RESULT_ATTRIBUTES TEXT_SEARCH_RESULT_ATTRIBUTES", "g_find_fg", "g_find")
attributes("WRITE_SEARCH_RESULT_ATTRIBUTES", "g_find_fg", "g_highlight")
attributes("IDENTIFIER_UNDER_CARET_ATTRIBUTES", effect="g_brackets", effect_type=1)
attributes("WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES", effect="g_tags", effect_type=1)
attributes("DEFAULT_HIGHLIGHTED_REFERENCE MATCHED_BRACE_ATTRIBUTES MATCHED_TAG_NAME", effect="g_brackets", effect_type=1)
attributes([
    "BAD_CHARACTER",
    "UNMATCHED_BRACE_ATTRIBUTES",
    "WRONG_REFERENCES_ATTRIBUTES",
    "RUNTIME_ERROR",
    "Unresolved reference access",
], "invalid_fg", "invalid_bg", effect="reg_red", effect_type=2,
   stripe="reg_red")
attributes("ERRORS_ATTRIBUTES TEXT_STYLE_ERROR", effect="reg_red", effect_type=2, stripe="reg_red")
attributes("WARNING_ATTRIBUTES TEXT_STYLE_WARNING", effect="reg_yellow", effect_type=2, stripe="reg_yellow")
attributes("WEAK_WARNING_ATTRIBUTES INFO_ATTRIBUTES", effect="reg_blue", effect_type=1, stripe="reg_blue")
attributes("DEPRECATED_ATTRIBUTES MARKED_FOR_REMOVAL_ATTRIBUTES", effect="deprecated_bg", effect_type=3)
attributes("TYPO", effect="reg_green", effect_type=2)
attributes("FOLDED_TEXT_ATTRIBUTES", "raw", "raw_bg")
attributes("BREAKPOINT_ATTRIBUTES", background="invalid_bg", stripe="reg_red")
attributes("EXECUTIONPOINT_ATTRIBUTES", "g_fg", "g_highlight")
attributes("LIVE_TEMPLATE_ATTRIBUTES TEMPLATE_VARIABLE_ATTRIBUTES", "attr_option", "interp_bg")
attributes("LIVE_TEMPLATE_INACTIVE_SEGMENT", "preproc_inactive")
attributes("INLAY_DEFAULT INLAY_TEXT_WITHOUT_BACKGROUND INLINE_PARAMETER_HINT", "g_gutter_fg", "interp_bg")
attributes("INLINE_PARAMETER_HINT_CURRENT INLINE_PARAMETER_HINT_HIGHLIGHTED", "g_fg", "g_find")
attributes("BREADCRUMBS_DEFAULT BREADCRUMBS_INACTIVE", "g_gutter_fg")
attributes("BREADCRUMBS_CURRENT BREADCRUMBS_HOVERED", "g_fg", "g_line_hl")


FONT_TYPES = {
    "bold": 1,
    "italic": 2,
    "bold italic": 3,
}


def slug(name):
    value = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not value:
        raise SystemExit("cannot make a file name from %r" % name)
    return value


def strip_hash(color):
    if color is None:
        return ""
    return color.lstrip("#")


def parse_rgb(color):
    value = strip_hash(color)
    if len(value) < 6:
        raise SystemExit("cannot parse color %r" % color)
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def rgb_hex(rgb):
    return "#%02X%02X%02X" % tuple(round(value) for value in rgb)


def mix(first, second, amount):
    a = parse_rgb(first)
    b = parse_rgb(second)
    return rgb_hex(tuple(x + (y - x) * amount for x, y in zip(a, b)))


def alpha(color, value):
    if not re.fullmatch(r"[0-9A-Fa-f]{2}", value):
        raise SystemExit("bad alpha %r" % value)
    return rgb_hex(parse_rgb(color)) + value.upper()


def luminance(color):
    channels = []
    for value in parse_rgb(color):
        value /= 255.0
        channels.append(value / 12.92 if value <= 0.04045
                        else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(first, second):
    if len(first) == 9:
        first = mix(second, first, int(first[-2:], 16) / 255)
    a, b = sorted((luminance(first), luminance(second)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def contrasting_text(background):
    return "#000000" if contrast(background, "#000000") >= contrast(background, "#FFFFFF") else "#FFFFFF"


def macos_ui_palette(dark):
    """Map Aqua and Dark Aqua NSColor defaults sampled in sRGB on macOS 27.2."""
    # Swing uses solid colors for some surfaces. Resolve translucent controls
    # and separators over their AppKit window or under-page background.
    if not dark:
        return {
            "main_window": "#F6F6F6",
            "surface": "#FFFFFF",
            "elevated": "#FFFFFF",
            "panel": "#FFFFFF",
            "tab_inactive": "#DCDCDC",
            "tab_active": "#B3D7FF",
            "element": "#FFFFFF",
            "element_hover": "#E2E2E2",
            "element_active": "#D7D7D7",
            "element_selected": "#0064E1",
            "element_disabled": "#FFFFFF",
            "border": "#E6E6E6",
            "border_variant": "#DDDDDD",
            "grid": "#E6E6E6",
            "focus": "#0067F47F",
            "text": "#000000D8",
            "muted": "#0000007F",
            "disabled_text": "#0000003F",
            "accent": "#007AFF",
            "link": "#0068DA",
            "error": "#FF383C",
            "warning": "#FF8D28",
            "success": "#34C759",
        }

    return {
        "main_window": "#282828",
        "surface": "#1E1E1E",
        "elevated": "#282828",
        "panel": "#1E1E1E",
        "tab_inactive": "#464646",
        "tab_active": "#3F638B",
        "element": "#565656",
        "element_hover": "#515151",
        "element_active": "#454545",
        "element_selected": "#0059D1",
        "element_disabled": "#3A3A3A",
        "border": "#393939",
        "border_variant": "#424242",
        "grid": "#1A1A1A",
        "focus": "#1AA9FF7F",
        "text": "#FFFFFFD8",
        "muted": "#FFFFFF8C",
        "disabled_text": "#FFFFFF3F",
        "accent": "#007AFF",
        "link": "#419CFF",
        "error": "#FF4245",
        "warning": "#FF9230",
        "success": "#30D158",
    }


def style_options(scheme, style_role):
    if style_role is None:
        return None, False
    style = scheme["styles"].get(style_role)
    if style is None:
        return None, False
    return FONT_TYPES.get(style), "underline" in style


def add_value_option(value, name, value_text):
    ET.SubElement(value, "option", {"name": name, "value": str(value_text)})


def build_editor_scheme(scheme):
    colors = scheme["colors"]
    dark = scheme["name"] in DARK_SCHEMES
    root = ET.Element("scheme", {
        "name": theme_name(scheme),
        "version": "142",
        "parent_scheme": "Darcula" if dark else "Default",
    })

    meta = ET.SubElement(root, "metaInfo")
    for key, value in (
        ("ide", "idea"),
        ("ideVersion", "2025.3.0.0"),
        ("originalScheme", theme_name(scheme)),
        ("pluginId", PLUGIN_ID),
    ):
        child = ET.SubElement(meta, "property", {"name": key})
        child.text = value

    for key, value in (
        ("EDITOR_FONT_NAME", FONT_NAME),
        ("EDITOR_FONT_SIZE", FONT_SIZE),
        ("EDITOR_LIGATURES", "false"),
        ("LINE_SPACING", LINE_SPACING),
        ("CONSOLE_FONT_NAME", FONT_NAME),
        ("CONSOLE_FONT_SIZE", FONT_SIZE),
        ("CONSOLE_LIGATURES", "false"),
        ("CONSOLE_LINE_SPACING", LINE_SPACING),
    ):
        ET.SubElement(root, "option", {"name": key, "value": str(value)})

    editor_colors = ET.SubElement(root, "colors")
    color_values = [
        ("CARET_COLOR", colors["g_caret"]),
        ("CARET_ROW_COLOR", colors["g_line_hl"]),
        ("CONSOLE_BACKGROUND_KEY", colors["g_bg"]),
        ("DOCUMENTATION_COLOR", colors["raw_bg"]),
        ("GUTTER_BACKGROUND", colors["g_bg"]),
        ("INDENT_GUIDE", colors["g_guide"]),
        ("LINE_NUMBERS_COLOR", colors["g_gutter_fg"]),
        ("LINE_NUMBER_ON_CARET_ROW_COLOR", colors["g_gutter_fg_hl"]),
        ("LOOKUP_COLOR", colors["raw_bg"]),
        ("METHOD_SEPARATORS_COLOR", colors["g_guide"]),
        ("RIGHT_MARGIN_COLOR", colors["g_guide"]),
        ("SELECTED_INDENT_GUIDE", colors["g_active_guide"]),
        ("SELECTION_BACKGROUND", colors["g_sel"]),
        ("SELECTION_BACKGROUND_INACTIVE", colors["g_inactive_sel"]),
        ("SELECTION_FOREGROUND", colors["g_sel_fg"]),
        ("SOFT_WRAP_SIGN_COLOR", colors["g_gutter_fg"]),
        ("VISUAL_INDENT_GUIDE", colors["g_stack_guide"]),
        ("WHITESPACES", colors["g_invisibles"]),
        ("FOLDED_TEXT_BORDER_COLOR", colors["g_fold"]),
        ("ADDED_LINES_COLOR", colors["diff_add_fg"]),
        ("MODIFIED_LINES_COLOR", colors["diff_chg_fg"]),
        ("DELETED_LINES_COLOR", colors["diff_del_fg"]),
        ("FILESTATUS_ADDED", colors["diff_add_fg"]),
        ("FILESTATUS_MODIFIED", colors["reg_blue"]),
        ("FILESTATUS_DELETED", colors["diff_del_fg"]),
        ("FILESTATUS_UNKNOWN", colors["reg_red"]),
        ("FILESTATUS_MERGED", colors["reg_purple"]),
        ("ScrollBar.background", colors["g_bg"]),
        ("ScrollBar.thumbColor", alpha(colors["g_fg"], "28")),
        ("ScrollBar.hoverThumbColor", alpha(colors["g_fg"], "55")),
        ("ScrollBar.Transparent.thumbColor", alpha(colors["g_fg"], "28")),
        ("ScrollBar.Transparent.hoverThumbColor", alpha(colors["g_fg"], "55")),
        ("ScrollBar.Mac.thumbColor", alpha(colors["g_fg"], "28")),
        ("ScrollBar.Mac.hoverThumbColor", alpha(colors["g_fg"], "55")),
        ("ScrollBar.Mac.Transparent.thumbColor", alpha(colors["g_fg"], "28")),
        ("ScrollBar.Mac.Transparent.hoverThumbColor", alpha(colors["g_fg"], "55")),
    ]
    for key, value in color_values:
        ET.SubElement(editor_colors, "option", {
            "name": key,
            "value": strip_hash(value),
        })

    editor_attributes = ET.SubElement(root, "attributes")
    for spec in ATTRIBUTE_SPECS:
        option = ET.SubElement(
            editor_attributes, "option", {"name": spec.name})
        value = ET.SubElement(option, "value")
        if spec.foreground:
            add_value_option(value, "FOREGROUND", strip_hash(colors[spec.foreground]))
        if spec.background:
            add_value_option(value, "BACKGROUND", strip_hash(colors[spec.background]))
        font_type, underline = style_options(scheme, spec.style)
        if font_type is not None:
            add_value_option(value, "FONT_TYPE", font_type)
        effect = spec.effect
        effect_type = spec.effect_type
        if underline and effect is None:
            effect = spec.foreground
            effect_type = 1
        if effect:
            add_value_option(value, "EFFECT_COLOR", strip_hash(colors[effect]))
        if effect_type is not None:
            add_value_option(value, "EFFECT_TYPE", effect_type)
        if spec.stripe:
            add_value_option(value, "ERROR_STRIPE_COLOR", strip_hash(colors[spec.stripe]))

    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="unicode") + "\n"


def build_theme(scheme):
    colors = scheme["colors"]
    dark = scheme["name"] in DARK_SCHEMES
    background = colors["g_bg"]
    chrome = macos_ui_palette(dark)
    # Aqua's status colors need a darker foreground on white surfaces.
    status_text_mix = 0 if dark else 0.38
    accent_secondary = mix(chrome["panel"], chrome["accent"], 0.18)
    error_secondary = mix(chrome["panel"], chrome["error"], 0.16)
    warning_secondary = mix(chrome["panel"], chrome["warning"], 0.16)
    success_secondary = mix(chrome["panel"], chrome["success"], 0.16)

    named_colors = {
        "transparent": alpha(chrome["main_window"], "00"),
        "text-default": chrome["text"],
        "text-muted": chrome["muted"],
        "text-secondary": mix(chrome["text"], chrome["surface"], 0.32),
        "text-disabled": chrome["disabled_text"],
        "text-over-accent": "#FFFFFF",
        "text-over-accent-inverted": chrome["text"],
        "text-link": chrome["link"],
        "text-error": mix(chrome["error"], chrome["text"], status_text_mix),
        "text-warning": mix(chrome["warning"], chrome["text"], status_text_mix),
        "text-success": mix(chrome["success"], chrome["text"], status_text_mix),
        "editor-text": colors["g_fg"],
        "layer-0-bg": chrome["main_window"],
        "layer-0-bg-inline": chrome["main_window"],
        "layer-0-border": chrome["border"],
        "layer-0-border-inline": chrome["border"],
        "layer-1-bg": chrome["panel"],
        "layer-1-bg-inline": chrome["elevated"],
        "layer-1-border": chrome["border"],
        "layer-1-border-inline": chrome["border_variant"],
        "layer-2-bg": chrome["surface"],
        "layer-2-bg-inline": chrome["elevated"],
        "layer-2-border": chrome["border"],
        "layer-2-border-inline": chrome["border_variant"],
        "accent-brand-bg": chrome["accent"],
        "accent-brand-border": chrome["accent"],
        "accent-brand-bg-secondary": accent_secondary,
        "accent-brand-border-secondary": chrome["accent"],
        "accent-error-bg": chrome["error"],
        "accent-error-border": chrome["error"],
        "accent-error-bg-secondary": error_secondary,
        "accent-error-border-secondary": chrome["error"],
        "accent-warning-bg": chrome["warning"],
        "accent-warning-border": chrome["warning"],
        "accent-warning-bg-secondary": warning_secondary,
        "accent-warning-border-secondary": chrome["warning"],
        "accent-success-bg": chrome["success"],
        "accent-success-border": chrome["success"],
        "accent-success-bg-secondary": success_secondary,
        "accent-success-border-secondary": chrome["success"],
        "core-bg-transparent-hovered": alpha(chrome["text"], "12"),
        "core-bg-transparent-pressed": alpha(chrome["text"], "20"),
        "core-border-transparent": alpha(chrome["text"], "24"),
        "dialog-bg": chrome["panel"],
        "dialog-bg-inline": chrome["elevated"],
        "dialog-border": chrome["border"],
        "popup-bg": chrome["elevated"],
        "popup-bg-inline": chrome["elevated"],
        "popup-border": chrome["border"],
        "popup-border-inline": chrome["border_variant"],
        "editor-bg": background,
        "editor-bg-inline": chrome["elevated"],
        "editor-border": chrome["border"],
        "editor-border-inline": chrome["border_variant"],
        "tool-window-bg": chrome["surface"],
        "tool-window-bg-inline": chrome["elevated"],
        "tool-window-border": chrome["border"],
        "tool-window-border-inline": chrome["border_variant"],
        "main-window-bg": chrome["main_window"],
        "main-window-border": chrome["border"],
        "island-border": chrome["border_variant"],
        "table-grid": chrome["grid"],
        # Islands and macOS paint parts of the unified header from the main
        # window rather than TitlePane. All top-bar sources must agree.
        "title-bar-bg": chrome["main_window"],
        "title-bar-bg-inactive": chrome["main_window"],
        "status-bar-bg": chrome["main_window"],
        # The tab bar and editor share one surface inside the island.
        "tab-bar-bg": background,
        "tab-bg-inactive": chrome["tab_inactive"],
        "focus-color": chrome["focus"],
        "control-bg": chrome["element"],
        "control-bg-disabled": chrome["element_disabled"],
        "control-bg-raised": chrome["elevated"],
        "control-border": chrome["border"],
        "control-border-disabled": chrome["border"],
        "control-border-raised": chrome["border_variant"],
        "control-brand-bg": chrome["element_selected"],
        "control-brand-border": chrome["element_selected"],
        "toolbar-bg-hovered": chrome["element_hover"],
        "toolbar-bg-pressed": chrome["element_active"],
        "toolbar-border": chrome["border_variant"],
        "toolbar-selected-bg": chrome["tab_inactive"],
        "toolbar-selected-bg-active": chrome["element_selected"],
        "selection-bg-active": chrome["element_selected"],
        "selection-bg-active-muted": chrome["tab_active"],
        "selection-bg-inactive": chrome["tab_inactive"],
        "selection-bg-hovered": alpha(chrome["text"], "0D"),
        "tab-selected-bg-active": chrome["tab_active"],
        "tab-selected-bg-inactive": chrome["tab_inactive"],
        "tab-selected-border-active": chrome["accent"],
        "tab-selected-border-inactive": chrome["border_variant"],
        "tab-bg-hovered": chrome["element_hover"],
        "tab-file-color-mask-bg": alpha(chrome["main_window"], "80"),
        "feedback-bg": chrome["elevated"],
        "feedback-border": chrome["border"],
        "feedback-brand-bg": accent_secondary,
        "feedback-brand-border": chrome["accent"],
        "feedback-success-bg": success_secondary,
        "feedback-success-border": colors["reg_green"],
        "feedback-warning-bg": warning_secondary,
        "feedback-warning-border": colors["reg_yellow"],
        "feedback-error-bg": error_secondary,
        "feedback-error-border": colors["reg_red"],
        "inlay-bg": colors["interp_bg"],
        "inlay-border": chrome["border"],
        "editor-floating-toolbar-bg": chrome["elevated"],
        "search-match-bg": colors["g_find"],
        "tree-indent-guide-border": chrome["border_variant"],
        "icon-default-stroke": chrome["muted"],
        "icon-over-accent": contrasting_text(chrome["accent"]),
        "icon-green-stroke": chrome["success"],
    }

    ui = {
        "Islands": 1,
        "Island": {
            "arc": 28,
            "arc.compact": 22,
            "borderWidth": 7,
            "borderWidth.compact": 4,
            "borderColor": "island-border",
            "inactiveAlpha": 0.44,
        },
        "MainWindow": {
            "background": "main-window-bg",
            "Tab": {
                "background": "main-window-bg",
                "borderColor": "main-window-bg",
                "selectedBackground": "main-window-bg",
                "selectedInactiveBackground": "main-window-bg",
                "hoverBackground": "toolbar-bg-hovered",
            },
        },
        # On macOS the project/branch controls live in TitlePane while the
        # run controls live in MainToolbar. Both must use the same color or
        # the unified header acquires a hard vertical seam.
        "TitlePane": {
            "background": "title-bar-bg",
            "inactiveBackground": "title-bar-bg-inactive",
            "foreground": "text-default",
            "inactiveForeground": "text-muted",
            "infoForeground": "text-secondary",
            "inactiveInfoForeground": "text-disabled",
        },
        "MainToolbar": {
            "background": "title-bar-bg",
            "inactiveBackground": "title-bar-bg-inactive",
            "foreground": "text-default",
            "borderColor": "transparent",
            "separatorColor": "toolbar-border",
            "Button": {"arc": 22, "arc.compact": 16},
            "Dropdown": {
                "hoverBackground": "toolbar-bg-hovered",
                "pressedBackground": "toolbar-bg-pressed",
            },
            "Icon": {
                "hoverBackground": "toolbar-bg-hovered",
                "pressedBackground": "toolbar-bg-pressed",
            },
        },
        "MenuBar": {
            "background": "title-bar-bg",
            "foreground": "text-default",
            "selectionBackground": "selection-bg-active",
            "selectionForeground": "text-over-accent",
        },
        "StatusBar": {
            "background": "status-bar-bg",
            "borderColor": "transparent",
            "topBorderWidth": 0,
        },
        "ToolWindow": {
            "background": "tool-window-bg",
            "borderColor": "transparent",
            "Header": {
                "background": "tool-window-bg",
                "inactiveBackground": "tool-window-bg",
                "borderColor": "tool-window-border",
            },
            "HeaderTab": {
                "underlineColor": "tab-selected-border-active",
                "inactiveUnderlineColor": "tab-selected-border-inactive",
                "underlinedTabBackground": "tab-selected-bg-active",
                "underlinedTabInactiveBackground": "tab-selected-bg-inactive",
            },
            "Stripe": {
                "background": "main-window-bg",
                "borderColor": "transparent",
                "separatorColor": "toolbar-border",
            },
        },
        "EditorTabs": {
            "background": "tab-bar-bg",
            "underTabsBorderColor": "editor-border",
            "underlinedBorderColor": "tab-selected-border-active",
            "inactiveUnderlinedTabBorderColor": "tab-selected-border-inactive",
            "underlinedTabBackground": "tab-selected-bg-active",
            "underlinedTabForeground": "text-default",
            "inactiveUnderlinedTabBackground": "tab-selected-bg-inactive",
            "hoverBackground": "tab-bg-hovered",
            "hoverInactiveBackground": "tab-bg-hovered",
        },
        "Panel": {"background": "dialog-bg"},
        "Label": {"foreground": "text-default", "disabledForeground": "text-disabled"},
        "Separator": {"separatorColor": "dialog-border"},
        "Tree": {
            "background": "tool-window-bg",
            "foreground": "text-default",
            "selectionBackground": "selection-bg-active",
            "selectionForeground": "text-over-accent",
            "selectionInactiveBackground": "selection-bg-inactive",
            "Selection": {"arc": 12},
        },
        "List": {
            "background": "dialog-bg",
            "foreground": "text-default",
            "selectionBackground": "selection-bg-active",
            "selectionForeground": "text-over-accent",
            "selectionInactiveBackground": "selection-bg-inactive",
            "selectionInactiveForeground": "text-default",
        },
        "Table": {
            "background": "dialog-bg",
            "foreground": "text-default",
            "gridColor": "table-grid",
            "selectionBackground": "selection-bg-active",
            "selectionForeground": "text-over-accent",
            "selectionInactiveBackground": "selection-bg-inactive",
            "selectionInactiveForeground": "text-default",
        },
        "Button": {
            "arc": 14,
            "foreground": "text-default",
            "disabledText": "text-disabled",
            "startBackground": "control-bg",
            "endBackground": "control-bg",
            "startBorderColor": "control-border-raised",
            "endBorderColor": "control-border",
            "default": {
                "foreground": "text-over-accent",
                "startBackground": "control-brand-bg",
                "endBackground": "control-brand-bg",
                "startBorderColor": "control-brand-border",
                "endBorderColor": "control-brand-border",
            },
        },
        "TextField": {
            "background": "dialog-bg",
            "foreground": "text-default",
        },
        "TextArea": {
            "background": "dialog-bg",
            "foreground": "text-default",
        },
        "ComboBox": {
            "background": "control-bg",
            "foreground": "text-default",
        },
        "Popup": {
            "background": "popup-bg",
            "borderColor": "popup-border",
            "separatorColor": "popup-border",
            "Header": {
                "activeBackground": "popup-bg",
                "inactiveBackground": "popup-bg",
            },
            "Selection": {"arc": 12},
        },
        "PopupMenu": {
            "background": "popup-bg",
            "foreground": "text-default",
            "Selection": {"arc": 12},
        },
        "SearchEverywhere": {
            "Header": {"background": "popup-bg"},
            "SearchField": {"background": "dialog-bg"},
            "List": {"settingsBackground": "popup-bg"},
            "Tab": {
                "selectedBackground": "tab-selected-bg-active",
                "selectedForeground": "text-default",
            },
        },
        "MenuItem": {
            "background": "popup-bg",
            "foreground": "text-default",
            "selectionBackground": "selection-bg-active",
            "selectionForeground": "text-over-accent",
        },
        "Component": {
            "arc": 12,
            "borderColor": "control-border",
            "focusColor": "focus-color",
        },
    }

    return {
        "name": theme_name(scheme),
        "dark": dark,
        "author": PLUGIN_VENDOR,
        "parentTheme": "Islands Dark" if dark else "Islands Light",
        "editorScheme": "/colorSchemes/%s.xml" % slug(scheme["name"]),
        "colors": named_colors,
        "ui": ui,
        "icons": {
            "ColorPalette": {
                "Actions.Blue": chrome["accent"],
                "Actions.Green": chrome["success"],
                "Actions.Red": chrome["error"],
                "Actions.Yellow": chrome["warning"],
                "Objects.Blue": colors["reg_blue"],
                "Objects.Green": colors["reg_green"],
                "Objects.Purple": colors["reg_purple"],
                "Objects.Red": colors["reg_red"],
                "Objects.Yellow": colors["reg_yellow"],
            }
        },
    }


def theme_id(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, PLUGIN_ID + "/" + name))


def build_plugin_xml():
    root = ET.Element("idea-plugin")
    for tag, text in (
        ("id", PLUGIN_ID),
        ("name", PLUGIN_NAME),
        ("version", PLUGIN_VERSION),
        ("vendor", PLUGIN_VENDOR),
    ):
        child = ET.SubElement(root, tag)
        child.text = text
    ET.SubElement(root, "idea-version", {"since-build": SINCE_BUILD})
    depends = ET.SubElement(root, "depends")
    depends.text = "com.intellij.modules.platform"
    description = ET.SubElement(root, "description")
    description.text = (
        "Twenty-one retro IDE color schemes with matching Islands UI themes "
        "for IntelliJ Platform-based JetBrains IDEs.")
    extensions = ET.SubElement(root, "extensions", {"defaultExtensionNs": "com.intellij"})
    for scheme in SCHEMES:
        file_slug = slug(scheme["name"])
        ET.SubElement(extensions, "themeProvider", {
            "id": theme_id(scheme["name"]),
            "path": "/themes/%s.theme.json" % file_slug,
            "targetUi": "islands",
        })
        ET.SubElement(extensions, "bundledColorScheme", {
            "id": theme_name(scheme),
            "path": "colorSchemes/%s" % file_slug,
        })
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="unicode") + "\n"


def zip_entry(archive, name, data):
    info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data)


def build_archives(resources):
    jar_buffer = BytesIO()
    with zipfile.ZipFile(jar_buffer, "w") as jar:
        zip_entry(jar, "META-INF/MANIFEST.MF", "Manifest-Version: 1.0\n\n")
        for path, data in sorted(resources.items()):
            zip_entry(jar, path, data)
    jar_data = jar_buffer.getvalue()

    jar_path = OUT / (PLUGIN_NAME + ".jar")
    jar_path.write_bytes(jar_data)

    zip_path = OUT / (PLUGIN_NAME + ".zip")
    with zipfile.ZipFile(zip_path, "w") as archive:
        zip_entry(
            archive,
            "%s/lib/%s.jar" % (PLUGIN_NAME, slug(PLUGIN_NAME)),
            jar_data,
        )
    return jar_path, zip_path


def validate():
    check_all()
    names = [spec.name for spec in ATTRIBUTE_SPECS]
    duplicates = sorted(name for name in set(names) if names.count(name) > 1)
    if duplicates:
        raise SystemExit("duplicate JetBrains attribute keys: %s" % duplicates)
    roles = set()
    styles = set()
    for spec in ATTRIBUTE_SPECS:
        roles.update(role for role in (
            spec.foreground, spec.background, spec.effect, spec.stripe) if role)
        if spec.style:
            styles.add(spec.style)
    for scheme in SCHEMES:
        missing_roles = sorted(roles - set(scheme["colors"]))
        missing_styles = sorted(styles - set(scheme["styles"]))
        if missing_roles or missing_styles:
            raise SystemExit(
                "%s: missing roles %s or styles %s" %
                (scheme["name"], missing_roles, missing_styles))
        theme = build_theme(scheme)
        top_bar_keys = (
            theme["ui"]["TitlePane"]["background"],
            theme["ui"]["TitlePane"]["inactiveBackground"],
            theme["ui"]["MainToolbar"]["background"],
            theme["ui"]["MainToolbar"]["inactiveBackground"],
            theme["ui"]["MainWindow"]["background"],
            theme["ui"]["MainWindow"]["Tab"]["background"],
            theme["ui"]["MainWindow"]["Tab"]["selectedBackground"],
            theme["ui"]["MainWindow"]["Tab"]["selectedInactiveBackground"],
        )
        resolved_top_bar = {theme["colors"][key] for key in top_bar_keys}
        if len(resolved_top_bar) != 1:
            raise SystemExit("%s: split unified top-bar colors %s" %
                             (scheme["name"], sorted(resolved_top_bar)))
        # AppKit's near-neutral surfaces rely on a separator for definition.
        for panel in ("main-window-bg", "editor-bg", "tool-window-bg"):
            if contrast(theme["colors"][panel], theme["colors"]["island-border"]) < 1.20:
                raise SystemExit("%s: %s blends into the island separator" %
                                 (scheme["name"], panel))
        for foreground, background, label in (
            ("text-secondary", "title-bar-bg", "toolbar secondary text"),
            ("text-default", "tool-window-bg", "tool-window text"),
            ("text-over-accent", "selection-bg-active", "selected text"),
            ("text-default", "selection-bg-inactive", "inactive selected text"),
            ("text-default", "dialog-bg", "dialog text"),
            ("text-default", "popup-bg", "popup text"),
            ("text-default", "tab-selected-bg-active", "selected tab text"),
            ("text-default", "control-bg", "button text"),
            ("text-over-accent", "control-brand-bg", "default button text"),
            ("text-error", "dialog-bg", "error text"),
            ("text-warning", "dialog-bg", "warning text"),
            ("text-success", "dialog-bg", "success text"),
        ):
            ratio = contrast(theme["colors"][foreground], theme["colors"][background])
            if ratio < 4.5:
                raise SystemExit(
                    "%s: %s contrast is %.2f:1" %
                    (scheme["name"], label, ratio))


def main():
    validate()
    THEMES.mkdir(parents=True, exist_ok=True)
    COLOR_SCHEMES.mkdir(parents=True, exist_ok=True)
    IMPORTABLE_SCHEMES.mkdir(parents=True, exist_ok=True)

    resources = {"META-INF/plugin.xml": build_plugin_xml()}
    (PLUGIN / "META-INF").mkdir(parents=True, exist_ok=True)
    (PLUGIN / "META-INF" / "plugin.xml").write_text(
        resources["META-INF/plugin.xml"], encoding="utf-8")

    for scheme in SCHEMES:
        file_slug = slug(scheme["name"])
        editor_xml = build_editor_scheme(scheme)
        theme_json = json.dumps(build_theme(scheme), indent=2) + "\n"

        editor_path = COLOR_SCHEMES / (file_slug + ".xml")
        importable_path = IMPORTABLE_SCHEMES / (theme_name(scheme) + ".icls")
        theme_path = THEMES / (file_slug + ".theme.json")
        editor_path.write_text(editor_xml, encoding="utf-8")
        importable_path.write_text(editor_xml, encoding="utf-8")
        theme_path.write_text(theme_json, encoding="utf-8")

        resources["colorSchemes/%s.xml" % file_slug] = editor_xml
        resources["themes/%s.theme.json" % file_slug] = theme_json
        print("wrote %-26s JetBrains editor scheme and Islands theme" % theme_name(scheme))

    jar_path, zip_path = build_archives(resources)
    print("wrote %s" % jar_path)
    print("wrote %s" % zip_path)


if __name__ == "__main__":
    main()
