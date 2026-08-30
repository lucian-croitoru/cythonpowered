"""Unit tests for cythonpowered.textparse.

Cross-validation against the Python original is the primary strategy:
every function is compared against BeautifulSoup (lxml parser), lxml
directly, or the regex implementations from utils.definitions._textparse
across a range of inputs. Edge cases are covered explicitly: empty
inputs, boundary values (octet 255 vs 256, TLD length 1 vs 2), invalid
or malformed inputs (bare '<' in text, mixed-case tags, empty local
parts), and non-ASCII text (documented ASCII-only behavior where
applicable).

Note on find()/find_all(): these return raw substrings of the input, so
results are compared after normalization: unescape entities (lxml
escapes '<'/'>'/'&' when re-serializing), normalize quotes (bs4 does
this on decode), and sort attributes in the outermost opening tag (bs4
sorts alphabetically, lxml and the raw substring keep document order).
Deep HTML error recovery (implicit end tags, foster parenting) is not
emulated — see README.
"""

import html as html_module
import re

import cythonpowered.textparse as tp
import pytest
from utils.definitions._textparse import (
    py_get_text_bs4,
    py_get_text_lxml,
    py_find_bs4,
    py_findall_bs4,
    py_find_lxml,
    py_findall_lxml,
    py_get_attr_bs4,
    py_get_attr_lxml,
    py_get_ips,
    py_get_emails,
    py_get_mac_addrs,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


def normalize_tag(s):
    """Normalize a tag string so that raw substrings, bs4's
    re-serialization, and lxml's re-serialization compare equal:

    - unescape HTML entities (lxml escapes on re-serialization)
    - normalize single quotes to double quotes (bs4 does this)
    - sort attributes in the outermost opening tag (bs4 sorts
      alphabetically, lxml keeps document order)
    - drop the self-closing slash on void elements (bs4 writes
      <br/>, lxml writes <br>)
    """
    if s is None:
        return None
    s = html_module.unescape(s)
    s = s.replace("'", '"')

    def _sort_attrs(m):
        name = m.group(1)
        attrs = re.findall(r'([\w-]+)="([^"]*)"', m.group(2))
        attrs.sort()
        attr_str = "".join(f' {k}="{v}"' for k, v in attrs)
        slash = "" if name.lower() in _VOID_TAGS else m.group(3)
        return f'<{name}{attr_str}{slash}>'

    return re.sub(
        r'^<([a-zA-Z][\w-]*)((?:\s+[\w-]+\s*=\s*"[^"]*")*)(/?)>',
        _sort_attrs,
        s,
        count=1,
    )


def normalize_tags(lst):
    """Normalize a list of tag strings (None passes through)."""
    if lst is None:
        return None
    return [normalize_tag(t) for t in lst]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

# Well-formed HTML fragments used for cross-validation; all reference
# implementations (cython, bs4, lxml) agree on these.
TEST_HTML = [
    "<p>Hello\n  world</p>",
    "<p>Hello world</p>",
    "<div class='container'>Nested <b>text</b> here</div>",
    "<!-- comment --><p>After comment</p>",
    '<a href="http://example.com?q=1&r=2">Link</a>',
    "<script>alert('xss')</script><p>Safe</p>",
    "<ul><li>Item 1</li><li>Item 2</li></ul>",
    '<input type="text" name="username" value="john"/>',
    "<b>bold</b> <i>italic</i>",
    "<p>First</p><p>Second</p>",
    '<span title="t">x</span><span>y</span>',
    "<table><tr><td>Cell 1</td><td>Cell 2</td></tr></table>",
]

# Tag names exercised by the find()/find_all() cross-validation tests.
FIND_TAGS = ["p", "div", "script", "ul", "li", "input", "span", "b", "i", "table"]


# ---------------------------------------------------------------------------
# html.get_text
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("html", TEST_HTML)
def test_html_get_text_vs_bs4_single(html):
    """get_text matches BeautifulSoup().get_text() on well-formed HTML,
    with and without strip."""
    expected_bs4 = py_get_text_bs4(html)
    expected_lxml = py_get_text_lxml(html)
    actual = tp.html.get_text(html)
    assert actual == expected_bs4
    assert actual == expected_lxml

    expected_stripped = py_get_text_bs4(html, strip=True)
    actual_stripped = tp.html.get_text(html, strip=True)
    assert actual_stripped == expected_stripped


def test_html_get_text_vs_bs4_full():
    """get_text matches BeautifulSoup().get_text() on the concatenation
    of all fixtures (exercises tag boundaries between fragments)."""
    html = "".join(TEST_HTML)
    expected_bs4 = py_get_text_bs4(html)
    expected_lxml = py_get_text_lxml(html)
    actual = tp.html.get_text(html)
    assert actual == expected_bs4
    assert actual == expected_lxml

    expected_stripped = py_get_text_bs4(html, strip=True)
    actual_stripped = tp.html.get_text(html, strip=True)
    assert actual_stripped == expected_stripped


def test_html_get_text_empty():
    """Empty input yields empty text (no crash, no spurious parts)."""
    assert tp.html.get_text("") == ""
    assert tp.html.get_text("", strip=True) == ""


def test_html_get_text_plain_text():
    """Text without tags passes through unchanged."""
    assert tp.html.get_text("plain text 123") == "plain text 123"


@pytest.mark.parametrize("text", [
    "héllo wörld 中文",
    # U+013C: low byte 0x3C == ord('<') — must not be misread as a tag
    "a" + chr(0x13C) + "b",
    # U+013E: low byte 0x3E == ord('>') — must not close a tag
    "a<" + chr(0x13E) + "b",
])
def test_html_get_text_non_ascii(text):
    """Non-ASCII text is preserved, including code points whose low byte
    collides with '<' or '>' (cross-validated against bs4)."""
    assert tp.html.get_text(text) == text
    assert tp.html.get_text(text) == py_get_text_bs4(text)


def test_html_get_text_bare_lt_in_text():
    """A bare '<' not followed by a letter or '/' stays text (HTML5 data
    state); it must not start a tag and swallow the following text."""
    html = "<p>a < b and <div>x</div></p>"
    assert tp.html.get_text(html) == py_get_text_bs4(html)
    assert tp.html.get_text(html) == "a < b and x"


def test_html_get_text_scriptfoo_not_script():
    """<scriptfoo> is not a <script> block (exact tag-name match); its
    content is text, like bs4/lxml."""
    html = "<scriptfoo>alert(1)</scriptfoo><p>ok</p>"
    assert tp.html.get_text(html) == py_get_text_bs4(html)
    assert tp.html.get_text(html) == "alert(1)ok"


def test_html_get_text_comment_only():
    """Comments (closed or not) yield no text."""
    assert tp.html.get_text("<!-- abc -->") == ""
    assert tp.html.get_text("<!-- unclosed") == ""


def test_html_get_text_script_style_dropped():
    """<script>/<style> content is dropped, like bs4/lxml get_text."""
    assert tp.html.get_text("<script>a</script>b") == "b"
    assert tp.html.get_text("<style>.x{}</style>b") == "b"
    # </scriptfoo> must not close a <script> block
    assert tp.html.get_text("<script>a</scriptfoo>b</script>c") == "c"


def test_html_get_text_unclosed_tag():
    """Text inside an unclosed tag is still extracted."""
    assert tp.html.get_text("<div>hello") == "hello"
    assert tp.html.get_text("<div>hello") == py_get_text_bs4("<div>hello")


# ---------------------------------------------------------------------------
# html.find / html.find_all
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tag", FIND_TAGS)
def test_html_find_recursive(tag):
    """find() matches BeautifulSoup().find() and lxml's find() when
    searching recursively (after tag normalization)."""
    html = f'<body>{"".join(TEST_HTML)}</body>'

    expected_bs4 = normalize_tag(py_find_bs4(html, tag, recursive=True))
    actual = normalize_tag(tp.html.find(html, tag, recursive=True))

    html = f'<html><body>{"".join(TEST_HTML)}</body></html>'
    expected_lxml = normalize_tag(py_find_lxml(html, tag, recursive=True))

    assert actual == expected_bs4
    assert actual == expected_lxml


@pytest.mark.parametrize("tag", FIND_TAGS)
def test_html_find_non_recursive(tag):
    """find() with recursive=False matches the references (tags nested
    inside <body> are not top-level, so all references agree on None)."""
    html = f'<body>{"".join(TEST_HTML)}</body>'

    expected_bs4 = normalize_tag(py_find_bs4(html, tag, recursive=False))
    actual = normalize_tag(tp.html.find(html, tag, recursive=False))

    html = f'<html><body>{"".join(TEST_HTML)}</body></html>'
    expected_lxml = normalize_tag(py_find_lxml(html, tag, recursive=False))

    assert actual == expected_bs4
    assert actual == expected_lxml


@pytest.mark.parametrize("tag", FIND_TAGS)
def test_html_findall_recursive(tag):
    """find_all() matches BeautifulSoup().find_all() and lxml's findall()
    when searching recursively (after tag normalization)."""
    html = f'<body>{"".join(TEST_HTML)}</body>'

    expected_bs4 = normalize_tags(py_findall_bs4(html, tag, recursive=True))
    actual = normalize_tags(tp.html.find_all(html, tag, recursive=True))

    html = f'<html><body>{"".join(TEST_HTML)}</body></html>'
    expected_lxml = normalize_tags(py_findall_lxml(html, tag, recursive=True))

    assert actual == expected_bs4
    assert actual == expected_lxml


def test_html_find_case_insensitive():
    """Tag names match case-insensitively (HTML tag names are
    case-insensitive, like BeautifulSoup).

    The raw substring keeps the original case; bs4 and lxml both
    normalize tag names to lowercase in their DOM, so the result is
    asserted directly rather than cross-validated.
    """
    assert tp.html.find('<DIV class="x">y</DIV>', 'div') == '<DIV class="x">y</DIV>'
    assert tp.html.find('<DiV>y</DiV>', 'div') == '<DiV>y</DiV>'
    assert tp.html.find('<IMG src="x">t</IMG>', 'img') == '<IMG src="x">'
    assert tp.html.find('<div>y</div>', 'DIV') == '<div>y</div>'
    assert tp.html.find_all('<div>a</div><DIV>b</div>', 'div') == [
        '<div>a</div>', '<DIV>b</div>',
    ]


def test_html_find_non_ascii_tag():
    """A non-ASCII tag can never match (HTML tag names are ASCII) and
    yields no match instead of raising, like BeautifulSoup."""
    assert tp.html.find('<div>x</div>', 'dév') is None
    assert tp.html.find_all('<div>x</div>', 'dév') == []
    assert py_find_bs4('<div>x</div>', 'dév') is None


def test_html_find_non_ascii_text():
    """Non-ASCII text before/around tags must not corrupt the extracted
    substrings (UTF-8 byte offsets vs code point offsets)."""
    assert tp.html.find("héllo<div>x</div>", "div") == "<div>x</div>"
    assert tp.html.find("café<br>", "br") == "<br>"
    assert tp.html.find_all("héllo<input/> <input a=1/>", "input") == [
        "<input/>", "<input a=1/>",
    ]


def test_html_find_bare_lt_in_text():
    """A bare '<' in text is not a tag, so a following real tag is still
    found (cross-validated against bs4)."""
    html = '<p>a < b and <div>x</div></p>'
    assert tp.html.find(html, 'div') == '<div>x</div>'
    assert normalize_tag(tp.html.find(html, 'div')) == \
        normalize_tag(py_find_bs4(html, 'div'))


def test_html_find_void_wbr():
    """<wbr> and <br> are void elements: find returns the opening tag
    only (there is no closing tag to search for)."""
    assert tp.html.find('<wbr>x</wbr><div>y</div>', 'wbr') == '<wbr>'
    assert tp.html.find('<br>x<br>', 'br') == '<br>'


def test_html_find_self_closing():
    """Explicitly self-closing tags are returned as-is."""
    assert tp.html.find('<foo a="1"/>text', 'foo') == '<foo a="1"/>'
    assert tp.html.find('<foo a="1" />text', 'foo') == '<foo a="1" />'


def test_html_find_all_nested():
    """find_all returns nested matching tags too (document order), like
    BeautifulSoup().find_all()."""
    html = '<div><div>x</div></div>'
    assert tp.html.find_all(html, 'div') == [
        '<div><div>x</div></div>',
        '<div>x</div>',
    ]


def test_html_find_no_match():
    """find returns None and find_all returns [] when nothing matches,
    including empty input."""
    assert tp.html.find('<div>x</div>', 'span') is None
    assert tp.html.find_all('<div>x</div>', 'span') == []
    assert tp.html.find('', 'div') is None
    assert tp.html.find_all('', 'div') == []


def test_html_find_non_recursive_direct():
    """With recursive=False only top-level (depth 0) tags match."""
    assert tp.html.find('<div><span>a</span></div>', 'span', recursive=False) is None
    assert tp.html.find('<div><span>a</span></div>', 'div', recursive=False) == \
        '<div><span>a</span></div>'
    assert tp.html.find_all(
        '<div><span>a</span><div><span>b</span></div></div>',
        'span', recursive=False,
    ) == []
    assert tp.html.find_all('<div>a</div><span>b</span>', 'span', recursive=False) == \
        ['<span>b</span>']


# ---------------------------------------------------------------------------
# html.get_attr
# ---------------------------------------------------------------------------

TEST_TAGS = [
    (
        '<div class="test" id="block1">content1</div><div class="test2" id="block2" style="somestyle: 2px; border: green;">content2</div>',
        "div",
        "style",
    ),
    (
        '<div class="test2" id="block2" style="somestyle: 2px; border: green;">content2</div>',
        "div",
        "style",
    ),
    ('<a href="http://example.com" title="Link">Click</a>', "a", "href"),
    ('<input type="text" name="username" value="john"/>', "input", "name"),
    ('<span style="color: red">text</span>', "span", "style"),
]


@pytest.mark.parametrize(["html", "tag", "attr"], TEST_TAGS)
def test_get_attr_vs_bs4(html, tag, attr):
    """get_attr matches BeautifulSoup().find().get() on well-formed tags."""
    expected = py_get_attr_bs4(html, tag, attr)
    actual = tp.html.find(html, tag)
    if actual:
        actual = tp.html.get_attr(actual, attr)
    assert actual == expected


@pytest.mark.parametrize(["html", "tag", "attr"], TEST_TAGS)
def test_get_attr_vs_lxml(html, tag, attr):
    """get_attr matches lxml's find().get() on well-formed tags."""
    expected = py_get_attr_lxml(html, tag, attr)
    actual = tp.html.find(html, tag)
    if actual:
        actual = tp.html.get_attr(actual, attr)
    assert actual == expected


def test_get_attr_empty_attr_name():
    """An empty attribute name can never match (element.get('') is
    None). Cross-validated against bs4 (lxml's iter('') raises)."""
    assert tp.html.get_attr('<div class="x">t</div>', '') is None
    assert tp.html.get_attr('<a =x>', '') is None
    assert py_get_attr_bs4('<div>t</div>', 'div', '') is None


@pytest.mark.parametrize(["html", "tag", "attr"], [
    ('<div>t</div>', 'div', 'missing'),          # absent attribute -> None
    ('<div hidden>t</div>', 'div', 'hidden'),    # boolean attribute -> ''
    ('<div CLASS="x">t</div>', 'div', 'class'),  # case-insensitive name
    ('<a href=x.com>t</a>', 'a', 'href'),        # unquoted value
    ('<a title="a=b">t</a>', 'a', 'title'),      # '=' inside quoted value
    ('<div title="héllo">t</div>', 'div', 'title'),  # non-ASCII value
])
def test_get_attr_edge_cases(html, tag, attr):
    """Edge cases (absent/boolean attributes, case-insensitive names,
    unquoted and non-ASCII values) cross-validated against lxml's
    find().get().

    lxml is used as the reference because bs4 returns a list for the
    'class' attribute (AttributeValueList) while lxml and
    cythonpowered return a plain string.
    """
    expected = py_get_attr_lxml(html, tag, attr)
    actual = tp.html.find(html, tag)
    if actual:
        actual = tp.html.get_attr(actual, attr)
    assert actual == expected


# ---------------------------------------------------------------------------
# get_ips
# ---------------------------------------------------------------------------

TEST_IPS = [
    "192.168.1.1 and 10.0.0.1",
    "0.0.0.0 to 255.255.255.255",
    "textbeforeIP127.0.0.1",
    "127.0.0.2textafterIP",
    "256.1.1.1 invalid",
    "1.2.3.4.5 not an IP",
    "",
    "999.1.1.1",
    "1.2.3.456",
    "01.2.3.4",
    "1.2.3.4.5.6.7.8",
    "127.0.0.1:8080",
    "1.2.3.4,",
    "1.2.3",
]


@pytest.mark.parametrize("text", TEST_IPS)
def test_get_ips_vs_regex(text):
    """get_ips matches the regex reference (including the 0-255 octet
    validation) across valid, boundary, and invalid inputs."""
    expected = py_get_ips(text)
    actual = tp.get_ips(text)
    assert actual == expected


def test_extract_all_ips():
    """All valid IPs are extracted from the joined fixtures, invalid
    ones (256 octet, 5-part) are not."""
    all_ips = " ".join(TEST_IPS)
    actual = tp.get_ips(all_ips)
    assert "192.168.1.1" in actual
    assert "10.0.0.1" in actual
    assert "127.0.0.1" in actual
    assert "127.0.0.2" in actual
    assert "256.1.1.1" not in actual
    assert "1.2.3.4.5" not in actual


# ---------------------------------------------------------------------------
# get_emails
# ---------------------------------------------------------------------------

TEST_EMAILS = [
    "Contact us at user@example.com or admin@test.org",
    "test.name+tag@domain.co.uk",
    "john-doe.someguy@test.com",
    "invalid#mail@123.com",
    "al$oinvalidmail@foobar.io",
    "",
    "@b.com",
    "a@b.com-",
    "a@b.c1",
    "a@b.xc.d",
    "a@b.com-@c.com",
    "a@b..com",
    "a@@b.com",
    "user@localhost",
    "plain text without at sign",
    "a@b.c",
    "a@b.co",
]


@pytest.mark.parametrize("text", TEST_EMAILS)
def test_get_emails_vs_regex(text):
    """get_emails matches the regex reference exactly, including where
    the match ends (TLD is \\w{2,} after the rightmost qualifying dot,
    not 'all alpha to end of domain')."""
    expected = py_get_emails(text)
    actual = tp.get_emails(text)
    assert actual == expected


def test_extract_all_emails():
    """All valid emails are extracted from the joined fixtures; strings
    with invalid local parts are not matched in full."""
    all_emails = " ".join(TEST_EMAILS)
    actual = tp.get_emails(all_emails)
    assert "user@example.com" in actual
    assert "admin@test.org" in actual
    assert "test.name+tag@domain.co.uk" in actual
    assert "john-doe.someguy@test.com" in actual
    assert "invalid#mail@123.com" not in actual
    assert "al$oinvalidmail@foobar.io" not in actual


def test_get_emails_non_ascii_ascii_only():
    """Documented deviation: the function is ASCII only (the regex
    original's \\w also matches Unicode word chars), so a non-ASCII
    character terminates the local part."""
    assert tp.get_emails("usér@example.com") == ["r@example.com"]
    assert tp.get_emails("héllo@x.com") == ["llo@x.com"]


# ---------------------------------------------------------------------------
# get_mac_addrs
# ---------------------------------------------------------------------------

TEST_MAC_ADDRS = [
    "MAC: 00:1A:2B:3C:4D:5E and AA-BB-CC-DD-EE-FF",
    "00:1A:2B:3C:4D:5 and not-a-mac",
    "ZX-55-AB-78-A-FF-88 not a mac",
    "AB-F55-48-BD-78-AA also not a mac",
    "",
    "00:1A-2B:3C-4D:5E",
    "ABCD:11:22:33:44:55:66",
    "00:1A:2B:3C:4D:5",
    "aa:bb:cc:dd:ee:ff",
    "00:1A:2B:3C:4D:5E:FF",
]


@pytest.mark.parametrize("text", TEST_MAC_ADDRS)
def test_get_mac_addrs_vs_regex(text):
    """get_mac_addrs matches the regex reference exactly: separators may
    be mixed and there are no word boundaries (a match inside a longer
    hex run is still found, like the regex)."""
    expected = py_get_mac_addrs(text)
    actual = tp.get_mac_addrs(text)
    assert actual == expected


def test_extract_all_mac_addrs():
    """All valid MACs are extracted from the joined fixtures; incomplete
    or malformed ones are not."""
    all_mac_addrs = " ".join(TEST_MAC_ADDRS)
    actual = tp.get_mac_addrs(all_mac_addrs)
    assert "00:1A:2B:3C:4D:5E" in actual
    assert "AA-BB-CC-DD-EE-FF" in actual
    assert "00:1A:2B:3C:4D:5" not in actual
    assert "ZX-55-AB-78-A-FF-88" not in actual
    assert "AB-F55-48-BD-78-AA" not in actual
