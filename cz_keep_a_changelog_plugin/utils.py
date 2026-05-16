"""Utils."""

import re

import jinja2 as j2

MD_LINK_PATTERN: re.Pattern[str] = re.compile(r"\[[^\]]*\]\([^)]+\)")
GH_ISSUE_PATTERN: re.Pattern[str] = re.compile(r"(?<!\w)#(?P<issue_num>\d+)\b")


def replace_github_issues(
    text: str,
    issue_url_template: j2.Template,
) -> str:
    """Replace GitHub issue numbers `"#123"` by a corresponding markdown link.

    Notes:
        Ignores GitHub issue numbers in markdown links.

    Args:
        text: The text to replace the GitHub issue numbers in.
        issue_url_template: The issue URL template (`issue` will be replaced by
            the issue number).

    Returns:
        The text with replaced GitHub issue numbers.
    """
    link_spans: list[tuple[int, int]] = [
        (m.start(), m.end()) for m in MD_LINK_PATTERN.finditer(text)
    ]
    link_spans.sort()

    out = []
    i_link = 0
    i_text = 0

    for m in GH_ISSUE_PATTERN.finditer(text):
        start, end = m.span()
        while i_link < len(link_spans) and link_spans[i_link][1] <= start:
            i_link += 1
        # Skip in case of overlap with link
        if (
            i_link < len(link_spans)
            and link_spans[i_link][0] <= start < link_spans[i_link][1]
        ):
            continue
        # Append text inbetween
        out.append(text[i_text:start])
        # Append issue url
        issue_num = m.group("issue_num")
        issue_url = issue_url_template.render(issue=issue_num)
        out.append(f"[#{issue_num:s}]({issue_url:s})")
        # Set start of next text part to end
        i_text = end

    out.append(text[i_text:])
    return "".join(out)
