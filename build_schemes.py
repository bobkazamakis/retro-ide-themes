#!/usr/bin/env python3
"""Generate eighteen retro IDE Sublime Text color schemes from one canonical rule set.

Every scheme gets the SAME rule list (same names, same scopes, same order).
Only the colors and the font styles change, through per-scheme role palettes.
"""

import os

# The Sublime Text schemes go in the "sublime" folder beside this script.
# The Xcode themes go in "xcode"; build_xcode_themes.py writes those.
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sublime")
AUTHOR = "Retro IDE Themes"

# --------------------------------------------------------------------------
# Canonical rule set. Each entry: (group, name, scope, fg_role, bg_role, style_role)
# style_role is a key into the per-scheme "styles" dict; None means no font_style.
# --------------------------------------------------------------------------

RULES = [
    # ---------- Comments ----------
    ("Comments", "Comment",
     "comment, punctuation.definition.comment",
     "comment", None, "comment"),
    ("Comments", "Documentation comment",
     "comment.block.documentation, comment.line.documentation, "
     "comment.block.documentation.swift, comment.line.documentation.swift",
     "doc", None, "doc"),
    ("Comments", "Documentation keyword (- Parameter, - Returns)",
     "comment keyword, comment.block.documentation keyword, "
     "comment.block.documentation variable.parameter, comment entity.name, "
     "comment markup.bold",
     "doc_key", None, "doc_key"),
    ("Comments", "TODO / FIXME / MARK",
     "comment keyword.codetag, comment keyword.other.mark, "
     "comment keyword.other.documentation, "
     "comment.line.double-slash keyword.codetag, keyword.codetag",
     "codetag", None, "codetag"),
    ("Comments", "Shebang",
     "comment.line.number-sign.shebang, punctuation.definition.comment.shebang",
     "preproc", None, None),

    # ---------- Strings ----------
    ("Strings", "String",
     "string, string.quoted, string.quoted.single, string.quoted.double, "
     "punctuation.definition.string, punctuation.definition.string.begin, "
     "punctuation.definition.string.end",
     "string", None, None),
    ("Strings", "Raw and multiline string",
     "string.quoted.other, string.quoted.raw, string.quoted.triple, "
     "string.unquoted, meta.string.raw, "
     "punctuation.definition.string.begin.raw, punctuation.definition.string.end.raw",
     "string_raw", None, None),
    ("Strings", "Character literal",
     "constant.character, constant.character.literal, string.quoted.single.char",
     "char", None, None),
    ("Strings", "Character escape",
     "constant.character.escape, constant.character.escape.swift, "
     "constant.character.escape.unicode.swift, constant.character.entity",
     "escape", None, None),
    ("Strings", "String interpolation punctuation",
     "punctuation.section.interpolation, punctuation.section.interpolation.begin, "
     "punctuation.section.interpolation.end, punctuation.definition.interpolation, "
     "punctuation.section.embedded, punctuation.section.embedded.begin, "
     "punctuation.section.embedded.end",
     "interp_punct", None, None),
    ("Strings", "Code inside string interpolation",
     "meta.interpolation, meta.interpolation.swift, meta.embedded.line",
     "interp_fg", "interp_bg", None),
    ("Strings", "Regular expression",
     "string.regexp, string.regexp.classic",
     "regexp", None, None),
    ("Strings", "Regular expression operators and classes",
     "string.regexp keyword.operator, string.regexp punctuation.definition.group, "
     "string.regexp punctuation.definition.character-class, "
     "constant.other.character-class",
     "regexp_op", None, None),

    # ---------- Numbers and constants ----------
    ("Numbers and constants", "Number",
     "constant.numeric, constant.numeric.integer, constant.numeric.float, "
     "constant.numeric.hex, constant.numeric.binary, constant.numeric.octal, "
     "constant.numeric.value.swift, meta.number",
     "number", None, None),
    ("Numbers and constants", "Number unit and suffix",
     "constant.numeric.suffix, keyword.other.unit",
     "number", None, None),
    ("Numbers and constants", "Language constant (true, false, nil)",
     "constant.language, constant.language.boolean, constant.language.boolean.swift, "
     "constant.language.null, constant.language.null.swift, constant.language.nil",
     "const_lang", None, "const_lang"),
    ("Numbers and constants", "Other constant",
     "constant.other, constant.other.caps, constant.other.placeholder.swift, "
     "variable.other.constant, entity.name.constant, support.constant",
     "const_other", None, None),
    ("Numbers and constants", "Enum case member (.someCase)",
     "variable.other.enummember, constant.other.enum, "
     "meta.function-call.swift variable.other.enummember, "
     "meta.path.swift variable.other.constant",
     "enum_member", None, None),
    ("Numbers and constants", "Color literal",
     "constant.other.color, constant.other.color.rgb-value",
     "const_other", None, None),

    # ---------- Keywords ----------
    ("Keywords", "Keyword",
     "keyword, keyword.other, keyword.declaration",
     "keyword", None, "keyword"),
    ("Keywords", "Control keyword (if, guard, for, return, throw)",
     "keyword.control, keyword.control.swift, keyword.control.flow, "
     "keyword.control.transfer, keyword.control.conditional, keyword.control.loop, "
     "keyword.control.exception",
     "keyword_control", None, "keyword"),
    ("Keywords", "Import keyword",
     "keyword.control.import, keyword.control.import.swift, keyword.other.import, "
     "keyword.control.at-rule.import",
     "keyword", None, "keyword"),
    ("Keywords", "Module and namespace name",
     "support.module, support.module.swift, support.module.system.swift, "
     "meta.import support.other, entity.name.namespace, meta.namespace entity.name",
     "module", None, None),
    ("Keywords", "Storage type (func, class, struct, enum, protocol, var, let)",
     "storage, storage.type, storage.type.swift, storage.type.function, "
     "storage.type.class, storage.type.struct, storage.type.enum, "
     "storage.type.protocol, storage.type.extension",
     "storage_type", None, "keyword"),
    ("Keywords", "Storage modifier (public, static, final, mutating, async, throws, weak)",
     "storage.modifier, storage.modifier.swift, storage.modifier.access, "
     "storage.modifier.lifetime, keyword.other.async, keyword.control.throws, "
     "keyword.other.declaration-specifier",
     "storage_mod", None, "keyword"),
    ("Keywords", "Language variable (self, Self, super, this)",
     "variable.language, variable.language.swift, variable.language.this, "
     "storage.type.self.swift, keyword.other.self",
     "self", None, "self"),
    ("Keywords", "Operator keyword (as, is, in, try, await, some, any)",
     "keyword.operator.word, keyword.operator.type, keyword.operator.cast, "
     "keyword.operator.expression, keyword.other.in, keyword.other.some, "
     "keyword.other.any",
     "operator_word", None, "keyword"),
    ("Keywords", "Operator",
     "keyword.operator, keyword.operator.arithmetic, keyword.operator.comparison, "
     "keyword.operator.logical, keyword.operator.bitwise, keyword.operator.assignment, "
     "keyword.operator.optional, keyword.operator.range, "
     "keyword.operator.ternary-conditional.swift",
     "operator", None, None),
    ("Keywords", "Custom operator declaration",
     "meta.declaration.operator.swift entity.name, meta.operator entity.name, "
     "keyword.declaration.operator, keyword.declaration.operator.swift",
     "operator_decl", None, "operator_decl"),

    # ---------- Compiler directives and attributes ----------
    ("Compiler directives and attributes",
     "Compiler directive ({$IFDEF}, #if, #available, #selector)",
     "meta.preprocessor, meta.preprocessor.swift, keyword.control.directive, "
     "keyword.other.preprocessor, keyword.control.import.include, "
     "punctuation.definition.keyword.swift, "
     "support.function.preprocessor.platform-condition.swift, text.preprocessor.swift",
     "preproc", None, "preproc"),
    ("Compiler directives and attributes", "Inactive preprocessor block",
     "comment.block.preprocessor, meta.preprocessor.inactive, meta.disabled",
     "preproc_inactive", None, None),
    ("Compiler directives and attributes", "Directive condition value (os, arch)",
     "constant.language.preprocessor.architecture.swift, "
     "constant.language.preprocessor.environment.swift, "
     "constant.language.preprocessor.operating-system.swift, "
     "constant.language.preprocessor.wildcard.swift",
     "directive_value", None, None),
    ("Compiler directives and attributes", "Attribute (@available, @objc, @MainActor)",
     "meta.annotation, meta.attribute, storage.type.annotation, variable.annotation, "
     "punctuation.definition.annotation, punctuation.definition.annotation.begin.swift, "
     "punctuation.definition.annotation.end.swift, support.function.annotation.swift, "
     "support.function.annotation.underscored.swift, variable.function.annotation.swift, "
     "meta.annotation.identifier.swift",
     "attribute", None, "attribute"),
    ("Compiler directives and attributes", "Property wrapper name (@State, @Binding)",
     "meta.annotation entity.name, meta.attribute entity.name.type, "
     "meta.annotation.swift support.type",
     "attribute", None, "attribute"),
    ("Compiler directives and attributes", "Attribute option",
     "constant.language.attribute-option.swift, meta.annotation.parameters.swift, "
     "meta.attribute variable.parameter",
     "attr_option", None, None),

    # ---------- Types ----------
    ("Types", "Type declaration name",
     "entity.name.type, entity.name.class, entity.name.struct, entity.name.enum, "
     "entity.name.protocol, entity.name.interface, entity.name.actor, "
     "entity.name.actor.swift, entity.name.class.swift, entity.name.struct.swift, "
     "entity.name.enum.swift, entity.name.protocol.swift, "
     "entity.name.x.extension.swift",
     "type", None, "type"),
    ("Types", "Type reference and library type",
     "support.type, support.class, support.class.swift, support.class.type, "
     "support.class.cocoa.swift, support.type.class.foundation.swift, "
     "support.type.struct.standard-library.swift, support.type.struct.foundation.swift, "
     "support.type.enum.standard-library.swift, support.type.enum.foundation.swift, "
     "support.type.protocol.standard-library.swift, "
     "support.type.protocol.foundation.swift, "
     "support.type.typealias.standard-library.swift, "
     "support.type.typealias.foundation.swift, support.other.swift, "
     "entity.other.inherited-class, storage.type.primitive",
     "type_lib", None, "type"),
    ("Types", "Type alias and associated type",
     "entity.name.type.alias, entity.name.type.associatedtype, "
     "entity.name.typealias.swift",
     "type_alias", None, "type"),
    ("Types", "Generic parameter",
     "variable.parameter.generic, meta.generic entity.name.type, "
     "meta.generic.declaration entity.name.type, meta.generic.swift support.other.swift, "
     "punctuation.definition.generic, punctuation.definition.generic.begin, "
     "punctuation.definition.generic.end.swift",
     "generic", None, None),
    ("Types", "Type punctuation (optional ?, force !)",
     "punctuation.definition.optional, keyword.operator.optional-type",
     "type_punct", None, None),

    # ---------- Functions ----------
    ("Functions", "Global or free function declaration",
     "entity.name.function, entity.name.function.swift, "
     "meta.function.declaration entity.name, meta.entity.name.function.swift, "
     "meta.entity.name.subscript.swift",
     "func_global_decl", None, "func_decl"),
    ("Functions", "Member function or method declaration",
     "entity.name.method, entity.name.function.member, "
     "entity.name.function.member.static, meta.method.declaration entity.name",
     "func_member_decl", None, "func_decl"),
    ("Functions", "Global or free function call",
     "variable.function, variable.function.custom-dot-operator.swift, "
     "meta.function-call entity.name.function, support.function, "
     "support.function.standard-library.swift, support.function.foundation.swift, "
     "support.function.cocoa.swift, support.function.objc.swift",
     "func_global_call", None, "func_call"),
    ("Functions", "Member function or method call",
     "variable.function.method, variable.function.member, support.function.method, "
     "meta.method-call variable.function, entity.name.function.operator.member",
     "func_member_call", None, "func_call"),
    ("Functions", "Built-in function (print, min, max)",
     "support.function.builtin, support.function.any-method",
     "func_builtin", None, "func_call"),
    ("Functions", "Argument label",
     "variable.parameter.function-call, meta.function-call variable.parameter",
     "arg_label", None, None),
    ("Functions", "Parameter declaration",
     "variable.parameter, variable.parameter.swift, variable.parameter.function, "
     "meta.function.parameters variable.parameter",
     "param", None, "param"),
    ("Functions", "Initializer and deinitializer",
     "keyword.declaration.function.constructor, storage.type.function.constructor, "
     "entity.name.function.constructor, entity.name.function.destructor, "
     "meta.entity.name.init.swift",
     "init", None, "init"),
    ("Functions", "Subscript and accessor (get, set, willSet, didSet)",
     "keyword.other.accessor, storage.type.accessor, keyword.other.subscript",
     "accessor", None, "keyword"),
    ("Functions", "Wildcard and shorthand argument ($0, _)",
     "variable.language.anonymous, variable.language.wildcard.swift, "
     "variable.parameter.shorthand, variable.other.positional, "
     "variable.other.shorthand-argument.swift",
     "shorthand", None, None),

    # ---------- Variables ----------
    ("Variables", "Variable",
     "variable, variable.other, variable.other.swift, variable.other.readwrite, "
     "variable.other.tuple.swift",
     "var_local", None, None),
    ("Variables", "Declared variable and property name",
     "meta.definition.variable entity.name, variable.other.declaration, "
     "meta.entity.name.var.swift, meta.entity.name.let.swift",
     "var_local", None, None),
    ("Variables", "Member access (property)",
     "variable.other.member, variable.other.property, variable.other.object.property, "
     "variable.other.instance, variable.other.field, meta.path variable.other",
     "member", None, None),
    ("Variables", "Environment and global variable",
     "variable.other.env, variable.other.global, variable.other.predefined, "
     "punctuation.definition.variable",
     "var_global", None, None),

    # ---------- Other languages: C, Python, JavaScript, Go, Rust, shell, SQL ----------
    ("Other language features", "Macro name (C, C++, Rust)",
     "entity.name.constant.preprocessor, entity.name.function.preprocessor, "
     "entity.name.function.macro, meta.preprocessor.macro entity.name, "
     "support.function.macro",
     "macro", None, "preproc"),
    ("Other language features", "Package and namespace declaration (Go, Java, C#)",
     "entity.name.package, meta.namespace.declaration entity.name, "
     "support.other.namespace",
     "module", None, None),
    ("Other language features", "Decorator (Python, JavaScript, Angular)",
     "meta.function.decorator, meta.function.decorator variable.function, "
     "punctuation.definition.decorator, entity.name.function.decorator",
     "attribute", None, "attribute"),
    ("Other language features", "Format specifier and placeholder (printf, f-string)",
     "constant.other.placeholder, meta.format.brace, meta.format.percent, "
     "constant.other.format-spec",
     "escape", None, None),
    ("Other language features", "Command-line option (shell, make)",
     "variable.parameter.option, constant.other.option, "
     "meta.function-call.arguments variable.parameter.option",
     "const_other", None, None),
    ("Other language features", "Built-in class and library object (JavaScript, Python)",
     "support.class.builtin, support.type.exception, support.type.python, "
     "support.class.library, support.other.class",
     "type_lib", None, "type"),
    ("Other language features", "SQL and query keyword",
     "keyword.other.DML, keyword.other.DDL, keyword.other.create, "
     "keyword.other.alias.sql, storage.type.sql",
     "keyword", None, "keyword"),
    ("Other language features", "Lifetime and reference (Rust, C++)",
     "storage.modifier.lifetime.rust, entity.name.lifetime, "
     "keyword.operator.reference, keyword.operator.dereference",
     "storage_mod", None, None),
    ("Other language features", "Type hint and annotation separator (Python, TypeScript)",
     "meta.annotation.type, punctuation.separator.annotation.python, "
     "punctuation.separator.type, keyword.operator.type.annotation",
     "type_punct", None, None),

    # ---------- Punctuation and structure ----------
    ("Punctuation and structure", "Punctuation",
     "punctuation.separator, punctuation.terminator, punctuation.accessor, "
     "punctuation.accessor.dot.swift, punctuation.separator.annotation.swift, "
     "punctuation.separator.annotation.type-annotation.swift, "
     "punctuation.separator.annotation.conformance.swift, "
     "punctuation.separator.annotation.conformance-or-inheritance.swift, "
     "punctuation.separator.annotation.return-arrow.swift, "
     "punctuation.separator.key-value.swift",
     "punct", None, None),
    ("Punctuation and structure", "Braces, brackets, parentheses",
     "punctuation.section.block, punctuation.section.brackets, "
     "punctuation.section.parens, punctuation.section.group, "
     "punctuation.section.braces, punctuation.section.mapping, "
     "punctuation.section.sequence",
     "brace", None, None),
    ("Punctuation and structure", "Line continuation",
     "punctuation.separator.continuation, punctuation.separator.continuation.line.swift",
     "continuation", None, None),
    ("Punctuation and structure", "Label and case pattern",
     "entity.name.label, meta.label",
     "label", None, None),
    ("Punctuation and structure", "Invalid",
     "invalid, invalid.illegal, invalid.swift, invalid.illegal.swift",
     "invalid_fg", "invalid_bg", None),
    ("Punctuation and structure", "Deprecated",
     "invalid.deprecated",
     "invalid_fg", "deprecated_bg", None),
    ("Punctuation and structure", "Error message",
     "message.error, markup.error",
     "reg_red", None, None),
    ("Punctuation and structure", "Warning message",
     "message.warning, markup.warning",
     "reg_yellow", None, None),
    ("Punctuation and structure", "Info message",
     "message.info, markup.info",
     "reg_blue", None, None),

    # ---------- Markup ----------
    ("Markup (Markdown and docs)", "Markup heading",
     "markup.heading, entity.name.section, punctuation.definition.heading",
     "head", None, "head"),
    ("Markup (Markdown and docs)", "Markup bold",
     "markup.bold, punctuation.definition.bold",
     "bold", None, "bold"),
    ("Markup (Markdown and docs)", "Markup italic",
     "markup.italic, punctuation.definition.italic",
     "italic", None, "italic"),
    ("Markup (Markdown and docs)", "Markup bold italic",
     "markup.bold markup.italic, markup.italic markup.bold",
     "bold", None, "bold_italic"),
    ("Markup (Markdown and docs)", "Markup underline",
     "markup.underline",
     "link", None, "underline"),
    ("Markup (Markdown and docs)", "Markup strikethrough",
     "markup.strikethrough",
     "quote", None, None),
    ("Markup (Markdown and docs)", "Markup link",
     "markup.underline.link, string.other.link, meta.link",
     "link", None, "underline"),
    ("Markup (Markdown and docs)", "Markup raw / code",
     "markup.raw, markup.raw.inline, markup.raw.inline.swift, markup.raw.block, "
     "markup.raw.code-fence",
     "raw", "raw_bg", None),
    ("Markup (Markdown and docs)", "Markup list punctuation",
     "markup.list punctuation.definition.list_item, "
     "punctuation.definition.list_item.markdown",
     "list_punct", None, None),
    ("Markup (Markdown and docs)", "Markup quote",
     "markup.quote, punctuation.definition.blockquote",
     "quote", None, "quote"),
    ("Markup (Markdown and docs)", "Markup separator",
     "meta.separator, markup.separator",
     "list_punct", None, "bold"),

    # ---------- Diff ----------
    ("Diff", "Diff inserted",
     "markup.inserted",
     "diff_add_fg", "diff_add_bg", None),
    ("Diff", "Diff deleted",
     "markup.deleted",
     "diff_del_fg", "diff_del_bg", None),
    ("Diff", "Diff changed",
     "markup.changed",
     "diff_chg_fg", "diff_chg_bg", None),
    ("Diff", "Diff header",
     "meta.diff.header, meta.diff.header.from-file, meta.diff.header.to-file, "
     "meta.diff.index",
     "head", None, "bold"),
    ("Diff", "Diff range",
     "meta.diff.range, punctuation.definition.range.diff",
     "list_punct", None, None),

    # ---------- Data formats ----------
    ("Data formats (JSON, YAML, XML, plist, CSS)", "Object key",
     "meta.mapping.key string, meta.mapping.key, entity.name.tag.yaml, "
     "support.type.property-name, meta.property-name",
     "key", None, None),
    ("Data formats (JSON, YAML, XML, plist, CSS)", "Tag",
     "entity.name.tag, punctuation.definition.tag",
     "tag", None, "tag"),
    ("Data formats (JSON, YAML, XML, plist, CSS)", "Tag attribute",
     "entity.other.attribute-name.localname, meta.tag entity.other.attribute-name, "
     "entity.other.attribute-name",
     "tag_attr", None, None),
    ("Data formats (JSON, YAML, XML, plist, CSS)", "Doctype and processing instruction",
     "meta.tag.sgml.doctype, keyword.declaration.doctype, "
     "meta.tag.preprocessor, meta.tag.sgml",
     "preproc", None, None),
    # The class and id scopes stay behind "source.css". The HTML syntax gives
    # the same names to the class= and id= attributes of a tag, and those must
    # keep the tag-attribute color.
    ("Data formats (JSON, YAML, XML, plist, CSS)", "CSS selector",
     "entity.other.pseudo-class, entity.other.pseudo-element, "
     "source.css entity.other.attribute-name.class, "
     "source.css entity.other.attribute-name.id",
     "type", None, None),
    ("Data formats (JSON, YAML, XML, plist, CSS)", "YAML anchor and alias",
     "entity.name.other.alias, variable.other.alias, punctuation.definition.alias, "
     "entity.name.other.anchor",
     "const_other", None, None),

    # ---------- Plugin and diagnostic regions (SublimeLinter, LSP, Git) ----------
    ("Plugin and diagnostic regions", "Region redish",
     "region.redish", "reg_red", None, None),
    ("Plugin and diagnostic regions", "Region orangish",
     "region.orangish", "reg_orange", None, None),
    ("Plugin and diagnostic regions", "Region yellowish",
     "region.yellowish", "reg_yellow", None, None),
    ("Plugin and diagnostic regions", "Region greenish",
     "region.greenish", "reg_green", None, None),
    ("Plugin and diagnostic regions", "Region bluish",
     "region.bluish", "reg_blue", None, None),
    ("Plugin and diagnostic regions", "Region purplish",
     "region.purplish", "reg_purple", None, None),
    ("Plugin and diagnostic regions", "Region pinkish",
     "region.pinkish", "reg_pink", None, None),
]

# Globals template: (key, role-or-literal). A value in {braces} is a role name.
#
# A role with the value None makes the generator leave the global out. This is
# necessary for "selection_foreground": if a scheme sets it, Sublime draws all
# selected text in that one color, and the syntax colors go away while you
# select. Only the schemes with a dark selection bar set it, because dark blue
# under dark blue text is not readable. See g_sel_fg in each palette.
GLOBALS = [
    ("background", "{g_bg}"),
    ("foreground", "{g_fg}"),
    ("caret", "{g_caret}"),
    ("block_caret", "{g_block_caret}"),
    ("invisibles", "{g_invisibles}"),
    ("line_highlight", "{g_line_hl}"),
    ("selection", "{g_sel}"),
    ("selection_foreground", "{g_sel_fg}"),
    ("selection_border", "{g_sel_border}"),
    ("selection_border_width", "1"),
    ("inactive_selection", "{g_inactive_sel}"),
    ("inactive_selection_foreground", "{g_inactive_sel_fg}"),
    ("highlight", "{g_highlight}"),
    ("find_highlight", "{g_find}"),
    ("find_highlight_foreground", "{g_find_fg}"),
    ("gutter", "{g_gutter}"),
    ("gutter_foreground", "{g_gutter_fg}"),
    ("gutter_foreground_highlight", "{g_gutter_fg_hl}"),
    ("line_diff_width", "3"),
    ("line_diff_added", "{diff_add_fg}"),
    ("line_diff_modified", "{diff_chg_fg}"),
    ("line_diff_deleted", "{diff_del_fg}"),
    ("guide", "{g_guide}"),
    ("active_guide", "{g_active_guide}"),
    ("stack_guide", "{g_stack_guide}"),
    ("misspelling", "{reg_red}"),
    ("fold_marker", "{g_fold}"),
    ("shadow", "{g_shadow}"),
    ("shadow_width", "4"),
    ("accent", "{g_accent}"),
    ("brackets_options", "underline"),
    ("brackets_foreground", "{g_brackets}"),
    ("bracket_contents_options", "underline"),
    ("bracket_contents_foreground", "{g_brackets}"),
    ("tags_options", "stippled_underline"),
    ("tags_foreground", "{g_tags}"),
]

# --------------------------------------------------------------------------
# Per-scheme palettes
# --------------------------------------------------------------------------

VS2012_LIGHT = {
    "name": "Visual Studio 2012 Light",
    "note": "Visual Studio 2012 Light — blue directives, purple macros, teal types, and mostly plain identifiers",
    "colors": {
        # surfaces and interface
        "g_bg": "#FFFFFF", "g_fg": "#000000", "g_caret": "#000000",
        "g_block_caret": "#5C5C5C", "g_invisibles": "#DCDCD2",
        "g_line_hl": "#F2F6FB", "g_sel": "#CCE4F7", "g_sel_fg": None,
        "g_sel_border": "#A8CDEB", "g_inactive_sel": "#E4EFFA",
        "g_inactive_sel_fg": None, "g_highlight": "#D8B933",
        "g_find": "#FBEFA0", "g_find_fg": "#000000",
        "g_gutter_fg": "#8C8C82", "g_gutter_fg_hl": "#2B91AF",
        "g_guide": "#E6E6DE", "g_active_guide": "#B8CFE5",
        "g_stack_guide": "#EFEFE7", "g_fold": "#FBEFA0", "g_shadow": "#00000012",
        "g_accent": "#2B91AF", "g_brackets": "#1F6E88", "g_tags": "#1F6E88",
        # syntax
        "comment": "#008000", "doc": "#2A8C2A", "doc_key": "#3F7F5F",
        "codetag": "#2E7D32",
        "string": "#A31515", "string_raw": "#A31515", "char": "#8B1A1A",
        "escape": "#B5561B", "interp_punct": "#B5561B", "interp_fg": "#000000",
        "interp_bg": "#FDF5F3", "regexp": "#9B2D6F", "regexp_op": "#7A3E9D",
        "number": "#000000", "const_lang": "#0000FF", "const_other": "#000000",
        "enum_member": "#2F4F4F",
        "keyword": "#0000FF", "keyword_control": "#0000FF", "module": "#000000",
        "storage_type": "#0000FF", "storage_mod": "#0000FF", "self": "#0000FF",
        "operator_word": "#0000FF", "operator": "#000000", "operator_decl": "#008080",
        "preproc": "#0000FF", "macro": "#BD63C5", "preproc_inactive": "#7A7A7A",
        "directive_value": "#000000", "attribute": "#7A3E9D",
        "attr_option": "#9A6BB8",
        "type": "#2B91AF", "type_lib": "#2B91AF", "type_alias": "#2B91AF",
        "generic": "#1F6E88", "type_punct": "#2B91AF",
        "func_decl": "#000000", "func_call": "#000000", "func_builtin": "#000000",
        "arg_label": "#000000", "param": "#000000", "init": "#000000",
        "accessor": "#0000FF", "shorthand": "#000000",
        "var": "#000000", "var_decl": "#000000", "member": "#000000", "var_project": "#000000",
        "punct": "#000000", "brace": "#000000", "continuation": "#82827A",
        "label": "#000000", "invalid_fg": "#FFFFFF", "invalid_bg": "#C0392B",
        "deprecated_bg": "#7A3E9D",
        "head": "#00007F", "bold": "#000000", "italic": "#000000",
        "link": "#1F6E88", "raw": "#A31515", "raw_bg": "#F7F7F4",
        "list_punct": "#2B91AF", "quote": "#404040",
        "diff_add_fg": "#0B6B33", "diff_add_bg": "#EAF7EE",
        "diff_del_fg": "#9B1C1C", "diff_del_bg": "#FDECEC",
        "diff_chg_fg": "#8A5A00", "diff_chg_bg": "#FCF6E3",
        "key": "#1F6E88", "tag": "#00007F", "tag_attr": "#C0392B",
        "reg_red": "#C0392B", "reg_orange": "#B8860B", "reg_yellow": "#8A6D00",
        "reg_green": "#2E8B57", "reg_blue": "#2B91AF", "reg_purple": "#7A3E9D",
        "reg_pink": "#9B2D6F",
    },
    "styles": {
        "comment": "italic", "doc": "italic", "doc_key": "bold italic",
        "codetag": "bold italic", "keyword": None, "self": "italic",
        "const_lang": None, "operator_decl": None, "preproc": None,
        "attribute": None, "type": None, "func_decl": None, "func_call": None,
        "param": "italic", "init": None, "head": "bold", "bold": "bold",
        "italic": "italic", "bold_italic": "bold italic", "underline": "underline",
        "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #FFFFFF; color: #000000; "
             "border: 1px solid #B8CFE5; } a { color: #1F6E88; }",
}

DELPHI = {
    "name": "Delphi Classic",
    "note": "Delphi 7 code editor — white paper, black bold reserved words, navy italic comments",
    "colors": {
        "g_bg": "#FFFFFF", "g_fg": "#000000", "g_caret": "#000000",
        "g_block_caret": "#4A4A56", "g_invisibles": "#D8DCE4",
        "g_line_hl": "#F4F8FD", "g_sel": "#CBDFF7", "g_sel_fg": None,
        "g_sel_border": "#A6C6E8", "g_inactive_sel": "#E6EEF9",
        "g_inactive_sel_fg": None, "g_highlight": "#D4B22E",
        "g_find": "#FCF0A8", "g_find_fg": "#000000",
        "g_gutter_fg": "#8A8A94", "g_gutter_fg_hl": "#000080",
        "g_guide": "#E4E8EE", "g_active_guide": "#AFC6E0",
        "g_stack_guide": "#ECEFF4", "g_fold": "#FCF0A8", "g_shadow": "#00000012",
        "g_accent": "#000080", "g_brackets": "#000080", "g_tags": "#000080",
        "comment": "#000080", "doc": "#2A3F80", "doc_key": "#000080",
        "codetag": "#000080",
        "string": "#0000FF", "string_raw": "#0000FF", "char": "#0000C0",
        "escape": "#7A3E9D", "interp_punct": "#7A3E9D", "interp_fg": "#000000",
        "interp_bg": "#F3F5FD", "regexp": "#9B2D6F", "regexp_op": "#7A3E9D",
        "number": "#C05000", "const_lang": "#000000", "const_other": "#0B7A75",
        "enum_member": "#0B7A75",
        "keyword": "#000000", "keyword_control": "#000000", "module": "#0B7A75",
        "storage_type": "#000000", "storage_mod": "#000000", "self": "#000000",
        "operator_word": "#000000", "operator": "#000000", "operator_decl": "#000000",
        "preproc": "#008000", "preproc_inactive": "#7A7A7A",
        "directive_value": "#008000", "attribute": "#7A3E9D",
        "attr_option": "#9A6BB8",
        "type": "#0B7A75", "type_lib": "#0B7A75", "type_alias": "#0B7A75",
        "generic": "#0E5F73", "type_punct": "#0B7A75",
        "func_decl": "#7A3E9D", "func_call": "#7A3E9D", "func_builtin": "#7A3E9D",
        "arg_label": "#5A5A70", "param": "#3C3C46", "init": "#000000",
        "accessor": "#000000", "shorthand": "#0E5F73",
        "var": "#000000", "var_decl": "#000000", "member": "#000000", "var_project": "#6B4423",
        "punct": "#3C3C46", "brace": "#000000", "continuation": "#82828C",
        "label": "#000080", "invalid_fg": "#FFFFFF", "invalid_bg": "#C0392B",
        "deprecated_bg": "#7A3E9D",
        "head": "#000080", "bold": "#000000", "italic": "#000000",
        "link": "#000080", "raw": "#0000FF", "raw_bg": "#F6F7FA",
        "list_punct": "#0B7A75", "quote": "#3C3C46",
        "diff_add_fg": "#0B6B33", "diff_add_bg": "#EAF7EE",
        "diff_del_fg": "#9B1C1C", "diff_del_bg": "#FDECEC",
        "diff_chg_fg": "#8A5A00", "diff_chg_bg": "#FCF6E3",
        "key": "#0B7A75", "tag": "#000080", "tag_attr": "#800000",
        "reg_red": "#C0392B", "reg_orange": "#C05000", "reg_yellow": "#8A6D00",
        "reg_green": "#2E8B57", "reg_blue": "#000080", "reg_purple": "#7A3E9D",
        "reg_pink": "#9B2D6F",
    },
    "styles": {
        # Delphi bolded reserved words only. Color carries everything else.
        "comment": "italic", "doc": "italic", "doc_key": "bold italic",
        "codetag": "bold italic", "keyword": "bold", "self": "bold italic",
        "const_lang": None, "operator_decl": None, "preproc": None,
        "attribute": None, "type": None, "func_decl": None, "func_call": None,
        "param": "italic", "init": None, "head": "bold", "bold": "bold",
        "italic": "italic", "bold_italic": "bold italic", "underline": "underline",
        "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #FFFFFF; color: #000000; "
             "border: 1px solid #AFC6E0; } a { color: #000080; }",
}

TP = {
    "name": "Turbo Pascal",
    "note": "Borland DOS IDE — blue paper, yellow text, EGA 16-color palette",
    "colors": {
        "g_bg": "#0000A8", "g_fg": "#FCFC54", "g_caret": "#FCFCFC",
        "g_block_caret": "#54FCFC", "g_invisibles": "#3C3CC8",
        "g_line_hl": "#0808B8", "g_sel": "#00A8A8", "g_sel_fg": "#000000",
        "g_sel_border": "#54FCFC", "g_inactive_sel": "#1C1CB8",
        "g_inactive_sel_fg": "#FCFC54", "g_highlight": "#FCFC54",
        "g_find": "#A8A800", "g_find_fg": "#FCFCFC",
        "g_gutter_fg": "#7C7CE0", "g_gutter_fg_hl": "#54FCFC",
        "g_guide": "#2020B4", "g_active_guide": "#54FCFC",
        "g_stack_guide": "#1818AC", "g_fold": "#54FCFC", "g_shadow": "#00003080",
        "g_accent": "#54FCFC", "g_brackets": "#54FCFC", "g_tags": "#54FCFC",
        "comment": "#A8A8A8", "doc": "#A8A8A8", "doc_key": "#FCFCFC",
        "codetag": "#FCFCFC",
        "string": "#54FC54", "string_raw": "#54FC54", "char": "#54FC54",
        "escape": "#FC5454", "interp_punct": "#FC5454", "interp_fg": "#FCFC54",
        "interp_bg": "#0D0DB4", "regexp": "#FC54FC", "regexp_op": "#FCFCFC",
        "number": "#FC54FC", "const_lang": "#FCFCFC", "const_other": "#FC54FC",
        "enum_member": "#FC54FC",
        "keyword": "#FCFCFC", "keyword_control": "#FCFCFC", "module": "#54FCFC",
        "storage_type": "#FCFCFC", "storage_mod": "#FCFCFC", "self": "#FCFCFC",
        "operator_word": "#FCFCFC", "operator": "#FCFCFC", "operator_decl": "#FCFCFC",
        "preproc": "#FC5454", "preproc_inactive": "#6C6CD8",
        "directive_value": "#FC5454", "attribute": "#FC5454",
        "attr_option": "#FC5454",
        "type": "#54FCFC", "type_lib": "#54FCFC", "type_alias": "#54FCFC",
        "generic": "#54FCFC", "type_punct": "#54FCFC",
        "func_decl": "#FCFC54", "func_call": "#FCFC54", "func_builtin": "#FCFC54",
        "arg_label": "#FCFC54", "param": "#FCFC54", "init": "#FCFCFC",
        "accessor": "#FCFCFC", "shorthand": "#54FCFC",
        "var": "#FCFC54", "var_decl": "#FCFC54", "member": "#FCFC54", "var_project": "#FCFC54",
        "punct": "#54FCFC", "brace": "#FCFCFC", "continuation": "#A8A8A8",
        "label": "#54FCFC", "invalid_fg": "#FCFCFC", "invalid_bg": "#A80000",
        "deprecated_bg": "#A800A8",
        "head": "#FCFCFC", "bold": "#FCFCFC", "italic": "#FCFC54",
        "link": "#54FCFC", "raw": "#54FC54", "raw_bg": "#000090",
        "list_punct": "#54FCFC", "quote": "#A8A8A8",
        "diff_add_fg": "#54FC54", "diff_add_bg": "#004C00",
        "diff_del_fg": "#FC5454", "diff_del_bg": "#600000",
        "diff_chg_fg": "#FCFC54", "diff_chg_bg": "#5A5A00",
        "key": "#54FCFC", "tag": "#FCFCFC", "tag_attr": "#54FCFC",
        "reg_red": "#FC5454", "reg_orange": "#A85400", "reg_yellow": "#FCFC54",
        "reg_green": "#54FC54", "reg_blue": "#54FCFC", "reg_purple": "#FC54FC",
        "reg_pink": "#FC54FC",
    },
    "styles": {
        # The DOS IDE had no bold. Bright EGA colors did the work.
        "comment": "italic", "doc": "italic", "doc_key": "bold italic",
        "codetag": "bold italic", "keyword": None, "self": "italic",
        "const_lang": None, "operator_decl": None, "preproc": None,
        "attribute": None, "type": None, "func_decl": None,
        "func_call": None, "param": "italic", "init": None, "head": "bold",
        "bold": "bold", "italic": "italic", "bold_italic": "bold italic",
        "underline": "underline", "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #0000A8; color: #FCFC54; "
             "border: 1px solid #54FCFC; } a { color: #54FCFC; }",
}

TCPP = {
    "name": "Turbo C++ 3.0",
    "note": "Turbo C++ 3.0 for DOS — Borland's blue EGA shell, flat identifiers, red preprocessor",
    "colors": {
        # Same Borland DOS shell as Turbo Pascal, same EGA 16-color palette.
        "g_bg": "#0000A8", "g_fg": "#FCFC54", "g_caret": "#FCFCFC",
        "g_block_caret": "#54FCFC", "g_invisibles": "#3C3CC8",
        "g_line_hl": "#0808B8", "g_sel": "#00A8A8", "g_sel_fg": "#000000",
        "g_sel_border": "#54FCFC", "g_inactive_sel": "#1C1CB8",
        "g_inactive_sel_fg": "#FCFC54", "g_highlight": "#FCFC54",
        "g_find": "#A8A800", "g_find_fg": "#FCFCFC",
        "g_gutter_fg": "#7C7CE0", "g_gutter_fg_hl": "#54FCFC",
        "g_guide": "#2020B4", "g_active_guide": "#54FCFC",
        "g_stack_guide": "#1818AC", "g_fold": "#54FCFC", "g_shadow": "#00003080",
        "g_accent": "#54FCFC", "g_brackets": "#54FCFC", "g_tags": "#54FCFC",
        "comment": "#A8A8A8", "doc": "#A8A8A8", "doc_key": "#FCFCFC",
        "codetag": "#FCFCFC",
        "string": "#54FC54", "string_raw": "#54FC54", "char": "#54FC54",
        "escape": "#FC5454", "interp_punct": "#FC5454", "interp_fg": "#FCFC54",
        "interp_bg": "#0D0DB4", "regexp": "#FC54FC", "regexp_op": "#FCFCFC",
        "number": "#FC54FC", "const_lang": "#FCFCFC", "const_other": "#FC54FC",
        "enum_member": "#FC54FC",
        "keyword": "#FCFCFC", "keyword_control": "#FCFCFC", "module": "#FCFC54",
        "storage_type": "#FCFCFC", "storage_mod": "#FCFCFC", "self": "#FCFCFC",
        "operator_word": "#FCFCFC", "operator": "#FCFCFC", "operator_decl": "#FCFCFC",
        "preproc": "#FC5454", "preproc_inactive": "#6C6CD8",
        "directive_value": "#FC5454", "attribute": "#FC5454",
        "attr_option": "#FC5454",
        # The old lexer could not tell a type name from a variable name, the
        # same limit that keeps Visual C++ 6 and CodeWarrior flat in this repo.
        "type": "#FCFC54", "type_lib": "#FCFC54", "type_alias": "#FCFC54",
        "generic": "#FCFC54", "type_punct": "#FCFCFC",
        "func_decl": "#FCFC54", "func_call": "#FCFC54", "func_builtin": "#FCFC54",
        "arg_label": "#FCFC54", "param": "#FCFC54", "init": "#FCFC54",
        "accessor": "#FCFCFC", "shorthand": "#FCFC54",
        "var": "#FCFC54", "var_decl": "#FCFC54", "member": "#FCFC54", "var_project": "#FCFC54",
        "punct": "#FCFCFC", "brace": "#FCFCFC", "continuation": "#A8A8A8",
        "label": "#FCFC54", "invalid_fg": "#FCFCFC", "invalid_bg": "#A80000",
        "deprecated_bg": "#A800A8",
        "head": "#FCFCFC", "bold": "#FCFCFC", "italic": "#FCFC54",
        "link": "#54FCFC", "raw": "#54FC54", "raw_bg": "#000090",
        "list_punct": "#54FCFC", "quote": "#A8A8A8",
        "diff_add_fg": "#54FC54", "diff_add_bg": "#004C00",
        "diff_del_fg": "#FC5454", "diff_del_bg": "#600000",
        "diff_chg_fg": "#FCFC54", "diff_chg_bg": "#5A5A00",
        "key": "#54FCFC", "tag": "#FCFCFC", "tag_attr": "#54FCFC",
        "reg_red": "#FC5454", "reg_orange": "#A85400", "reg_yellow": "#FCFC54",
        "reg_green": "#54FC54", "reg_blue": "#54FCFC", "reg_purple": "#FC54FC",
        "reg_pink": "#FC54FC",
    },
    "styles": {
        # The DOS IDE had no bold. Bright EGA colors did the work.
        "comment": "italic", "doc": "italic", "doc_key": "bold italic",
        "codetag": "bold italic", "keyword": None, "self": "italic",
        "const_lang": None, "operator_decl": None, "preproc": None,
        "attribute": None, "type": None, "func_decl": None,
        "func_call": None, "param": "italic", "init": None, "head": "bold",
        "bold": "bold", "italic": "italic", "bold_italic": "bold italic",
        "underline": "underline", "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #0000A8; color: #FCFC54; "
             "border: 1px solid #54FCFC; } a { color: #54FCFC; }",
}

XCODE = {
    "name": "Xcode Classic",
    "note": "Xcode 3 / Project Builder — white paper, magenta keywords, brick strings, teal types",
    "colors": {
        "g_bg": "#FFFFFF", "g_fg": "#000000", "g_caret": "#000000",
        "g_block_caret": "#5A5A5A", "g_invisibles": "#D6D6D6",
        "g_line_hl": "#ECF5FF", "g_sel": "#B3D7FF", "g_sel_fg": None,
        "g_sel_border": "#8FC1F5", "g_inactive_sel": "#DCE9F7",
        "g_inactive_sel_fg": None, "g_highlight": "#E0C240",
        "g_find": "#FDF2A0", "g_find_fg": "#000000",
        "g_gutter_fg": "#9A9A9A", "g_gutter_fg_hl": "#3F6E75",
        "g_guide": "#E8E8E8", "g_active_guide": "#B8CFE5",
        "g_stack_guide": "#F0F0F0", "g_fold": "#FDF2A0", "g_shadow": "#00000012",
        "g_accent": "#AA0D91", "g_brackets": "#3F6E75", "g_tags": "#3F6E75",
        "comment": "#007400", "doc": "#007400", "doc_key": "#005C00",
        "codetag": "#005C00",
        "string": "#C41A16", "string_raw": "#C41A16", "char": "#1C00CF",
        "escape": "#1C00CF", "interp_punct": "#643820", "interp_fg": "#000000",
        "interp_bg": "#FAF7F7", "regexp": "#C41A16", "regexp_op": "#643820",
        "number": "#1C00CF", "const_lang": "#AA0D91", "const_other": "#3900A0",
        "enum_member": "#3900A0",
        "keyword": "#AA0D91", "keyword_control": "#AA0D91", "module": "#3F6E75",
        "storage_type": "#AA0D91", "storage_mod": "#AA0D91", "self": "#AA0D91",
        "operator_word": "#AA0D91", "operator": "#000000", "operator_decl": "#3900A0",
        "preproc": "#643820", "preproc_inactive": "#7A7A7A",
        "directive_value": "#643820", "attribute": "#AA0D91",
        "attr_option": "#815F03",
        "type": "#3F6E75", "type_lib": "#3F6E75", "type_alias": "#3F6E75",
        "generic": "#5C787E", "type_punct": "#3F6E75",
        "func_decl": "#26474B", "func_call": "#3F6E75", "func_builtin": "#3F6E75",
        "arg_label": "#6C7A7D", "param": "#3D3D3D", "init": "#AA0D91",
        "accessor": "#AA0D91", "shorthand": "#3900A0",
        "var": "#000000", "var_decl": "#000000", "member": "#318495", "var_project": "#318495",
        "punct": "#000000", "brace": "#000000", "continuation": "#7A7A7A",
        "label": "#3900A0", "invalid_fg": "#FFFFFF", "invalid_bg": "#C0392B",
        "deprecated_bg": "#815F03",
        "head": "#AA0D91", "bold": "#000000", "italic": "#000000",
        "link": "#0E0EFF", "raw": "#C41A16", "raw_bg": "#F7F7F7",
        "list_punct": "#3F6E75", "quote": "#4F4F4F",
        "diff_add_fg": "#0B6B33", "diff_add_bg": "#EAF7EE",
        "diff_del_fg": "#9B1C1C", "diff_del_bg": "#FDECEC",
        "diff_chg_fg": "#8A5A00", "diff_chg_bg": "#FCF6E3",
        "key": "#3F6E75", "tag": "#AA0D91", "tag_attr": "#815F03",
        "reg_red": "#C0392B", "reg_orange": "#815F03", "reg_yellow": "#B8860B",
        "reg_green": "#007400", "reg_blue": "#3F6E75", "reg_purple": "#AA0D91",
        "reg_pink": "#C41A16",
    },
    "styles": {
        # Xcode drew all code in one weight, and it did not slant comments.
        "comment": None, "doc": None, "doc_key": "bold", "codetag": "bold",
        "keyword": None, "self": None, "const_lang": None,
        "operator_decl": None, "preproc": None, "attribute": None, "type": None,
        "func_decl": None, "func_call": None, "param": None, "init": None,
        "head": "bold", "bold": "bold", "italic": "italic",
        "bold_italic": "bold italic", "underline": "underline", "quote": "italic",
        "tag": None,
    },
    "popup": "html { background-color: #FFFFFF; color: #000000; "
             "border: 1px solid #B3D7FF; } a { color: #0E0EFF; }",
}

VB6 = {
    "name": "Visual Basic 6",
    "note": "VB6 code window — white paper, blue keywords, green comments, navy selection",
    "colors": {
        "g_bg": "#FFFFFF", "g_fg": "#000000", "g_caret": "#000000",
        "g_block_caret": "#555555", "g_invisibles": "#D4D0C8",
        "g_line_hl": "#F2F2F2", "g_sel": "#D4DAEC", "g_sel_fg": None,
        "g_sel_border": "#0A246A", "g_inactive_sel": "#DCDCDC",
        "g_inactive_sel_fg": None, "g_highlight": "#808000",
        "g_find": "#FFFF80", "g_find_fg": "#000000",
        "g_gutter_fg": "#808080", "g_gutter_fg_hl": "#000080",
        "g_guide": "#E4E4E0", "g_active_guide": "#B0B0C8",
        "g_stack_guide": "#EDEDE9", "g_fold": "#FFFF80", "g_shadow": "#00000014",
        "g_accent": "#0000FF", "g_brackets": "#000080", "g_tags": "#000080",
        "comment": "#008000", "doc": "#008000", "doc_key": "#006400",
        "codetag": "#006400",
        "string": "#800000", "string_raw": "#800000", "char": "#800000",
        "escape": "#B5561B", "interp_punct": "#B5561B", "interp_fg": "#000000",
        "interp_bg": "#FAF6F6", "regexp": "#800080", "regexp_op": "#B5561B",
        "number": "#800080", "const_lang": "#0000FF", "const_other": "#800080",
        "enum_member": "#800080",
        "keyword": "#0000FF", "keyword_control": "#0000FF", "module": "#000080",
        "storage_type": "#0000FF", "storage_mod": "#0000FF", "self": "#0000FF",
        "operator_word": "#0000FF", "operator": "#000000", "operator_decl": "#000080",
        "preproc": "#0000FF", "preproc_inactive": "#7A7A7A",
        "directive_value": "#0000FF", "attribute": "#800080",
        "attr_option": "#A050A0",
        "type": "#000080", "type_lib": "#000080", "type_alias": "#000080",
        "generic": "#003A6B", "type_punct": "#000080",
        "func_decl": "#000000", "func_call": "#000000", "func_builtin": "#0000FF",
        "arg_label": "#6A6A6A", "param": "#404040", "init": "#0000FF",
        "accessor": "#0000FF", "shorthand": "#000080",
        "var": "#000000", "var_decl": "#000000", "member": "#000000", "var_project": "#008080",
        "punct": "#000000", "brace": "#000000", "continuation": "#808080",
        "label": "#000080", "invalid_fg": "#FFFFFF", "invalid_bg": "#800000",
        "deprecated_bg": "#800080",
        "head": "#000080", "bold": "#000000", "italic": "#000000",
        "link": "#0000FF", "raw": "#800000", "raw_bg": "#F6F6F6",
        "list_punct": "#000080", "quote": "#404040",
        "diff_add_fg": "#008000", "diff_add_bg": "#E8F4E8",
        "diff_del_fg": "#800000", "diff_del_bg": "#F8EAEA",
        "diff_chg_fg": "#808000", "diff_chg_bg": "#F8F6E0",
        "key": "#000080", "tag": "#000080", "tag_attr": "#800000",
        "reg_red": "#FF0000", "reg_orange": "#B8860B", "reg_yellow": "#808000",
        "reg_green": "#008000", "reg_blue": "#0000FF", "reg_purple": "#800080",
        "reg_pink": "#800000",
    },
    "styles": {
        # VB6 draws every token in one weight. Only markup keeps emphasis.
        "comment": None, "doc": None, "doc_key": "bold", "codetag": "bold",
        "keyword": None, "self": None, "const_lang": None, "operator_decl": None,
        "preproc": None, "attribute": None, "type": None, "func_decl": None,
        "func_call": None, "param": "italic", "init": None, "head": "bold",
        "bold": "bold", "italic": "italic", "bold_italic": "bold italic",
        "underline": "underline", "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #FFFFFF; color: #000000; "
             "border: 1px solid #0A246A; } a { color: #0000FF; }",
}

VC6 = {
    "name": "Visual C++ 6",
    "note": "Developer Studio 6 editor — flat black identifiers, blue keywords, green comments",
    "colors": {
        "g_bg": "#FFFFFF", "g_fg": "#000000", "g_caret": "#000000",
        "g_block_caret": "#555555", "g_invisibles": "#D4D0C8",
        "g_line_hl": "#F4F4F4", "g_sel": "#D3DCEE", "g_sel_fg": None,
        "g_sel_border": "#000080", "g_inactive_sel": "#DCDCD8",
        "g_inactive_sel_fg": None, "g_highlight": "#808000",
        "g_find": "#FFFF80", "g_find_fg": "#000000",
        "g_gutter_fg": "#6A6A6A", "g_gutter_fg_hl": "#000080",
        "g_guide": "#E6E4E0", "g_active_guide": "#B4B4C8",
        "g_stack_guide": "#EFEDE9", "g_fold": "#FFFF80", "g_shadow": "#00000014",
        "g_accent": "#000080", "g_brackets": "#000080", "g_tags": "#000080",
        # Developer Studio colored six categories only. The rest stays black.
        "comment": "#008000", "doc": "#008000", "doc_key": "#006400",
        "codetag": "#006400",
        "string": "#000080", "string_raw": "#000080", "char": "#000080",
        "escape": "#800080", "interp_punct": "#800080", "interp_fg": "#000000",
        "interp_bg": "#F6F6FA", "regexp": "#800080", "regexp_op": "#000080",
        "number": "#000080", "const_lang": "#0000FF", "const_other": "#000080",
        "enum_member": "#000080",
        "keyword": "#0000FF", "keyword_control": "#0000FF", "module": "#000080",
        "storage_type": "#0000FF", "storage_mod": "#0000FF", "self": "#0000FF",
        "operator_word": "#0000FF", "operator": "#000000", "operator_decl": "#000000",
        "preproc": "#0000FF", "preproc_inactive": "#7A7A7A",
        "directive_value": "#0000FF", "attribute": "#0000FF",
        "attr_option": "#000080",
        "type": "#000000", "type_lib": "#000000", "type_alias": "#000000",
        "generic": "#000000", "type_punct": "#000000",
        # Zed/clangd can collapse built-in and user types into one `type`
        # capture. Prefer the visible VC6 keyword blue in that fallback.
        "type_fallback": "#0000FF",
        "func_decl": "#000000", "func_call": "#000000", "func_builtin": "#000000",
        "arg_label": "#4A4A4A", "param": "#000000", "init": "#0000FF",
        "accessor": "#0000FF", "shorthand": "#000080",
        "var": "#000000", "var_decl": "#000000", "member": "#000000", "var_project": "#2E5C8A",
        "punct": "#000000", "brace": "#000000", "continuation": "#808080",
        "label": "#000080", "invalid_fg": "#FFFFFF", "invalid_bg": "#800000",
        "deprecated_bg": "#800080",
        "head": "#000080", "bold": "#000000", "italic": "#000000",
        "link": "#0000FF", "raw": "#000080", "raw_bg": "#F4F4F4",
        "list_punct": "#000080", "quote": "#4A4A4A",
        "diff_add_fg": "#008000", "diff_add_bg": "#E8F4E8",
        "diff_del_fg": "#800000", "diff_del_bg": "#F8EAEA",
        "diff_chg_fg": "#808000", "diff_chg_bg": "#F8F6E0",
        "key": "#000080", "tag": "#000080", "tag_attr": "#800000",
        "reg_red": "#FF0000", "reg_orange": "#B8860B", "reg_yellow": "#808000",
        "reg_green": "#008000", "reg_blue": "#0000FF", "reg_purple": "#800080",
        "reg_pink": "#800000",
    },
    "styles": {
        # MSDEV drew every token in one weight, and it did not slant comments.
        "comment": None, "doc": None, "doc_key": "bold", "codetag": "bold",
        "keyword": None, "self": None, "const_lang": None, "operator_decl": None,
        "preproc": None, "attribute": None, "type": None, "func_decl": None,
        "func_call": None, "param": None, "init": None, "head": "bold",
        "bold": "bold", "italic": "italic", "bold_italic": "bold italic",
        "underline": "underline", "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #FFFFFF; color: #000000; "
             "border: 1px solid #000080; } a { color: #0000FF; }",
}

BCB = {
    "name": "Borland C++ Builder",
    "note": "C++Builder editor — navy bold reserved words, green comments, olive directives",
    "colors": {
        "g_bg": "#FFFFFF", "g_fg": "#000000", "g_caret": "#000000",
        "g_block_caret": "#4A4A56", "g_invisibles": "#DADEE4",
        "g_line_hl": "#F5F8FC", "g_sel": "#D2E2F6", "g_sel_fg": None,
        "g_sel_border": "#A8C4E6", "g_inactive_sel": "#E9F0F9",
        "g_inactive_sel_fg": None, "g_highlight": "#C8A22A",
        "g_find": "#FBEEA6", "g_find_fg": "#000000",
        "g_gutter_fg": "#8A8A94", "g_gutter_fg_hl": "#000080",
        "g_guide": "#E2E6EC", "g_active_guide": "#AEC2DC",
        "g_stack_guide": "#EBEEF3", "g_fold": "#FBEEA6", "g_shadow": "#00000012",
        "g_accent": "#000080", "g_brackets": "#7F7F00", "g_tags": "#7F7F00",
        "comment": "#008000", "doc": "#2F7A4F", "doc_key": "#006400",
        "codetag": "#006400",
        "string": "#0000FF", "string_raw": "#0000FF", "char": "#0000C0",
        "escape": "#7A3E9D", "interp_punct": "#7A3E9D", "interp_fg": "#000000",
        "interp_bg": "#F3F5FD", "regexp": "#9B2D6F", "regexp_op": "#7A3E9D",
        "number": "#800000", "const_lang": "#000080", "const_other": "#0B7A75",
        "enum_member": "#0B7A75",
        "keyword": "#000080", "keyword_control": "#000080", "module": "#0B7A75",
        "storage_type": "#000080", "storage_mod": "#000080", "self": "#000080",
        "operator_word": "#000080", "operator": "#000000", "operator_decl": "#000080",
        "preproc": "#7F7F00", "preproc_inactive": "#7A7A7A",
        "directive_value": "#7F7F00", "attribute": "#7A3E9D",
        "attr_option": "#9A6BB8",
        "type": "#0B7A75", "type_lib": "#0B7A75", "type_alias": "#0B7A75",
        "generic": "#0E5F73", "type_punct": "#0B7A75",
        "func_decl": "#7A3E9D", "func_call": "#7A3E9D", "func_builtin": "#7A3E9D",
        "arg_label": "#5A5A70", "param": "#3C3C46", "init": "#000080",
        "accessor": "#000080", "shorthand": "#0E5F73",
        "var": "#000000", "var_decl": "#000000", "member": "#000000", "var_project": "#6B4423",
        "punct": "#3C3C46", "brace": "#7F7F00", "continuation": "#82828C",
        "label": "#000080", "invalid_fg": "#FFFFFF", "invalid_bg": "#C0392B",
        "deprecated_bg": "#7A3E9D",
        "head": "#000080", "bold": "#000000", "italic": "#000000",
        "link": "#0000FF", "raw": "#0000FF", "raw_bg": "#F6F7FA",
        "list_punct": "#7F7F00", "quote": "#3C3C46",
        "diff_add_fg": "#0B6B33", "diff_add_bg": "#EAF7EE",
        "diff_del_fg": "#9B1C1C", "diff_del_bg": "#FDECEC",
        "diff_chg_fg": "#8A5A00", "diff_chg_bg": "#FCF6E3",
        "key": "#0B7A75", "tag": "#000080", "tag_attr": "#800000",
        "reg_red": "#C0392B", "reg_orange": "#800000", "reg_yellow": "#7F7F00",
        "reg_green": "#008000", "reg_blue": "#000080", "reg_purple": "#7A3E9D",
        "reg_pink": "#9B2D6F",
    },
    "styles": {
        # As in Delphi: reserved words get the weight, nothing else.
        "comment": "italic", "doc": "italic", "doc_key": "bold italic",
        "codetag": "bold italic", "keyword": "bold", "self": "bold italic",
        "const_lang": None, "operator_decl": None, "preproc": None,
        "attribute": None, "type": None, "func_decl": None, "func_call": None,
        "param": "italic", "init": None, "head": "bold", "bold": "bold",
        "italic": "italic", "bold_italic": "bold italic", "underline": "underline",
        "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #FFFFFF; color: #000000; "
             "border: 1px solid #AEC2DC; } a { color: #000080; }",
}

ECLIPSE = {
    "name": "Eclipse Classic",
    "note": "Eclipse JDT defaults — maroon bold keywords, blue strings, blue Javadoc, brown locals",
    "colors": {
        "g_bg": "#FFFFFF", "g_fg": "#000000", "g_caret": "#000000",
        "g_block_caret": "#5A5A5A", "g_invisibles": "#DCDCDC",
        "g_line_hl": "#E8F2FE", "g_sel": "#C0DCF3", "g_sel_fg": None,
        "g_sel_border": "#9CC4E4", "g_inactive_sel": "#E4EDF6",
        "g_inactive_sel_fg": None, "g_highlight": "#C9A227",
        "g_find": "#FFF2A8", "g_find_fg": "#000000",
        "g_gutter_fg": "#808080", "g_gutter_fg_hl": "#7F0055",
        "g_guide": "#E7E7E7", "g_active_guide": "#B4CDE4",
        "g_stack_guide": "#F0F0F0", "g_fold": "#FFF2A8", "g_shadow": "#00000012",
        "g_accent": "#7F0055", "g_brackets": "#7F0055", "g_tags": "#7F0055",
        "comment": "#3F7F5F", "doc": "#3F5FBF", "doc_key": "#7F9FBF",
        "codetag": "#3F7F5F",
        "string": "#2A00FF", "string_raw": "#2A00FF", "char": "#2A00FF",
        "escape": "#7F0055", "interp_punct": "#7F0055", "interp_fg": "#000000",
        "interp_bg": "#F5F5FD", "regexp": "#2A00FF", "regexp_op": "#7F0055",
        "number": "#2A00FF", "const_lang": "#7F0055", "const_other": "#0000C0",
        "enum_member": "#0000C0",
        "keyword": "#7F0055", "keyword_control": "#7F0055", "module": "#000000",
        "storage_type": "#7F0055", "storage_mod": "#7F0055", "self": "#7F0055",
        "operator_word": "#7F0055", "operator": "#000000", "operator_decl": "#000000",
        "preproc": "#646464", "preproc_inactive": "#7A7A7A",
        "directive_value": "#646464", "attribute": "#646464",
        "attr_option": "#7F7F7F",
        "type": "#0000C0", "type_lib": "#0000C0", "type_alias": "#0000C0",
        "generic": "#0000C0", "type_punct": "#0000C0",
        "func_decl": "#000000", "func_call": "#000000", "func_builtin": "#000000",
        "arg_label": "#6A3E3E", "param": "#6A3E3E", "init": "#7F0055",
        "accessor": "#7F0055", "shorthand": "#0000C0",
        "var": "#000000", "var_decl": "#000000", "member": "#0000C0", "var_project": "#0000C0",
        "punct": "#000000", "brace": "#000000", "continuation": "#808080",
        "label": "#0000C0", "invalid_fg": "#FFFFFF", "invalid_bg": "#C0392B",
        "deprecated_bg": "#646464",
        "head": "#7F0055", "bold": "#000000", "italic": "#000000",
        "link": "#2A00FF", "raw": "#2A00FF", "raw_bg": "#F5F5F5",
        "list_punct": "#7F0055", "quote": "#3F7F5F",
        "diff_add_fg": "#0B6B33", "diff_add_bg": "#EAF7EE",
        "diff_del_fg": "#9B1C1C", "diff_del_bg": "#FDECEC",
        "diff_chg_fg": "#8A5A00", "diff_chg_bg": "#FCF6E3",
        "key": "#0000C0", "tag": "#3F7F7F", "tag_attr": "#7F007F",
        "reg_red": "#C0392B", "reg_orange": "#6A3E3E", "reg_yellow": "#8A6D00",
        "reg_green": "#3F7F5F", "reg_blue": "#3F5FBF", "reg_purple": "#7F0055",
        "reg_pink": "#7F007F",
    },
    "styles": {
        # Eclipse bolded keywords by default. Types get color, not weight.
        "comment": None, "doc": None, "doc_key": "bold", "codetag": "bold",
        "keyword": "bold", "self": "bold", "const_lang": "bold",
        "operator_decl": None, "preproc": None, "attribute": None, "type": None,
        "func_decl": None, "func_call": None, "param": None, "init": None,
        "head": "bold", "bold": "bold", "italic": "italic",
        "bold_italic": "bold italic", "underline": "underline", "quote": "italic",
        "tag": None,
    },
    "popup": "html { background-color: #FFFFFF; color: #000000; "
             "border: 1px solid #9CC4E4; } a { color: #2A00FF; }",
}

VS2012_DARK = {
    "name": "Visual Studio 2012 Dark",
    "note": "Visual Studio 2012 Dark — the first dark theme Visual Studio shipped",
    "colors": {
        "g_bg": "#1E1E1E", "g_fg": "#DCDCDC", "g_caret": "#DCDCDC",
        "g_block_caret": "#A0A0A0", "g_invisibles": "#3B3B3B",
        "g_line_hl": "#2A2A2A", "g_sel": "#264F78", "g_sel_fg": None,
        "g_sel_border": "#3A6EA5", "g_inactive_sel": "#3A3D41",
        "g_inactive_sel_fg": None, "g_highlight": "#C8A020",
        "g_find": "#515C6A", "g_find_fg": "#DCDCDC",
        "g_gutter_fg": "#2B91AF", "g_gutter_fg_hl": "#4EC9B0",
        "g_guide": "#404040", "g_active_guide": "#707070",
        "g_stack_guide": "#333333", "g_fold": "#515C6A", "g_shadow": "#00000060",
        "g_accent": "#4EC9B0", "g_brackets": "#4EC9B0", "g_tags": "#4EC9B0",
        "comment": "#57A64A", "doc": "#608B4E", "doc_key": "#8CBF7A",
        "codetag": "#D7BA7D",
        "string": "#D69D85", "string_raw": "#D69D85", "char": "#D69D85",
        "escape": "#D7BA7D", "interp_punct": "#D7BA7D", "interp_fg": "#DCDCDC",
        "interp_bg": "#262626", "regexp": "#D16969", "regexp_op": "#D7BA7D",
        "number": "#B5CEA8", "const_lang": "#569CD6", "const_other": "#C8C8C8",
        "enum_member": "#B8D7A3",
        # VS 2012 drew every keyword in one blue. The separate magenta for
        # control flow arrived later, in VS Code.
        "keyword": "#569CD6", "keyword_control": "#569CD6", "module": "#C8C8C8",
        "storage_type": "#569CD6", "storage_mod": "#569CD6", "self": "#569CD6",
        "operator_word": "#569CD6", "operator": "#B4B4B4",
        "operator_decl": "#B4B4B4",
        "preproc": "#9B9B9B", "macro": "#BD63C5", "preproc_inactive": "#787878",
        "directive_value": "#C8C8C8", "attribute": "#4EC9B0",
        "attr_option": "#9CDCFE",
        "type": "#4EC9B0", "type_lib": "#4EC9B0", "type_alias": "#4EC9B0",
        "generic": "#B8D7A3", "type_punct": "#4EC9B0",
        "func_decl": "#C8C8C8", "func_call": "#C8C8C8", "func_builtin": "#C8C8C8",
        "arg_label": "#7F7F7F", "param": "#7F7F7F", "init": "#C8C8C8",
        "accessor": "#569CD6", "shorthand": "#C8C8C8",
        "var": "#C8C8C8", "var_decl": "#C8C8C8", "member": "#DADADA", "var_project": "#C8C8C8",
        "punct": "#DCDCDC", "brace": "#DCDCDC", "continuation": "#909090",
        "label": "#D7BA7D", "invalid_fg": "#FFFFFF", "invalid_bg": "#A1260D",
        "deprecated_bg": "#5A3E00",
        "head": "#569CD6", "bold": "#DCDCDC", "italic": "#DCDCDC",
        "link": "#3794FF", "raw": "#D69D85", "raw_bg": "#252526",
        "list_punct": "#6796E6", "quote": "#57A64A",
        "diff_add_fg": "#6A9955", "diff_add_bg": "#1E3A24",
        "diff_del_fg": "#F14C4C", "diff_del_bg": "#3A1D1D",
        "diff_chg_fg": "#D7BA7D", "diff_chg_bg": "#3A3222",
        "key": "#9CDCFE", "tag": "#569CD6", "tag_attr": "#9CDCFE",
        "reg_red": "#F14C4C", "reg_orange": "#CE9178", "reg_yellow": "#D7BA7D",
        "reg_green": "#6A9955", "reg_blue": "#569CD6", "reg_purple": "#C586C0",
        "reg_pink": "#D16969",
    },
    "styles": {
        # Visual Studio drew all code in one weight and did not slant comments.
        "comment": None, "doc": None, "doc_key": "bold", "codetag": "bold",
        "keyword": None, "self": None, "const_lang": None, "operator_decl": None,
        "preproc": None, "attribute": None, "type": None, "func_decl": None,
        "func_call": None, "param": "italic", "init": None, "head": "bold",
        "bold": "bold", "italic": "italic", "bold_italic": "bold italic",
        "underline": "underline", "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #252526; color: #DCDCDC; "
             "border: 1px solid #3A6EA5; } a { color: #3794FF; }",
}

IDEA = {
    "name": "IntelliJ IDEA Default",
    "note": "IntelliJ IDEA Default — green bold strings, navy bold keywords, olive annotations",
    "colors": {
        "g_bg": "#FFFFFF", "g_fg": "#000000", "g_caret": "#000000",
        "g_block_caret": "#555555", "g_invisibles": "#D0D0D0",
        # The warm caret row is the mark of the IDEA light scheme.
        "g_line_hl": "#FCFAED", "g_sel": "#A6D2FF", "g_sel_fg": None,
        "g_sel_border": "#7DB4EE", "g_inactive_sel": "#DDEBFA",
        "g_inactive_sel_fg": None, "g_highlight": "#FFEB99",
        "g_find": "#FFEB99", "g_find_fg": "#000000",
        "g_gutter_fg": "#999999", "g_gutter_fg_hl": "#000080",
        "g_guide": "#E8E8E8", "g_active_guide": "#9C9C9C",
        "g_stack_guide": "#F0F0F0", "g_fold": "#E9F1FA",
        "g_shadow": "#00000012",
        "g_accent": "#000080", "g_brackets": "#000080", "g_tags": "#000080",
        "comment": "#808080", "doc": "#808080", "doc_key": "#808080",
        "codetag": "#008080",
        "string": "#008000", "string_raw": "#008000", "char": "#008000",
        "escape": "#0037A6", "interp_punct": "#000080", "interp_fg": "#000000",
        "interp_bg": "#F7F7F7", "regexp": "#008000", "regexp_op": "#0037A6",
        "number": "#0000FF", "const_lang": "#000080", "const_other": "#660E7A",
        "enum_member": "#660E7A",
        "keyword": "#000080", "keyword_control": "#000080", "module": "#000000",
        "storage_type": "#000080", "storage_mod": "#000080", "self": "#000080",
        "operator_word": "#000080", "operator": "#000000",
        "operator_decl": "#000000",
        "preproc": "#808000", "preproc_inactive": "#7A7A7A",
        "directive_value": "#660E7A", "attribute": "#808000",
        "attr_option": "#808000",
        # IDEA Default leaves classes, methods and locals black. Only fields,
        # constants and type parameters get a color.
        "type": "#000000", "type_lib": "#000000", "type_alias": "#000000",
        "generic": "#20999D", "type_punct": "#000000",
        "func_decl": "#000000", "func_call": "#000000", "func_builtin": "#000000",
        "arg_label": "#000000", "param": "#000000", "init": "#000080",
        "accessor": "#000080", "shorthand": "#660E7A",
        "var": "#000000", "var_decl": "#000000", "member": "#660E7A", "var_project": "#660E7A",
        "punct": "#000000", "brace": "#000000", "continuation": "#808080",
        "label": "#000080", "invalid_fg": "#FFFFFF", "invalid_bg": "#C0392B",
        "deprecated_bg": "#808000",
        "head": "#000080", "bold": "#000000", "italic": "#000000",
        "link": "#0000FF", "raw": "#008000", "raw_bg": "#F7F7F7",
        "list_punct": "#000080", "quote": "#808080",
        "diff_add_fg": "#0B6B33", "diff_add_bg": "#E7F2E7",
        "diff_del_fg": "#9B1C1C", "diff_del_bg": "#F5E6E6",
        "diff_chg_fg": "#1F4E79", "diff_chg_bg": "#E6EEF7",
        "key": "#660E7A", "tag": "#000080", "tag_attr": "#660E7A",
        "reg_red": "#C0392B", "reg_orange": "#808000", "reg_yellow": "#8A6D00",
        "reg_green": "#008000", "reg_blue": "#000080", "reg_purple": "#660E7A",
        "reg_pink": "#A0208A",
    },
    "styles": {
        # IDEA bolds keywords and fields, and slants comments.
        "comment": "italic", "doc": "italic", "doc_key": "bold",
        "codetag": "bold", "keyword": "bold", "self": "bold",
        "const_lang": "bold", "operator_decl": None, "preproc": None,
        "attribute": None, "type": None, "func_decl": None, "func_call": None,
        "param": None, "init": "bold", "head": "bold", "bold": "bold",
        "italic": "italic", "bold_italic": "bold italic",
        "underline": "underline", "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #FFFFFF; color: #000000; "
             "border: 1px solid #7DB4EE; } a { color: #0000FF; }",
}

EMACS = {
    "name": "Emacs 21",
    "note": "Emacs font-lock on light paper — firebrick comments, rosy-brown strings, purple keywords",
    "colors": {
        "g_bg": "#FFFFFF", "g_fg": "#000000", "g_caret": "#000000",
        "g_block_caret": "#555555", "g_invisibles": "#D0D0D0",
        "g_line_hl": "#F0F0F0",
        # lightgoldenrod2: the region color of Emacs on a light frame.
        "g_sel": "#EEDC82", "g_sel_fg": None, "g_sel_border": "#D9C36A",
        "g_inactive_sel": "#F5EDD0", "g_inactive_sel_fg": None,
        "g_highlight": "#B4EEB4", "g_find": "#AFEEEE", "g_find_fg": "#000000",
        "g_gutter_fg": "#808080", "g_gutter_fg_hl": "#A020F0",
        "g_guide": "#E6E6E6", "g_active_guide": "#A0A0A0",
        "g_stack_guide": "#F0F0F0", "g_fold": "#EEDC82",
        "g_shadow": "#00000012",
        "g_accent": "#A020F0", "g_brackets": "#A020F0", "g_tags": "#A020F0",
        # font-lock draws strings in RosyBrown (#BC8F8F). That reads at 2.8:1
        # on white, and it covers every string in the file. This scheme uses a
        # darker rosy brown. Set these back to #BC8F8F for the exact face.
        "comment": "#B22222", "doc": "#966464", "doc_key": "#9400D3",
        "codetag": "#FF0000",
        "string": "#966464", "string_raw": "#966464", "char": "#966464",
        "escape": "#483D8B", "interp_punct": "#483D8B", "interp_fg": "#000000",
        "interp_bg": "#F7F7F7", "regexp": "#966464", "regexp_op": "#483D8B",
        "number": "#008B8B", "const_lang": "#008B8B", "const_other": "#008B8B",
        "enum_member": "#008B8B",
        "keyword": "#A020F0", "keyword_control": "#A020F0", "module": "#008B8B",
        "storage_type": "#A020F0", "storage_mod": "#A020F0", "self": "#A020F0",
        "operator_word": "#A020F0", "operator": "#000000",
        "operator_decl": "#0000FF",
        "preproc": "#483D8B", "preproc_inactive": "#7A7A7A",
        "directive_value": "#008B8B", "attribute": "#483D8B",
        "attr_option": "#6A5ACD",
        "type": "#228B22", "type_lib": "#228B22", "type_alias": "#228B22",
        "generic": "#2E8B57", "type_punct": "#228B22",
        "func_decl": "#0000FF", "func_call": "#0000FF", "func_builtin": "#483D8B",
        "arg_label": "#A0522D", "param": "#A0522D", "init": "#0000FF",
        "accessor": "#A020F0", "shorthand": "#A0522D",
        "var": "#000000", "var_decl": "#A0522D", "member": "#A0522D", "var_project": "#A0522D",
        "punct": "#000000", "brace": "#000000", "continuation": "#808080",
        "label": "#0000FF", "invalid_fg": "#FFFFFF", "invalid_bg": "#FF0000",
        "deprecated_bg": "#B22222",
        "head": "#0000FF", "bold": "#000000", "italic": "#000000",
        "link": "#0000EE", "raw": "#966464", "raw_bg": "#F5F5F5",
        "list_punct": "#A020F0", "quote": "#B22222",
        "diff_add_fg": "#227722", "diff_add_bg": "#DDFFDD",
        "diff_del_fg": "#AA2222", "diff_del_bg": "#FFDDDD",
        "diff_chg_fg": "#8A6D00", "diff_chg_bg": "#FFFFDD",
        "key": "#A0522D", "tag": "#0000FF", "tag_attr": "#A0522D",
        "reg_red": "#FF0000", "reg_orange": "#A0522D", "reg_yellow": "#8A6D00",
        "reg_green": "#228B22", "reg_blue": "#0000FF", "reg_purple": "#A020F0",
        "reg_pink": "#DA70D6",
    },
    "styles": {
        # font-lock keeps one weight. Only the warning face gets bold.
        "comment": None, "doc": None, "doc_key": "bold", "codetag": "bold",
        "keyword": None, "self": None, "const_lang": None,
        "operator_decl": None, "preproc": None, "attribute": None, "type": None,
        "func_decl": None, "func_call": None, "param": None, "init": None,
        "head": "bold", "bold": "bold", "italic": "italic",
        "bold_italic": "bold italic", "underline": "underline",
        "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #FFFFFF; color: #000000; "
             "border: 1px solid #D9C36A; } a { color: #0000EE; }",
}

VIM = {
    "name": "Vim Light",
    "note": "Vim GUI defaults for background=light — blue comments, brown bold keywords",
    "colors": {
        "g_bg": "#FFFFFF", "g_fg": "#000000", "g_caret": "#000000",
        "g_block_caret": "#555555",
        # SpecialKey and NonText are Blue in Vim.
        "g_invisibles": "#8080FF",
        "g_line_hl": "#E5E5E5", "g_sel": "#D3D3D3", "g_sel_fg": None,
        "g_sel_border": "#B8B8B8", "g_inactive_sel": "#E8E8E8",
        "g_inactive_sel_fg": None, "g_highlight": "#FFFF00",
        "g_find": "#FFFF00", "g_find_fg": "#000000",
        # LineNr is Brown in Vim, not gray.
        "g_gutter_fg": "#A52A2A", "g_gutter_fg_hl": "#A52A2A",
        "g_guide": "#E0E0E0", "g_active_guide": "#A52A2A",
        "g_stack_guide": "#EDEDED", "g_fold": "#D3D3D3",
        "g_shadow": "#00000012",
        "g_accent": "#A52A2A", "g_brackets": "#008B8B", "g_tags": "#008B8B",
        "comment": "#0000FF", "doc": "#0000FF", "doc_key": "#6A0DAD",
        "codetag": "#6A0DAD",
        # Vim draws Constant in Magenta (#FF00FF). That reads at 3.1:1 on white,
        # and Constant covers every string and number. This scheme darkens it.
        "string": "#C000C0", "string_raw": "#C000C0", "char": "#C000C0",
        "escape": "#6A5ACD", "interp_punct": "#6A5ACD", "interp_fg": "#000000",
        "interp_bg": "#F7F7F7", "regexp": "#C000C0", "regexp_op": "#6A5ACD",
        "number": "#C000C0", "const_lang": "#C000C0", "const_other": "#C000C0",
        "enum_member": "#C000C0",
        "keyword": "#A52A2A", "keyword_control": "#A52A2A", "module": "#6A0DAD",
        "storage_type": "#2E8B57", "storage_mod": "#2E8B57", "self": "#A52A2A",
        "operator_word": "#A52A2A", "operator": "#A52A2A",
        "operator_decl": "#A52A2A",
        "preproc": "#6A0DAD", "preproc_inactive": "#7A7A7A",
        "directive_value": "#C000C0", "attribute": "#6A5ACD",
        "attr_option": "#6A5ACD",
        "type": "#2E8B57", "type_lib": "#2E8B57", "type_alias": "#2E8B57",
        "generic": "#2E8B57", "type_punct": "#2E8B57",
        "func_decl": "#008B8B", "func_call": "#008B8B", "func_builtin": "#008B8B",
        "arg_label": "#008B8B", "param": "#008B8B", "init": "#008B8B",
        "accessor": "#A52A2A", "shorthand": "#008B8B",
        "var": "#000000", "var_decl": "#008B8B", "member": "#008B8B", "var_project": "#008B8B",
        "punct": "#6A5ACD", "brace": "#6A5ACD", "continuation": "#6A5ACD",
        "label": "#A52A2A", "invalid_fg": "#FFFFFF", "invalid_bg": "#FF0000",
        "deprecated_bg": "#6A0DAD",
        "head": "#A52A2A", "bold": "#000000", "italic": "#000000",
        "link": "#6A5ACD", "raw": "#C000C0", "raw_bg": "#F5F5F5",
        "list_punct": "#6A5ACD", "quote": "#0000FF",
        # The diff colors of Vim: LightBlue, LightCyan and LightMagenta.
        "diff_add_fg": "#005F87", "diff_add_bg": "#ADD8E6",
        "diff_del_fg": "#0000FF", "diff_del_bg": "#E0FFFF",
        "diff_chg_fg": "#8B008B", "diff_chg_bg": "#FFBBFF",
        "key": "#008B8B", "tag": "#6A5ACD", "tag_attr": "#008B8B",
        "reg_red": "#FF0000", "reg_orange": "#A52A2A", "reg_yellow": "#8A6D00",
        "reg_green": "#2E8B57", "reg_blue": "#0000FF", "reg_purple": "#6A0DAD",
        "reg_pink": "#C000C0",
    },
    "styles": {
        # Vim sets gui=bold on Statement and on Type. Nothing else.
        "comment": None, "doc": None, "doc_key": "bold", "codetag": "bold",
        "keyword": "bold", "self": "bold", "const_lang": None,
        "operator_decl": "bold", "preproc": None, "attribute": None,
        "type": "bold", "func_decl": None, "func_call": None, "param": None,
        "init": None, "head": "bold", "bold": "bold", "italic": "italic",
        "bold_italic": "bold italic", "underline": "underline",
        "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #FFFFFF; color: #000000; "
             "border: 1px solid #B8B8B8; } a { color: #6A5ACD; }",
}

CW = {
    "name": "CodeWarrior",
    "note": "Metrowerks CodeWarrior on classic Mac OS - red comments, blue "
            "keywords, purple literals",
    "colors": {
        "g_bg": "#FFFFFF", "g_fg": "#000000", "g_caret": "#000000",
        "g_block_caret": "#555555",
        "g_invisibles": "#B8B8B8",
        # Platinum grey, the window grey of Mac OS 8 and 9.
        "g_line_hl": "#EFEFEF",
        # The highlight blue-grey of classic Mac OS. CodeWarrior took the
        # selection color from the system, not from its own palette.
        "g_sel": "#B0C4DE", "g_sel_fg": None,
        "g_sel_border": "#8FA8C8", "g_inactive_sel": "#DCE3EC",
        "g_inactive_sel_fg": None, "g_highlight": "#FFF08C",
        "g_find": "#FFF08C", "g_find_fg": "#000000",
        # The CodeWarrior editor had no line-number margin. It put the line
        # number in a field at the bottom of the window. This grey is a choice.
        "g_gutter_fg": "#7A7A7A", "g_gutter_fg_hl": "#0000C0",
        "g_guide": "#E4E4E4", "g_active_guide": "#0000C0",
        "g_stack_guide": "#EFEFEF", "g_fold": "#B0C4DE",
        "g_shadow": "#00000012",
        "g_accent": "#0000C0", "g_brackets": "#C00000", "g_tags": "#C00000",
        "comment": "#C00000", "doc": "#C00000", "doc_key": "#800000",
        "codetag": "#800000",
        "string": "#800080", "string_raw": "#800080", "char": "#800080",
        "escape": "#806000", "interp_punct": "#806000", "interp_fg": "#000000",
        "interp_bg": "#F9F5EE", "regexp": "#800080", "regexp_op": "#806000",
        # CodeWarrior colored the strings, but not the numbers. This scheme
        # gives the numbers the string purple, so that every literal has one
        # color. Compare Visual C++ 6, which does the same with navy.
        "number": "#800080", "const_lang": "#0000C0", "const_other": "#006E6E",
        "enum_member": "#006E6E",
        "keyword": "#0000C0", "keyword_control": "#0000C0", "module": "#007000",
        "storage_type": "#0000C0", "storage_mod": "#0000C0", "self": "#0000C0",
        "operator_word": "#0000C0", "operator": "#000000",
        "operator_decl": "#0000C0",
        # Custom Keyword Set 3: the preprocessor and the attributes.
        "preproc": "#806000", "preproc_inactive": "#8A8A8A",
        "directive_value": "#800080", "attribute": "#806000",
        "attr_option": "#806000",
        # Custom Keyword Set 1: the types. The Toolbox types (Handle, OSErr,
        # Str255) went in this set.
        "type": "#007000", "type_lib": "#007000", "type_alias": "#007000",
        "generic": "#007000", "type_punct": "#007000",
        # Custom Keyword Set 2: the functions.
        "func_decl": "#6A00A0", "func_call": "#6A00A0", "func_builtin": "#6A00A0",
        "arg_label": "#6A00A0", "param": "#000000", "init": "#6A00A0",
        "accessor": "#0000C0", "shorthand": "#6A00A0",
        # Custom Keyword Set 4: the variables.
        "var": "#000000", "var_decl": "#000000", "member": "#000000",
        "var_project": "#006E6E",
        "punct": "#000000", "brace": "#000000", "continuation": "#806000",
        "label": "#0000C0", "invalid_fg": "#FFFFFF", "invalid_bg": "#C00000",
        "deprecated_bg": "#6A00A0",
        "head": "#0000C0", "bold": "#000000", "italic": "#000000",
        "link": "#0000C0", "raw": "#800080", "raw_bg": "#F4F4F4",
        "list_punct": "#806000", "quote": "#C00000",
        "diff_add_fg": "#007000", "diff_add_bg": "#E4F0E4",
        "diff_del_fg": "#C00000", "diff_del_bg": "#F9E4E4",
        "diff_chg_fg": "#806000", "diff_chg_bg": "#F6F0DE",
        "key": "#006E6E", "tag": "#0000C0", "tag_attr": "#6A00A0",
        "reg_red": "#C00000", "reg_orange": "#806000", "reg_yellow": "#8A6D00",
        "reg_green": "#007000", "reg_blue": "#0000C0", "reg_purple": "#6A00A0",
        "reg_pink": "#A0006A",
    },
    "styles": {
        # The CodeWarrior IDE gave each category a face of its own, but every
        # default was the plain face. No category came bold or italic.
        "comment": None, "doc": None, "doc_key": "bold", "codetag": "bold",
        "keyword": None, "self": None, "const_lang": None,
        "operator_decl": None, "preproc": None, "attribute": None,
        "type": None, "func_decl": None, "func_call": None, "param": None,
        "init": None, "head": "bold", "bold": "bold", "italic": "italic",
        "bold_italic": "bold italic", "underline": "underline",
        "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #FFFFFF; color: #000000; "
             "border: 1px solid #8FA8C8; } a { color: #0000C0; }",
}

NPP = {
    "name": "Notepad++ Default",
    "note": "Notepad++ default styler - green comments, blue bold keywords, "
            "grey strings, navy bold operators",
    "colors": {
        "g_bg": "#FFFFFF", "g_fg": "#000000",
        # "Caret colour" is purple in the default styler, not black.
        "g_caret": "#8000FF", "g_block_caret": "#8000FF",
        # "White space symbol" is a light orange.
        "g_invisibles": "#FFB56A",
        "g_line_hl": "#E8E8FF",
        # "Selected text colour" is a grey bar. Notepad++ locks the text color
        # of that bar, therefore the syntax colors stay.
        "g_sel": "#C0C0C0", "g_sel_fg": None,
        "g_sel_border": "#A0A0A0", "g_inactive_sel": "#DEDEDE",
        "g_inactive_sel_fg": None,
        # "Smart Highlighting" is green. "Find Mark Style" is red, therefore
        # the found text goes white.
        "g_highlight": "#00FF00",
        "g_find": "#FF0000", "g_find_fg": "#FFFFFF",
        # "Line number margin": grey numbers. The margin grey (#E4E4E4) does
        # not come here, because the gutter uses the paper of the text area.
        "g_gutter_fg": "#808080", "g_gutter_fg_hl": "#8000FF",
        "g_guide": "#C0C0C0", "g_active_guide": "#8000FF",
        "g_stack_guide": "#E4E4E4", "g_fold": "#808080",
        "g_shadow": "#00000012",
        "g_accent": "#8000FF",
        # "Brace highlight style" is red. "Tags match highlighting" is purple.
        "g_brackets": "#FF0000", "g_tags": "#8000FF",
        "comment": "#008000", "doc": "#008080", "doc_key": "#008080",
        "codetag": "#008080",
        # STRING, STRINGRAW and CHARACTER are all grey. Grey strings are the
        # mark of the default styler. The grey reads at 4.0:1 on white; set
        # "string" to #6E6E6E if you want more contrast.
        "string": "#808080", "string_raw": "#808080", "char": "#808080",
        # The JSON lexer draws "ESCAPE SEQUENCE" in blue.
        "escape": "#0000FF", "interp_punct": "#0000FF", "interp_fg": "#000000",
        "interp_bg": "#F4F4FF", "regexp": "#000000", "regexp_op": "#000080",
        # NUMBER is #FF8000 in the styler. That reads at 2.7:1 on white, and
        # this scheme darkens it. Set "number" back to #FF8000 for the exact
        # styler value.
        "number": "#B05500", "const_lang": "#0000FF", "const_other": "#000080",
        "enum_member": "#000080",
        "keyword": "#0000FF", "keyword_control": "#0000FF", "module": "#804000",
        "storage_type": "#8000FF", "storage_mod": "#0000FF", "self": "#0000FF",
        "operator_word": "#0000FF", "operator": "#000080",
        "operator_decl": "#000080",
        "preproc": "#804000", "preproc_inactive": "#A0A0A0",
        "directive_value": "#808080",
        # The Python lexer draws the decorators in orange, therefore the
        # attributes follow the darkened orange of the numbers.
        "attribute": "#B05500", "attr_option": "#B05500",
        # TYPE WORD: the second keyword list of each lexer.
        "type": "#8000FF", "type_lib": "#8000FF", "type_alias": "#8000FF",
        "generic": "#8000FF", "type_punct": "#000080",
        # Notepad++ gives the function names and the identifiers no color of
        # their own: DEFAULT and IDENTIFIER are both black in every lexer.
        # This scheme keeps that flat look. Only the Python built-ins keep
        # their purple (BUILTINS #880088).
        "func_decl": "#000000", "func_call": "#000000", "func_builtin": "#880088",
        "arg_label": "#000000", "param": "#000000", "init": "#000000",
        "accessor": "#000000", "shorthand": "#000080",
        # Notepad++ has no variable color. This navy is the OPERATOR navy of
        # the default styler, and it is a choice, not a record.
        "var": "#000000", "var_decl": "#000000", "member": "#000000",
        "var_project": "#000080",
        # OPERATOR covers the braces and the separators. It is navy and bold.
        "punct": "#000080", "brace": "#000080", "continuation": "#000080",
        "label": "#804000",
        # The ERROR styles of the lexers: black on a light orange.
        "invalid_fg": "#000000", "invalid_bg": "#FFA448",
        # "Mark Style 3", the yellow marker.
        "deprecated_bg": "#FFFF00",
        # The markup colors come from the txt2tags lexer, the one lexer of
        # Notepad++ that styles prose.
        "head": "#E20700", "bold": "#445675", "italic": "#653A39",
        "link": "#0930DE", "raw": "#009F00", "raw_bg": "#F3F3F3",
        "list_punct": "#E300EE", "quote": "#015F52",
        # The diff colors come from the "diff file" lexer: ADDED is blue,
        # DELETED is olive, and POSITION is orange. The lexer gives no
        # background, therefore these tints are mixed. "Changed" comes from
        # the ErrorList lexer (DIFF Changed).
        "diff_add_fg": "#0080FF", "diff_add_bg": "#E4F0FF",
        "diff_del_fg": "#808040", "diff_del_bg": "#F4F4E4",
        "diff_chg_fg": "#FF0080", "diff_chg_bg": "#FFE8F2",
        # JSON "PROPERTY NAME" is purple. XML "TAG" is blue and "ATTRIBUTE"
        # is red.
        "key": "#8000FF", "tag": "#0000FF", "tag_attr": "#FF0000",
        # The five mark styles of Notepad++. The yellow marker (#FFFF00) is
        # invisible on white as text, therefore this role uses a dark yellow.
        "reg_red": "#FF0000", "reg_orange": "#FF8000", "reg_yellow": "#8A6D00",
        "reg_green": "#008000", "reg_blue": "#0080FF", "reg_purple": "#8000FF",
        "reg_pink": "#FF0080",
    },
    "styles": {
        # fontStyle="1" in the styler means bold. INSTRUCTION WORD, OPERATOR
        # and COMMENT DOC KEYWORD carry it. The comments do not.
        "comment": None, "doc": None, "doc_key": "bold", "codetag": "bold",
        "keyword": "bold", "self": "bold", "const_lang": "bold",
        "operator_decl": "bold", "preproc": None, "attribute": "italic",
        "type": None, "func_decl": None, "func_call": None, "param": None,
        "init": None, "head": "bold", "bold": "bold", "italic": "italic",
        "bold_italic": "bold italic", "underline": "underline",
        "quote": "italic", "tag": None,
    },
    "popup": "html { background-color: #FFFFFF; color: #000000; "
             "border: 1px solid #A0A0A0; } a { color: #0930DE; }",
}

def palette_variant(base, name, note, color_overrides, style_overrides=None):
    """Create a palette without letting variants share mutable dictionaries."""
    colors = dict(base["colors"])
    colors.update(color_overrides)
    styles = dict(base["styles"])
    styles.update(style_overrides or {})
    return {
        "name": name,
        "note": note,
        "colors": colors,
        "styles": styles,
        "popup": base["popup"],
    }


# Visual Studio 2019's Enhanced C++ preset is the historical source for these
# colors. The roles are intentionally language-neutral here: JetBrains, Zed,
# and Sublime apply the same distinction to every grammar that exposes an
# equivalent function, variable, type, keyword, or literal role.
VS_ENHANCED_LIGHT = palette_variant(
    VS2012_LIGHT,
    "Visual Studio Enhanced Light",
    "VS Enhanced Light — brown functions, navy locals, gray parameters, purple control flow and macros",
    {
        "comment": "#008000", "doc": "#008000", "doc_key": "#008000",
        "codetag": "#008000",
        "string": "#A31515", "string_raw": "#A31515", "char": "#0000FF",
        "escape": "#B776FB", "interp_punct": "#B776FB", "interp_fg": "#000000",
        "interp_bg": "#FDF5F3", "regexp": "#811F3F", "regexp_op": "#D16969",
        "number": "#098658", "const_lang": "#0000FF", "const_other": "#000000",
        "enum_member": "#098658",
        "keyword": "#0000FF", "keyword_control": "#8F08C4", "module": "#000000",
        "storage_type": "#0000FF", "storage_mod": "#0000FF", "self": "#0000FF",
        "operator_word": "#0000FF", "operator": "#000000", "operator_decl": "#000000",
        "preproc": "#808080", "macro": "#8A1BFF", "preproc_inactive": "#808080",
        "directive_value": "#000000", "attribute": "#808080", "attr_option": "#8A1BFF",
        "type": "#2B91AF", "type_lib": "#2B91AF", "type_alias": "#2B91AF",
        "generic": "#2B91AF", "type_punct": "#2B91AF",
        "func_decl": "#74531F", "func_call": "#74531F", "func_builtin": "#74531F",
        "func_global_decl": "#74531F", "func_global_call": "#74531F",
        "func_member_decl": "#74531F", "func_member_call": "#74531F",
        "arg_label": "#808080", "param": "#808080", "init": "#74531F",
        "accessor": "#0000FF", "shorthand": "#1F377F",
        "var": "#1F377F", "var_decl": "#1F377F", "var_local": "#1F377F",
        "var_global": "#000000", "member": "#000000", "member_static": "#000000",
        "var_project": "#1F377F",
    },
    {
        "comment": None, "doc": None, "doc_key": None, "codetag": "bold",
        "self": None, "param": None,
    },
)

VS_ENHANCED_GLOBALS_MEMBERS_LIGHT = palette_variant(
    VS_ENHANCED_LIGHT,
    "Visual Studio Enhanced (Globals vs. Members) Light",
    "VS Enhanced Globals vs. Members Light — magenta globals, brown members, and navy locals",
    {
        # Microsoft published the preset as a screenshot rather than a token
        # table. This dark pink is reconstructed from that official image.
        "func_decl": "#B20A5B", "func_call": "#B20A5B",
        "func_global_decl": "#B20A5B", "func_global_call": "#B20A5B",
        "func_member_decl": "#74531F", "func_member_call": "#74531F",
        "const_other": "#B20A5B", "var_global": "#B20A5B",
        "member": "#74531F", "member_static": "#74531F", "var_project": "#B20A5B",
    },
)


# A deliberate Win32 polyglot rather than a historical reconstruction. VC6
# supplies blue reserved words and compiler directives plus green comments;
# VB6 supplies maroon strings and purple literals; and the Borland side
# supplies teal declarations and italic text. The palette stays inside the
# saturated Windows system-color cube, with a Windows 98 selection bar.
BORLAND_DELPHI_VB6_PLUS_PLUS = palette_variant(
    VC6,
    "Borland Delphi VB6++",
    "Borland Delphi VB6++ — Win32 Polyglot remix",
    {
        # Windows editor surface
        "g_sel": "#0A246A", "g_sel_fg": "#FFFFFF",
        "g_sel_border": "#0A246A", "g_inactive_sel": "#D4D0C8",
        "g_inactive_sel_fg": "#000000", "g_accent": "#000080",
        "g_highlight": "#000080", "g_find": "#D4DAEC",
        "g_fold": "#D4DAEC", "g_brackets": "#000080",
        "g_tags": "#000080",

        # VC6 comments, VB6 literals
        "comment": "#008000", "doc": "#008000", "doc_key": "#006060",
        "codetag": "#006060",
        "string": "#800000", "string_raw": "#800000", "char": "#800000",
        "escape": "#800080", "interp_punct": "#800080",
        "interp_fg": "#000000", "interp_bg": "#FAF6F6",
        "regexp": "#800000", "regexp_op": "#800080",
        "number": "#800080", "const_lang": "#800080",
        "const_other": "#800080", "enum_member": "#800080",

        # VC6 reserved words and directives, Delphi types
        "keyword": "#0000FF", "keyword_control": "#0000FF",
        "module": "#008080", "storage_type": "#0000FF",
        "storage_mod": "#0000FF", "self": "#0000FF",
        "operator_word": "#0000FF", "operator": "#000000",
        "operator_decl": "#000080",
        "preproc": "#0000FF", "macro": "#800080",
        "preproc_inactive": "#808080", "directive_value": "#000080",
        "attribute": "#800080", "attr_option": "#800080",
        "type": "#008080", "type_lib": "#006060",
        "type_alias": "#008080", "generic": "#800080",
        "type_punct": "#008080", "type_fallback": "#008080",

        # Semantic identifiers
        "func_decl": "#000080", "func_call": "#000080",
        "func_builtin": "#000080",
        "func_global_decl": "#000080", "func_global_call": "#000080",
        "func_member_decl": "#000080", "func_member_call": "#000080",
        "arg_label": "#606060", "param": "#606060", "init": "#000080",
        "accessor": "#0000FF", "shorthand": "#800080",
        "var": "#000000", "var_decl": "#000000", "var_local": "#000000",
        "var_global": "#800000", "member": "#006060",
        "member_static": "#800080", "var_project": "#000000",

        # Markup and structured data follow the same semantic families
        "head": "#000080", "link": "#0000FF", "raw": "#800000",
        "raw_bg": "#FAF6F6", "list_punct": "#000080", "quote": "#008000",
        "key": "#006060", "tag": "#008080", "tag_attr": "#800000",

        # Changed lines and warning regions use the blue/purple family too.
        "diff_chg_fg": "#000080", "diff_chg_bg": "#E8EEF8",
        "reg_orange": "#800000", "reg_yellow": "#800080",
    },
    {
        "comment": "italic", "doc": "italic", "doc_key": "italic",
        "codetag": "italic", "keyword": None, "self": None,
        "const_lang": None, "param": "italic", "head": None,
        "bold": None, "bold_italic": "italic",
    },
)


SCHEMES = [VS2012_LIGHT, VS_ENHANCED_LIGHT, VS_ENHANCED_GLOBALS_MEMBERS_LIGHT,
           DELPHI, TP, TCPP, XCODE, VB6, VC6, BORLAND_DELPHI_VB6_PLUS_PLUS, BCB,
           ECLIPSE, VS2012_DARK, IDEA, EMACS, VIM, CW, NPP]

# The side view with the line numbers uses the editor background. The line
# numbers must sit on the same paper as the code. This loop keeps the two
# colors equal in all schemes, therefore they cannot become different.
for _scheme in SCHEMES:
    # Most editors color a macro like its compiler directive. Visual Studio
    # 2012 is the exception and defines its historical purple explicitly.
    _scheme["colors"].setdefault("macro", _scheme["colors"]["preproc"])
    _scheme["colors"].setdefault("func_global_decl", _scheme["colors"]["func_decl"])
    _scheme["colors"].setdefault("func_global_call", _scheme["colors"]["func_call"])
    _scheme["colors"].setdefault("func_member_decl", _scheme["colors"]["func_decl"])
    _scheme["colors"].setdefault("func_member_call", _scheme["colors"]["func_call"])
    _scheme["colors"].setdefault("var_local", _scheme["colors"]["var"])
    _scheme["colors"].setdefault("var_global", _scheme["colors"]["var"])
    _scheme["colors"].setdefault("member_static", _scheme["colors"]["const_other"])
    _scheme["colors"].setdefault("type_fallback", _scheme["colors"]["type"])
    _scheme["colors"]["g_gutter"] = _scheme["colors"]["g_bg"]

# --------------------------------------------------------------------------
# Generator
# --------------------------------------------------------------------------


def check(scheme):
    """Make sure the scheme gives a color for every role that the rules use."""
    colors, styles = scheme["colors"], scheme["styles"]
    for _, name, _, fg, bg, st in RULES:
        for role in (fg, bg):
            if role and role not in colors:
                raise SystemExit("%s: no color for role %r (rule %r)"
                                 % (scheme["name"], role, name))
            if role and colors[role] is None:
                raise SystemExit("%s: role %r is None, but rule %r needs a color"
                                 % (scheme["name"], role, name))
        if st and st not in styles:
            raise SystemExit("%s: no style for role %r (rule %r)"
                             % (scheme["name"], st, name))
    for _, template in GLOBALS:
        if template.startswith("{"):
            role = template[1:-1]
            if role not in colors:
                raise SystemExit("%s: no color for global role %r"
                                 % (scheme["name"], role))


def check_same_roles():
    """All schemes must name the same roles. The first scheme sets the list.

    check() only looks at the roles that the rules use. A role that no rule
    uses can go missing from one scheme, and no one sees it until a new rule
    asks for it. This test finds that condition now.
    """
    first = SCHEMES[0]
    for group in ("colors", "styles"):
        want = set(first[group])
        for scheme in SCHEMES[1:]:
            extra = set(scheme[group]) - want
            missing = want - set(scheme[group])
            if extra or missing:
                raise SystemExit(
                    "%s: %s do not agree with %s (extra: %s, missing: %s)"
                    % (scheme["name"], group, first["name"],
                       sorted(extra) or "none", sorted(missing) or "none"))


def check_no_duplicate_scopes():
    """No scope selector can be in two rules.

    Two rules with the same selector have the same weight. Sublime then keeps
    the last rule, and the color of the first rule never shows.
    """
    where = {}
    for _, name, scope, _, _, _ in RULES:
        for part in (p.strip() for p in scope.split(",")):
            if part in where:
                raise SystemExit("scope %r is in both %r and %r"
                                 % (part, where[part], name))
            where[part] = name


def wrap_scope(scope):
    """Scopes stay on one line: JSON strings must not contain real newlines."""
    return '"%s"' % ", ".join(p.strip() for p in scope.split(","))


def render(scheme):
    colors, styles = scheme["colors"], scheme["styles"]
    out = []
    out.append("{")
    out.append('    // %s' % scheme["note"])
    out.append('    // Generated from the shared rule set. All schemes in this folder')
    out.append('    // carry the same rule names and the same scopes.')
    out.append('    "name": "%s",' % scheme["name"])
    out.append('    "author": "%s",' % AUTHOR)

    # variables
    out.append('    "variables":')
    out.append("    {")
    live = [k for k in colors if colors[k] is not None]
    width = max(len(k) for k in live) + 3
    for key in live:
        out.append('        %-*s "%s",' % (width, '"%s":' % key, colors[key]))
    out[-1] = out[-1].rstrip(",")
    out.append("    },")
    out.append("")

    # globals
    out.append('    "globals":')
    out.append("    {")
    gwidth = max(len(k) for k, _ in GLOBALS) + 3
    for key, template in GLOBALS:
        if template.startswith("{"):
            # A role set to None means "leave this global out".
            if colors[template[1:-1]] is None:
                continue
            out.append('        %-*s "var(%s)",'
                       % (gwidth, '"%s":' % key, template[1:-1]))
        else:
            # Every global value must be a string, and the widths are no
            # exception. Sublime refuses the file with "globals values must be
            # strings" if you write a bare number. Keep the quotes.
            out.append('        %-*s "%s",' % (gwidth, '"%s":' % key, template))
    out.append('        "popup_css": "%s"' % scheme["popup"])
    out.append("    },")
    out.append("")

    # rules
    out.append('    "rules":')
    out.append("    [")
    group = None
    entries = []
    for g, name, scope, fg, bg, st in RULES:
        block = []
        if g != group:
            group = g
            dashes = "-" * max(4, 62 - len(g))
            block.append("        // ---------- %s %s" % (g, dashes))
        block.append("        {")
        block.append('            "name": %s,' % ('"%s"' % name))
        block.append('            "scope": %s,' % wrap_scope(scope))
        props = ['            "foreground": "var(%s)"' % fg]
        if bg:
            props.append('            "background": "var(%s)"' % bg)
        style = styles.get(st) if st else None
        if style:
            props.append('            "font_style": "%s"' % style)
        block.append(",\n".join(props))
        block.append("        }")
        entries.append("\n".join(block))
    out.append(",\n".join(entries))
    out.append("    ]")
    out.append("}")
    return "\n".join(out) + "\n"


def check_all():
    """Run every test on the rule set and on all palettes."""
    check_same_roles()
    check_no_duplicate_scopes()
    for scheme in SCHEMES:
        check(scheme)


def main():
    check_all()
    os.makedirs(OUT, exist_ok=True)
    for scheme in SCHEMES:
        path = os.path.join(OUT, scheme["name"] + ".sublime-color-scheme")
        with open(path, "w") as fh:
            fh.write(render(scheme))
        print("wrote %s (%d rules)" % (path, len(RULES)))


# The write step stays behind this guard, so that build_xcode_themes.py can
# import SCHEMES without writing any file.
if __name__ == "__main__":
    main()
