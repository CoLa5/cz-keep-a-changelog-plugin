#!/usr/bin/env python3
"""Make docs."""

import itertools
import pathlib
import shutil
import textwrap
from typing import Final

import pdoc.render

import cz_keep_a_changelog_plugin

HERE: Final[pathlib.Path] = pathlib.Path(__file__).parent
DOC_URL: Final[str] = "https://cola5.github.io/cz-keep-a-changelog-plugin"
GIT_URL: Final[str] = "https://github.com/CoLa5/cz-keep-a-changelog-plugin"


def write_sitemap(path: pathlib.Path) -> None:  # noqa: D103
    with (path / "sitemap.xml").open("w", newline="\n") as f:
        header = """
            <?xml version="1.0" encoding="utf-8"?>
            <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
            """
        f.write(textwrap.dedent(header).strip())
        for file in path.glob("**/*.html"):
            if file.name.startswith("_"):
                continue
            filename = (
                file.relative_to(path).as_posix().replace("index.html", "")
            )
            f.write(f"""\n<url><loc>{DOC_URL:s}/{filename:s}</loc></url>""")
        f.write("""\n</urlset>""")


if __name__ == "__main__":
    pdoc.render.configure(
        docformat="google",
        edit_url_map={
            "cz_keep_a_changelog_plugin": (
                f"{GIT_URL:s}/blob/main/cz_keep_a_changelog_plugin/"
            ),
        },
        favicon="assets/favicon.svg",
        footer_text=(
            f'<a href="{GIT_URL:s}/releases/tag/'
            f'v{cz_keep_a_changelog_plugin.__version__:s}">'
            f"cz_keep_a_changelog_plugin "
            f"<b>v{cz_keep_a_changelog_plugin.__version__:s}</b>"
            f"</a>"
        ),
        logo="assets/logo.svg",
        logo_link=DOC_URL,
        search=True,
        template_directory=HERE / "pdoc_template",
    )
    output = HERE / ".." / "public"
    output.mkdir(exist_ok=True)
    pdoc.pdoc(
        HERE / ".." / "cz_keep_a_changelog_plugin",
        output_directory=output,
    )
    # Remove unnecessary forwarding index
    (output / "cz_keep_a_changelog_plugin.html").replace(output / "index.html")

    write_sitemap(output)

    # Copy icons
    (output / "assets").mkdir(exist_ok=True)
    for name, suffix in itertools.product(
        ("favicon", "logo"),
        (".png", ".svg"),
    ):
        filename = name + suffix
        shutil.copy2(
            HERE / "icons" / filename,
            output / "assets" / filename,
        )
    # Copy robots.txt
    shutil.copy2(HERE / "robots.txt", output / "robots.txt")
