## ⚡️ Swift Format

> Swift Formatter / Syntax Checker for Sublime Text 3<br>

<table width="100%" style="border-spacing: 0px;">
<tr>
    <th><b>⚡️ Blazingly Fast Formatting</b></th>
    <th><b>❗️ User Friendly Syntax Error Indicator</a></b></th>
</tr>
<tr>
    <td colspan="2" style="padding: 0px; margin: 0px;">
        <img src="https://user-images.githubusercontent.com/10491362/87870544-01507d00-c9e4-11ea-9fa1-1f7eb4b5bb20.gif" style="display: block; width: 100%;" />
    </td>
</tr>
</table>

### 📦 Install via Package Control

> Installation via Package Control is not available at the moment (Waiting for merge).

### 📦 Manual Install

1. Clone this repository as shown below (**Note that target directory name has to be `Swift Format`**)
2. You're ready (Restart Sublime Text if the package is not recognized)

```sh
cd "$HOME/Library/Application Support/Sublime Text 3/Packages"
git clone https://github.com/aerobounce/Sublime-Swift-Format.git "Swift Format"
```

### ⚠️ Dependency

- Swift Format does not work without **`swiftformat`** as this package utilizes the formatter.
    - You can easily install it with **Homebrew**: **`brew install swiftformat`**
    - For more details, visit: [nicklockwood/SwiftFormat][swiftformat]
- If your default shell have the **`PATH`** to **`swiftformat`**, you can start using this plugin.
- If that is not the case, specify the **Absolute PATH** in the settings:
```JavaScript
{
    "swiftformat_bin_path": "PATH to swiftformat"
}
```

### 📝 Available Commands

| Caption                                   | Command                         | Default Key Bindings |
| ----------------------------------------- | ------------------------------- | -------------------- |
| <kbd>Swift Format: Format</kbd>           | `swift_format`                  | None                 |
| <kbd>Swift Format: Format Selection</kbd> | `swift_format_selection`        | None                 |

- **Command** is the name of the command you can use for **Key-Bindings**.
- Be aware that any manual modifications with `Format Selection` might be lost upon saving a file if `format_on_save` is `true`, which it is by default.

### 🛠 Default Settings

```javascript
{
    /*
        Swift Format
    */
    "swiftformat_bin_path": "swiftformat",
    "format_on_save": true,         // Invoke "Swift Format: Format" command on save
    "format_selection_only": false, // Entire file will be used if no selection available
    "scroll_to_error_point": true,  // Scroll to the point error occured

    /*
        SwiftFormat Options
            • Default values will be used even if a value is empty.
                • To use only specific rules, use `rules` key.
            • To disable specific rules, use `disable` key.
                • What you can disable is not `options` listed in this file, but `rules`.
            • To see up-to-date rules: `swiftformat --rules`
    */
    "swiftversion": "",     // The version of Swift used in the files being formatted
    "rules": "",            // The list of rules to apply.
    "disable": "",          // A list of format rules to be disabled (comma-delimited)

    "allman": "",           // Use allman indentation style: "true" or "false" (default)
    "binarygrouping": "",   // Binary grouping,threshold (default: 4,8) or "none", "ignore"
    "closingparen": "",     // Closing paren position: "balanced" (default) or "same-line"
    "commas": "",           // Commas in collection literals: "always" (default) or "inline"
    "decimalgrouping": "",  // Decimal grouping,threshold (default: 3,6) or "none", "ignore"
    "elseposition": "",     // Placement of else/catch: "same-line" (default) or "next-line"
    "empty": "",            // How empty values are represented: "void" (default) or "tuple"
    "exponentcase": "",     // Case of 'e' in numbers: "lowercase" or "uppercase" (default)
    "exponentgrouping": "", // Group exponent digits: "enabled" or "disabled" (default)
    "fractiongrouping": "", // Group digits after '.': "enabled" or "disabled" (default)
    "header": "",           // Header comments: "strip", "ignore", or the text you wish use
    "hexgrouping": "",      // Hex grouping,threshold (default: 4,8) or "none", "ignore"
    "hexliteralcase": "",   // Casing for hex literals: "uppercase" (default) or "lowercase"
    "ifdef": "",            // #if indenting: "indent" (default), "no-indent" or "outdent"
    "importgrouping": "",   // "testable-top", "testable-bottom" or "alphabetized" (default)
    "indent": "",           // Number of spaces to indent, or "tab" to use tabs
    "indentcase": "",       // Indent cases inside a switch: "true" or "false" (default)
    "linebreaks": "",       // Linebreak character to use: "cr", "crlf" or "lf" (default)
    "maxwidth": "",         // Maximum length of a line before wrapping. defaults to "none"
    "nospaceoperators": "", // Comma-delimited list of operators without surrounding space
    "nowrapoperators": "",  // Comma-delimited list of operators that shouldn't be wrapped
    "octalgrouping": "",    // Octal grouping,threshold (default: 4,8) or "none", "ignore"
    "operatorfunc": "",     // Spacing for operator funcs: "spaced" (default) or "no-space"
    "patternlet": "",       // let/var placement in patterns: "hoist" (default) or "inline"
    "self": "",             // Explicit self: "insert", "remove" (default) or "init-only"
    "selfrequired": "",     // Comma-delimited list of functions with @autoclosure arguments
    "semicolons": "",       // Allow semicolons: "never" or "inline" (default)
    "shortoptionals": "",   // Use ? for Optionals "always" (default) or "except-properties"
    "specifierorder": "",   // Comma-delimited list of specifiers in preferred order
    "stripunusedargs": "",  // "closure-only", "unnamed-only" or "always" (default)
    "tabwidth": "",         // The width of a tab character. Defaults to "unspecified"
    "trailingclosures": "", // Comma-delimited list of functions that use trailing closures
    "trimwhitespace": "",   // Trim trailing space: "always" (default) or "nonblank-lines"
    "wraparguments": "",    // Wrap all arguments: "before-first", "after-first", "preserve"
    "wrapcollections": "",  // Wrap array/dict: "before-first", "after-first", "preserve"
    "wrapparameters": "",   // Wrap func params: "before-first", "after-first", "preserve"
    "xcodeindentation": ""  // Xcode indent guard/enum: "enabled" or "disabled" (default)
}
```

### 🤝 Thank you

- [nicklockwood/SwiftFormat][swiftformat] — Swift Format for Sublime Text is powerd by swiftformat, the best Swift formatter available.

[swiftformat]: https://github.com/nicklockwood/SwiftFormat
