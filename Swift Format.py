#!/usr/bin/env python
# coding: utf-8
#
# Swift Format.py
#
# AGPLv3 License
# Created by github.com/aerobounce on 2020/07/19.
# Copyright © 2020 to Present, aerobounce. All rights reserved.
#

import html
import re
from subprocess import PIPE, Popen

import sublime
import sublime_plugin

SETTINGS_FILENAME = "Swift Format.sublime-settings"
PHANTOM_STYLE = """
<style>
    div.error-arrow {
        border-top: 0.4rem solid transparent;
        border-left: 0.5rem solid color(var(--redish) blend(var(--background) 30%));
        width: 0;
        height: 0;
    }
    div.error {
        padding: 0.4rem 0 0.4rem 0.7rem;
        margin: 0 0 0.2rem;
        border-radius: 0 0.2rem 0.2rem 0.2rem;
    }
    div.error span.message {
        padding-right: 0.7rem;
    }
    div.error a {
        text-decoration: inherit;
        padding: 0.35rem 0.7rem 0.45rem 0.8rem;
        position: relative;
        bottom: 0.05rem;
        border-radius: 0 0.2rem 0.2rem 0;
        font-weight: bold;
    }
    html.dark div.error a {
        background-color: #00000018;
    }
    html.light div.error a {
        background-color: #ffffff18;
    }
</style>
"""
PHANTOM_SETS = {}


def update_phantoms(view, stderr, region):
    view_id = view.id()

    view.erase_phantoms(str(view_id))
    if view_id in PHANTOM_SETS:
        PHANTOM_SETS.pop(view_id)

    if not stderr or not "Unexpected" in stderr:
        return

    if not view_id in PHANTOM_SETS:
        PHANTOM_SETS[view_id] = sublime.PhantomSet(view, str(view_id))

    # Extract line and column
    digits = re.compile(r"\d+|$").findall(stderr)
    line = int(digits[0]) - 1
    column = int(digits[1]) - 1

    if region:
        line += view.rowcol(region.begin())[0]

    # Format error message
    pattern = "Running SwiftFormat...\nerror: "
    stderr = re.compile(pattern).sub("", stderr)

    # Func to hook with `on_navigate`
    def erase_phantom(self):
        view.erase_phantoms(str(view_id))

    phantoms = []
    point = view.text_point(line, column)
    region = sublime.Region(point, view.line(point).b)
    phantoms.append(
        sublime.Phantom(
            region,
            (
                "<body id=inline-error>"
                + PHANTOM_STYLE
                + '<div class="error-arrow"></div><div class="error">'
                + '<span class="message">'
                + html.escape(stderr, quote=False)
                + "</span>"
                + "<a href=hide>"
                + chr(0x00D7)
                + "</a></div>"
                + "</body>"
            ),
            sublime.LAYOUT_BELOW,
            on_navigate=erase_phantom,
        )
    )
    PHANTOM_SETS[view_id].update(phantoms)

    # Scroll to the syntax error point
    if sublime.load_settings(SETTINGS_FILENAME).get("scroll_to_error_point"):
        view.sel().clear()
        view.sel().add(sublime.Region(point))
        view.show_at_center(point)


def swiftformat(view, edit, use_selection):
    # Load settings file
    settings = sublime.load_settings(SETTINGS_FILENAME)

    # Get bin path
    swiftformat_bin_path = "{} ".format(settings.get("swiftformat_bin_path"))

    # Get option values
    swiftversion_value     = settings.get("swiftversion")
    rules_value            = settings.get("rules")
    disable_value          = settings.get("disable")
    # enable_value           = settings.get("enable")
    allman_value           = settings.get("allman")
    binarygrouping_value   = settings.get("binarygrouping")
    closingparen_value     = settings.get("closingparen")
    commas_value           = settings.get("commas")
    decimalgrouping_value  = settings.get("decimalgrouping")
    elseposition_value     = settings.get("elseposition")
    empty_value            = settings.get("empty")
    exponentcase_value     = settings.get("exponentcase")
    exponentgrouping_value = settings.get("exponentgrouping")
    fractiongrouping_value = settings.get("fractiongrouping")
    header_value           = settings.get("header")
    hexgrouping_value      = settings.get("hexgrouping")
    hexliteralcase_value   = settings.get("hexliteralcase")
    ifdef_value            = settings.get("ifdef")
    importgrouping_value   = settings.get("importgrouping")
    indent_value           = settings.get("indent")
    indentcase_value       = settings.get("indentcase")
    linebreaks_value       = settings.get("linebreaks")
    maxwidth_value         = settings.get("maxwidth")
    nospaceoperators_value = settings.get("nospaceoperators")
    nowrapoperators_value  = settings.get("nowrapoperators")
    octalgrouping_value    = settings.get("octalgrouping")
    operatorfunc_value     = settings.get("operatorfunc")
    patternlet_value       = settings.get("patternlet")
    _self_value            = settings.get("self")
    selfrequired_value     = settings.get("selfrequired")
    semicolons_value       = settings.get("semicolons")
    shortoptionals_value   = settings.get("shortoptionals")
    specifierorder_value   = settings.get("specifierorder")
    stripunusedargs_value  = settings.get("stripunusedargs")
    tabwidth_value         = settings.get("tabwidth")
    trailingclosures_value = settings.get("trailingclosures")
    trimwhitespace_value   = settings.get("trimwhitespace")
    wraparguments_value    = settings.get("wraparguments")
    wrapcollections_value  = settings.get("wrapcollections")
    wrapparameters_value   = settings.get("wrapparameters")
    xcodeindentation_value = settings.get("xcodeindentation")

    # Prepare options
    swiftversion           = "--swiftversion {} ".format(swiftversion_value)         if swiftversion_value else ""
    rules                  = "--rules {} ".format(rules_value)                       if rules_value else ""
    disable                = "--disable {} ".format(disable_value)                   if disable_value else ""
    # enable                 = "--enable {} ".format(enable_value)                     if enable_value else ""
    allman                 = "--allman {} ".format(allman_value)                     if allman_value else ""
    binarygrouping         = "--binarygrouping {} ".format(binarygrouping_value)     if binarygrouping_value else ""
    closingparen           = "--closingparen {} ".format(closingparen_value)         if closingparen_value else ""
    commas                 = "--commas {} ".format(commas_value)                     if commas_value else ""
    decimalgrouping        = "--decimalgrouping {} ".format(decimalgrouping_value)   if decimalgrouping_value else ""
    elseposition           = "--elseposition {} ".format(elseposition_value)         if elseposition_value else ""
    empty                  = "--empty {} ".format(empty_value)                       if empty_value else ""
    exponentcase           = "--exponentcase {} ".format(exponentcase_value)         if exponentcase_value else ""
    exponentgrouping       = "--exponentgrouping {} ".format(exponentgrouping_value) if exponentgrouping_value else ""
    fractiongrouping       = "--fractiongrouping {} ".format(fractiongrouping_value) if fractiongrouping_value else ""
    header                 = "--header {} ".format(header_value)                     if header_value else ""
    hexgrouping            = "--hexgrouping {} ".format(hexgrouping_value)           if hexgrouping_value else ""
    hexliteralcase         = "--hexliteralcase {} ".format(hexliteralcase_value)     if hexliteralcase_value else ""
    ifdef                  = "--ifdef {} ".format(ifdef_value)                       if ifdef_value else ""
    importgrouping         = "--importgrouping {} ".format(importgrouping_value)     if importgrouping_value else ""
    indent                 = "--indent {} ".format(indent_value)                     if indent_value else ""
    indentcase             = "--indentcase {} ".format(indentcase_value)             if indentcase_value else ""
    linebreaks             = "--linebreaks {} ".format(linebreaks_value)             if linebreaks_value else ""
    maxwidth               = "--maxwidth {} ".format(maxwidth_value)                 if maxwidth_value else ""
    nospaceoperators       = "--nospaceoperators {} ".format(nospaceoperators_value) if nospaceoperators_value else ""
    nowrapoperators        = "--nowrapoperators {} ".format(nowrapoperators_value)   if nowrapoperators_value else ""
    octalgrouping          = "--octalgrouping {} ".format(octalgrouping_value)       if octalgrouping_value else ""
    operatorfunc           = "--operatorfunc {} ".format(operatorfunc_value)         if operatorfunc_value else ""
    patternlet             = "--patternlet {} ".format(patternlet_value)             if patternlet_value else ""
    _self                  = "--_self {} ".format(_self_value)                       if _self_value else ""
    selfrequired           = "--selfrequired {} ".format(selfrequired_value)         if selfrequired_value else ""
    semicolons             = "--semicolons {} ".format(semicolons_value)             if semicolons_value else ""
    shortoptionals         = "--shortoptionals {} ".format(shortoptionals_value)     if shortoptionals_value else ""
    specifierorder         = "--specifierorder {} ".format(specifierorder_value)     if specifierorder_value else ""
    stripunusedargs        = "--stripunusedargs {} ".format(stripunusedargs_value)   if stripunusedargs_value else ""
    tabwidth               = "--tabwidth {} ".format(tabwidth_value)                 if tabwidth_value else ""
    trailingclosures       = "--trailingclosures {} ".format(trailingclosures_value) if trailingclosures_value else ""
    trimwhitespace         = "--trimwhitespace {} ".format(trimwhitespace_value)     if trimwhitespace_value else ""
    wraparguments          = "--wraparguments {} ".format(wraparguments_value)       if wraparguments_value else ""
    wrapcollections        = "--wrapcollections {} ".format(wrapcollections_value)   if wrapcollections_value else ""
    wrapparameters         = "--wrapparameters {} ".format(wrapparameters_value)     if wrapparameters_value else ""
    xcodeindentation       = "--xcodeindentation {} ".format(xcodeindentation_value) if xcodeindentation_value else ""


    # Compose swiftformat command
    command = (
        swiftformat_bin_path
        + swiftversion
        + rules
        + disable
        # + enable
        + allman
        + binarygrouping
        + closingparen
        + commas
        + decimalgrouping
        + elseposition
        + empty
        + exponentcase
        + exponentgrouping
        + fractiongrouping
        + header
        + hexgrouping
        + hexliteralcase
        + ifdef
        + importgrouping
        + indent
        + indentcase
        + linebreaks
        + maxwidth
        + nospaceoperators
        + nowrapoperators
        + octalgrouping
        + operatorfunc
        + patternlet
        + _self
        + selfrequired
        + semicolons
        + shortoptionals
        + specifierorder
        + stripunusedargs
        + tabwidth
        + trailingclosures
        + trimwhitespace
        + wraparguments
        + wrapcollections
        + wrapparameters
        + xcodeindentation
    )

    # Format

    def format_text(target_text, selection, region):
        # Open subprocess with the command
        with Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) as popen:
            # Write selection into stdin, then ensure the descriptor is closed
            popen.stdin.write(target_text.encode("utf-8"))
            popen.stdin.close()

            # Read stdout and stderr
            stdout = popen.stdout.read().decode("utf-8")
            stderr = popen.stderr.read().decode("utf-8")

            # Catch some keywords in stderr
            command_succeeded = "successfully" in stderr
            syntax_error = "Unexpected" in stderr

            # Replace with the result only if no error has been caught
            if command_succeeded:
                view.replace(edit, selection, stdout)

            # Present alert: `swiftformat` not found
            if "not found" in stderr:
                sublime.error_message(
                    "SwiftFormat - Error:\n"
                    + stderr
                    + "Specify absolute path to 'swiftformat' in settings"
                )
                return command_succeeded

            # Present alert: Unknown error
            if not command_succeeded and not syntax_error:
                sublime.error_message("SwiftFormat - Error:\n" + stderr)
                return command_succeeded

            # Update Phantoms
            update_phantoms(view, stderr, region)

            return command_succeeded

    # Prevent needles iteration AMAP
    has_selection = any([not r.empty() for r in view.sel()])
    if (settings.get("format_selection_only") or use_selection) and has_selection:
        for region in view.sel():
            if region.empty():
                continue

            # Break at the first error
            if not format_text(view.substr(region), region, region):
                break

    else:
        # Don't format entire file when use_selection is true
        if use_selection:
            return

        # Use entire region/string of view
        selection = sublime.Region(0, view.size())
        target_text = view.substr(selection)
        format_text(target_text, selection, None)


class SwiftFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        swiftformat(self.view, edit, False)


class SwiftFormatSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        swiftformat(self.view, edit, True)


class SwiftFormatListener(sublime_plugin.ViewEventListener):
    def on_pre_save(self):
        if self.view.window().extract_variables()["file_extension"] == "swift":
            if sublime.load_settings(SETTINGS_FILENAME).get("format_on_save"):
                self.view.run_command("swift_format")

    def on_close(self):
        view_id = self.view.id()
        if view_id in PHANTOM_SETS:
            PHANTOM_SETS.pop(view_id)
