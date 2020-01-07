from nbconvert.preprocessors import Preprocessor


class WrapHtmlPreprocessor(Preprocessor):
    """
    Wraps html ouput from cells in the shortcode `rawhtml`.

    The `rawhtml` shortcode is a file which should be placed in `layouts/shortcodes/rawhtml.html` with this contents:

        <!-- raw html -->
        {{.Inner}}

    Hugo starting from version 0.60 (see discussion: https://discourse.gohugo.io/t/raw-html-getting-omitted-in-0-60-0/22032)
    doesn't render html tags by default, it needs the `unsafe = true` flag instead.

    However, it doesn't handle blocks of HTML very well even if `unsafe = true` in the config.toml and the approach of
    having a shortcode works better.
    """

    def preprocess_cell(self, cell, resources, index):
        outputs = cell.get("outputs", [])
        for output in outputs:
            data = output.get("data", {})
            if "text/html" in data:
                data["text/html"] = (
                    "{{< rawhtml >}}\n" + data["text/html"] + "\n{{< /rawhtml >}}"
                )
        return cell, resources
