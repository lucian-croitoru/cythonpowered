# -----------------------------------------------------------------------------
# textparse — Fast text extraction functions powered by Cython
# Single-pass C scanning, no regex compilation, no backtracking
# -----------------------------------------------------------------------------

class html:
    """Fast raw-string HTML extraction (text, tags, attributes)."""

    @staticmethod
    def get_text(html: str, strip: bool = False):
        """Extract text from HTML, optionally stripping whitespace.

        Replacement for: BeautifulSoup(html).get_text()
        """
        return html_get_text(html, strip=strip)

    @staticmethod
    def find(html: str, tag: str, recursive: bool = True):
        """Find the first matching tag as a raw substring.

        Replacement for: BeautifulSoup(html).find()
        """
        return find_tag(html=html, tag=tag, find_all=False, recursive=recursive)

    @staticmethod
    def find_all(html: str, tag: str, recursive: bool = True):
        """Find all matching tags as a list of raw substrings.

        Replacement for: BeautifulSoup(html).find_all()
        """
        return find_tag(html=html, tag=tag, find_all=True, recursive=recursive)

    @staticmethod
    def get_attr(tag: str, attr: str):
        """Get an attribute value from a single tag string.

        Replacement for: BeautifulSoup().find().get()
        """
        return get_html_attr(tag=tag, attr=attr)


# -----------------------------------------------------------------------------
# ASCII character classification.
#
# Explicit range checks instead of ctype.h: ctype's isalpha()/isdigit()/
# isxdigit() are locale-dependent and only defined for values 0-255, while
# these helpers receive full code points (Py_UCS4). Range checks are
# locale-independent and deterministic. The ASCII-only behavior of the
# public functions is documented in their docstrings.
# -----------------------------------------------------------------------------

cdef inline bint _is_ascii_alpha(Py_UCS4 c):
    return (c >= 65 and c <= 90) or (c >= 97 and c <= 122)


cdef inline bint _is_ascii_digit(Py_UCS4 c):
    return c >= 48 and c <= 57


cdef inline bint _is_ascii_word(Py_UCS4 c):
    # ASCII \w: letters, digits, underscore
    return _is_ascii_alpha(c) or _is_ascii_digit(c) or c == 95


cdef inline bint _is_ascii_hex(Py_UCS4 c):
    return (
        _is_ascii_digit(c) or
        (c >= 65 and c <= 70) or
        (c >= 97 and c <= 102)
    )


cdef inline Py_UCS4 _ascii_lower(Py_UCS4 c):
    # ASCII-only lowercase; non-ASCII passes through unchanged.
    # The cast to unsigned int keeps this C arithmetic: Cython would
    # otherwise treat Py_UCS4 + int as a character operation (str).
    if 65 <= c <= 90:
        return <Py_UCS4>(<unsigned int>c + 32)
    return c
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
cdef inline str _tag_name_at(str html, Py_ssize_t tag_open, Py_ssize_t close_pos):
    """
    Lowercase tag name of the tag opened at tag_open (position of '<')
    and closed at close_pos (position of '>'); bounds are exclusive.
    A leading '/' (closing tag) is skipped.
    """
    cdef Py_ssize_t j = tag_open + 1
    cdef Py_ssize_t name_start
    cdef Py_UCS4 ch

    if j < close_pos and html[j] == '/':
        j += 1

    name_start = j

    while j < close_pos:
        ch = <Py_UCS4>ord(html[j])
        if ch <= 32 or ch == 62 or ch == 47:  # whitespace, '>', '/'
            break
        j += 1

    return html[name_start:j].lower()


cdef inline bint _is_self_closing_at(str html, Py_ssize_t tag_open, Py_ssize_t close_pos):
    """
    True if the tag opened at tag_open ('<') and closed at close_pos ('>')
    is explicitly self-closing, e.g. <foo /> or <foo/>.
    """
    cdef Py_ssize_t j = close_pos - 1
    cdef Py_UCS4 ch

    while j > tag_open:
        ch = <Py_UCS4>ord(html[j])
        if ch > 32:
            break
        j -= 1

    return j > tag_open and html[j] == '/'


cdef inline Py_ssize_t _find_closing_raw_tag(str html, Py_ssize_t i, Py_ssize_t n, str name):
    """
    html[i] is a '<' inside <script>/<style> content. If the tag at i is
    the closing tag for `name` (e.g. </script>), return the index just
    past its '>'; otherwise return -1.

    The name must be followed by whitespace, '>' or '/' so that
    </scriptfoo> does not close a <script> block.
    """
    cdef Py_ssize_t j = i + 1
    cdef Py_ssize_t name_start
    cdef Py_UCS4 ch

    if j >= n or html[j] != '/':
        return -1
    j += 1

    name_start = j
    while j < n:
        ch = <Py_UCS4>ord(html[j])
        if ch <= 32 or ch == 62 or ch == 47:  # whitespace, '>', '/'
            break
        j += 1

    # Length check first so the (rare) slice allocation only happens on a
    # candidate with the right name length.
    if j - name_start != len(name) or html[name_start:j].lower() != name:
        return -1

    while j < n and html[j] != '>':
        j += 1

    if j >= n:
        return -1

    return j + 1


cdef inline list _html_strip_tags(str html):
    """
    Removes all HTML tags from a string and returns a list of text parts,
    one per text node, in document order.

    Handles nested tags, quoted attributes, HTML comments, bare '<' in
    text, and <script>/<style> blocks (content dropped, like bs4/lxml).
    A tag starts only when '<' is followed by an ASCII letter, '/' or '?'
    (HTML5 data state), so 'a < b' stays plain text.
    """
    cdef Py_ssize_t i = 0
    cdef Py_ssize_t n = len(html)
    cdef Py_ssize_t text_start = 0
    cdef Py_ssize_t tag_open = 0
    cdef Py_ssize_t j
    cdef list parts = []
    cdef bint in_tag = False
    cdef bint in_comment = False
    cdef bint in_script = False
    cdef bint in_style = False
    cdef Py_UCS4 ch
    cdef Py_UCS4 quote = 0
    cdef str name

    while i < n:
        ch = <Py_UCS4>ord(html[i])

        # ---------------- comment ----------------
        if in_comment:
            if ch == 62 and i >= 2 and html[i - 2:i] == '--':  # '>'
                in_comment = False
                i += 1
                text_start = i
            else:
                i += 1
            continue

        # ---------------- script / style content ----------------
        if in_script or in_style:
            if ch == 60:  # '<'
                j = _find_closing_raw_tag(html, i, n, 'script' if in_script else 'style')
                if j >= 0:
                    in_script = False
                    in_style = False
                    i = j
                    text_start = i
                    continue
            i += 1
            continue

        # ---------------- inside a tag ----------------
        if in_tag:
            if quote != 0:
                if ch == quote:
                    quote = 0
            elif ch == 34 or ch == 39:  # '"' or "'"
                quote = ch
            elif ch == 62:  # '>'
                in_tag = False
                if html[tag_open + 1] != '/':
                    name = _tag_name_at(html, tag_open, i)
                    if name == 'script' and not _is_self_closing_at(html, tag_open, i):
                        in_script = True
                    elif name == 'style' and not _is_self_closing_at(html, tag_open, i):
                        in_style = True
                text_start = i + 1
            i += 1
            continue

        # ---------------- plain text ----------------
        if ch == 60:  # '<'
            if i + 1 < n:
                ch = <Py_UCS4>ord(html[i + 1])
                if ch == 33 and i + 3 < n and html[i + 2:i + 4] == '--':  # '!'
                    if text_start < i:
                        parts.append(html[text_start:i])
                    in_comment = True
                    i += 4
                    continue
                if _is_ascii_alpha(ch) or ch == 47 or ch == 63:  # '/', '?'
                    if text_start < i:
                        parts.append(html[text_start:i])
                    in_tag = True
                    tag_open = i
                    i += 1
                    continue
            # Bare '<' in text (e.g. "a < b"): not a tag
            i += 1
            continue

        i += 1

    # Only append the trailing text if we are not inside a construct
    # that swallows it (unclosed tag, comment, script or style block).
    if (
        not in_tag and
        not in_comment and
        not in_script and
        not in_style and
        text_start < n
    ):
        parts.append(html[text_start:])

    return parts
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
cpdef inline str html_get_text(str html, bint strip=False):
    """
    Extract text from HTML, optionally stripping whitespace per text node.
    <script>/<style> content and comments are dropped, like
    BeautifulSoup(...).get_text(). No HTML entity decoding.
    Replacement for: BeautifulSoup(html).get_text()
    """
    cdef list text = _html_strip_tags(html)
    cdef str part
    if strip:
        return ''.join([part.strip() for part in text])

    return ''.join(text)
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
from cpython.unicode cimport (
    PyUnicode_KIND,
    PyUnicode_DATA,
    PyUnicode_READ
)

cpdef inline str get_html_attr(str tag, str attr):
    """
    Get the value of an attribute from a single tag string, e.g.
    get_html_attr('<a href="x">t</a>', 'href') -> 'x'.

    Attribute names are compared case-insensitively (HTML attribute names
    are ASCII case-insensitive, like BeautifulSoup/lxml). A present but
    valueless (boolean) attribute returns '' (both BeautifulSoup with the
    lxml parser and lxml return '' for it). Returns None when the
    attribute is absent, like element.get().
    Replacement for: BeautifulSoup().find().get()
    """
    cdef:
        Py_ssize_t n = len(tag)
        Py_ssize_t m = len(attr)
        Py_ssize_t i = 0          # Current scan position
        Py_ssize_t j              # Loop variable
        Py_ssize_t start          # Start of current token

        # Cache Unicode internals once.
        # This avoids repeated Python-level indexing.
        int kind_tag = PyUnicode_KIND(tag)
        int kind_attr = PyUnicode_KIND(attr)

        void* data_tag = PyUnicode_DATA(tag)
        void* data_attr = PyUnicode_DATA(attr)

        Py_UCS4 c
        Py_UCS4 quote

        bint matched

    # An empty attribute name can never match (element.get("") is None).
    if m == 0:
        return None

    # ----------------------------------------------------------
    # Skip the opening tag name.
    #
    # Example:
    #     <a href="x">
    #      ^
    #      i starts here
    #
    # We stop once we reach the whitespace after "a".
    # ----------------------------------------------------------
    while i < n:
        c = PyUnicode_READ(kind_tag, data_tag, i)
        if c <= 32:
            break
        i += 1

    # ----------------------------------------------------------
    # Scan each attribute exactly once.
    # ----------------------------------------------------------
    while i < n:

        # Skip whitespace between attributes.
        while i < n:
            c = PyUnicode_READ(kind_tag, data_tag, i)
            if c > 32:
                break
            i += 1

        if i >= n:
            break

        # Stop at end of tag.
        if PyUnicode_READ(kind_tag, data_tag, i) == 62:
            break

        # Beginning of current attribute name.
        start = i

        # Read until '=', whitespace or '>'.
        while i < n:
            c = PyUnicode_READ(kind_tag, data_tag, i)
            if c == 61 or c <= 32 or c == 62:
                break
            i += 1

        # ------------------------------------------------------
        # Compare attribute name (case-insensitive).
        #
        # This performs an in-place character comparison.
        # No temporary substring is ever created.
        # ------------------------------------------------------
        if i - start == m:

            matched = True
            for j in range(m):
                if (
                    _ascii_lower(PyUnicode_READ(kind_tag, data_tag, start + j))
                    !=
                    _ascii_lower(PyUnicode_READ(kind_attr, data_attr, j))
                ):
                    matched = False
                    break

            if matched:
                # ==================================================
                # Attribute name matched.
                # Parse and return its value.
                # ==================================================

                # Skip spaces before '='
                while i < n and PyUnicode_READ(kind_tag, data_tag, i) <= 32:
                    i += 1

                # Present but valueless (boolean) attribute.
                if i >= n or PyUnicode_READ(kind_tag, data_tag, i) != 61:
                    return ""

                i += 1

                # Skip spaces after '='
                while i < n and PyUnicode_READ(kind_tag, data_tag, i) <= 32:
                    i += 1

                if i >= n:
                    return ""

                quote = PyUnicode_READ(kind_tag, data_tag, i)

                # -----------------------------
                # Quoted attribute
                # href="..."
                # -----------------------------
                if quote == '"' or quote == "'":
                    i += 1
                    start = i

                    while i < n and PyUnicode_READ(kind_tag, data_tag, i) != quote:
                        i += 1

                    # This is the ONLY string allocation.
                    return tag[start:i]

                # -----------------------------
                # Unquoted attribute
                # value=123
                # -----------------------------
                start = i

                while i < n:
                    c = PyUnicode_READ(kind_tag, data_tag, i)
                    if c <= 32 or c == 62:
                        break
                    i += 1

                return tag[start:i]

        # ------------------------------------------------------
        # Attribute name didn't match.
        #
        # Skip over the entire attribute value so that scanning
        # resumes at the next attribute.
        # ------------------------------------------------------
        while i < n:

            c = PyUnicode_READ(kind_tag, data_tag, i)

            if c == 62:
                return None

            if c == 61:

                i += 1

                while i < n and PyUnicode_READ(kind_tag, data_tag, i) <= 32:
                    i += 1

                if i >= n:
                    return None

                quote = PyUnicode_READ(kind_tag, data_tag, i)

                # Skip quoted value.
                if quote == '"' or quote == "'":

                    i += 1

                    while i < n and PyUnicode_READ(kind_tag, data_tag, i) != quote:
                        i += 1

                    if i < n:
                        i += 1

                # Skip unquoted value.
                else:

                    while i < n:
                        c = PyUnicode_READ(kind_tag, data_tag, i)
                        if c <= 32 or c == 62:
                            break
                        i += 1

                break

            i += 1

    # Attribute not found.
    return None
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# Fast HTML tag search
# -----------------------------------------------------------------------------

from cpython.unicode cimport PyUnicode_AsUTF8AndSize, PyUnicode_DecodeUTF8


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

cdef inline bint is_space(char c):
    return (
        c == ' ' or
        c == '\t' or
        c == '\n' or
        c == '\r'
    )


cdef inline str _utf8_substr(const char* buf, Py_ssize_t start, Py_ssize_t end):
    """
    Decode buf[start:end] as a str.

    Extraction ranges always begin at '<' and end just past '>' (both
    single-byte UTF-8 characters), so the range is always on character
    boundaries and decodes cleanly. This keeps the scan at byte level
    (fast, memcmp-friendly) while returning correct results for
    non-ASCII HTML, where byte offsets differ from code point offsets.
    """
    return PyUnicode_DecodeUTF8(<char*>buf + start, end - start, "strict")


cdef inline bint _ascii_mem_eq(const char* a, const char* b, Py_ssize_t n):
    """Case-insensitive ASCII comparison of n bytes."""
    cdef Py_ssize_t i
    for i in range(n):
        if _ascii_lower(<unsigned char>a[i]) != _ascii_lower(<unsigned char>b[i]):
            return False
    return True


cdef inline bint tag_equals(
    const char* html,
    Py_ssize_t start,
    Py_ssize_t end,
    const char* target,
    Py_ssize_t target_len
):
    # Case-insensitive ASCII comparison (HTML tag names are
    # case-insensitive; target is already lowercase ASCII).
    cdef Py_ssize_t i

    if end - start != target_len:
        return False

    for i in range(target_len):
        if _ascii_lower(<unsigned char>html[start + i]) != <Py_UCS4>target[i]:
            return False

    return True


cdef inline bint is_void_tag(
    const char* tag_ptr,
    Py_ssize_t tag_len
):
    """
    HTML5 void elements (case-insensitive).

    These elements do not have closing tags:

        <area>
        <base>
        <br>
        <col>
        <embed>
        <hr>
        <img>
        <input>
        <link>
        <meta>
        <param>
        <source>
        <track>
        <wbr>
    """

    if tag_len == 2:
        return (
            _ascii_mem_eq(tag_ptr, b"br", 2) or
            _ascii_mem_eq(tag_ptr, b"hr", 2)
        )

    if tag_len == 3:
        return (
            _ascii_mem_eq(tag_ptr, b"img", 3) or
            _ascii_mem_eq(tag_ptr, b"col", 3) or
            _ascii_mem_eq(tag_ptr, b"wbr", 3)
        )

    if tag_len == 4:
        return (
            _ascii_mem_eq(tag_ptr, b"area", 4) or
            _ascii_mem_eq(tag_ptr, b"base", 4) or
            _ascii_mem_eq(tag_ptr, b"link", 4) or
            _ascii_mem_eq(tag_ptr, b"meta", 4)
        )

    if tag_len == 5:
        return (
            _ascii_mem_eq(tag_ptr, b"input", 5) or
            _ascii_mem_eq(tag_ptr, b"embed", 5) or
            _ascii_mem_eq(tag_ptr, b"param", 5) or
            _ascii_mem_eq(tag_ptr, b"track", 5)
        )

    if tag_len == 6:
        return (
            _ascii_mem_eq(tag_ptr, b"source", 6)
        )

    return False


# -----------------------------------------------------------------------------
# Find the end of an opening tag.
#
# This correctly handles:
#
#     <input type="text">
#     <input title="1 > 0">
#
# so that '>' inside quotes isn't treated as the end of the tag.
# -----------------------------------------------------------------------------

cdef inline Py_ssize_t find_tag_end(
    const char* buf,
    Py_ssize_t start,
    Py_ssize_t n
):
    cdef:
        Py_ssize_t i = start
        char quote = 0

    while i < n:

        if quote != 0:
            if buf[i] == quote:
                quote = 0

        else:
            if buf[i] == '"' or buf[i] == "'":
                quote = buf[i]

            elif buf[i] == '>':
                return i

        i += 1

    return n


# -----------------------------------------------------------------------------
# Determine whether an opening tag is explicitly self-closing:
#
#     <foo />
#     <foo/>
# -----------------------------------------------------------------------------

cdef inline bint is_self_closing(
    const char* buf,
    Py_ssize_t start,
    Py_ssize_t end
):
    cdef Py_ssize_t i = end

    while i > start and is_space(buf[i - 1]):
        i -= 1

    return (
        i > start and
        buf[i - 1] == '/'
    )


# -----------------------------------------------------------------------------
# Find the next tag name.
#
# Returns:
#
#     0  = not a normal opening/closing tag
#     1  = opening tag
#     2  = closing tag
#
# name_start/name_end contain the tag name.
# tag_end contains the position of '>'.
# -----------------------------------------------------------------------------

cdef inline int parse_tag(
    const char* buf,
    Py_ssize_t start,
    Py_ssize_t n,
    Py_ssize_t* name_start,
    Py_ssize_t* name_end,
    Py_ssize_t* tag_end
):
    cdef:
        Py_ssize_t i = start + 1
        Py_ssize_t ns
        Py_ssize_t ne
        bint closing = False

    if i >= n:
        return 0

    # Closing tag
    if buf[i] == '/':
        closing = True
        i += 1

    # Comments, declarations, processing instructions, etc.
    if i >= n:
        return 0

    if (
        buf[i] == '!' or
        buf[i] == '?'
    ):
        return 0

    # The tag name must start immediately after '<' or '</' (HTML5 data
    # state); '<' followed by anything else is plain text, so "a < b"
    # must not be treated as a tag.
    ns = i

    # Tag name
    while (
        i < n and
        not is_space(buf[i]) and
        buf[i] != '>' and
        buf[i] != '/'
    ):
        i += 1

    ne = i

    if ne == ns:
        return 0

    # Find the end of the complete tag.
    i = find_tag_end(buf, i, n)

    if i >= n:
        return 0

    name_start[0] = ns
    name_end[0] = ne
    tag_end[0] = i

    if closing:
        return 2

    return 1


# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------

cpdef inline find_tag(
    str html,
    str tag,
    bint find_all=False,
    bint recursive=True
):
    """
    Fast HTML tag search.

    Tag names are matched case-insensitively (like BeautifulSoup). A
    non-ASCII tag can never match (HTML tag names are ASCII) and yields
    no match instead of raising, like BeautifulSoup.

    Examples:

        find_tag(html, "div")

            -> "<div>...</div>"

        find_tag(html, "input")

            -> '<input type="text">'

        find_tag(html, "input", find_all=True)

            -> [
                    '<input type="text">',
                    '<input type="email">'
                ]

    Args:
        html:
            HTML string to search.

        tag:
            Tag name, e.g. "div", "input", "img".

        find_all:
            Return all matching tags instead of the first one.

        recursive:
            If True, matching tags may occur inside other elements.

            If False, only top-level matching tags are returned.

    Returns:
        str
            First matching tag.

        list[str]
            All matching tags when find_all=True.

        None
            If no matching tag exists.

    Replacement for: BeautifulSoup().find() / BeautifulSoup().find_all()
    """

    cdef:
        Py_ssize_t n
        const char* buf

        const char* tag_ptr
        Py_ssize_t tag_len

        Py_ssize_t i = 0
        Py_ssize_t j

        Py_ssize_t open_start = 0
        Py_ssize_t open_end = 0

        Py_ssize_t name_start = 0
        Py_ssize_t name_end = 0

        Py_ssize_t close_name_start = 0
        Py_ssize_t close_name_end = 0
        Py_ssize_t close_end = 0

        Py_ssize_t depth = 0
        Py_ssize_t local_depth

        int tag_type
        int inner_type

        bint self_closing

        list results = []

        bytes lower_tag

    # HTML tag names are ASCII; a non-ASCII search tag can never match,
    # so return no match instead of raising (like BeautifulSoup).
    if not tag.isascii():
        return [] if find_all else None

    # -------------------------------------------------------------------------
    # Convert strings to UTF-8.
    # -------------------------------------------------------------------------

    buf = PyUnicode_AsUTF8AndSize(html, &n)

    # Make tag comparison case-insensitive.
    #
    # HTML tag names are ASCII case-insensitive.
    lower_tag = tag.lower().encode("ascii")
    tag_ptr = lower_tag
    tag_len = len(lower_tag)

    # -------------------------------------------------------------------------
    # Main scan
    # -------------------------------------------------------------------------

    while i < n:

        # Find next '<'
        if buf[i] != '<':
            i += 1
            continue

        open_start = i

        # ---------------------------------------------------------------------
        # Parse this tag.
        # ---------------------------------------------------------------------

        tag_type = parse_tag(
            buf,
            i,
            n,
            &name_start,
            &name_end,
            &open_end
        )

        # Not a normal tag.
        if tag_type == 0:
            i += 1
            continue

        # ---------------------------------------------------------------------
        # Closing tags don't start a search.
        #
        # We don't use them to blindly manipulate global depth because
        # unrelated closing tags should not affect whether our requested
        # tag is nested.
        # ---------------------------------------------------------------------

        if tag_type == 2:
            i = open_end + 1

            if depth > 0:
                depth -= 1

            continue

        # ---------------------------------------------------------------------
        # Opening tag.
        # ---------------------------------------------------------------------

        # Is this the tag we're looking for?
        if tag_equals(
            buf,
            name_start,
            name_end,
            tag_ptr,
            tag_len
        ):

            # -------------------------------------------------------------
            # Void HTML element.
            #
            # Examples:
            #
            #   <input>
            #   <input type="text">
            #   <img src="foo.jpg">
            #   <br>
            #
            # There is no closing tag to search for.
            # -------------------------------------------------------------

            if is_void_tag(
                tag_ptr,
                tag_len
            ):

                if recursive or depth == 0:

                    if not find_all:
                        return _utf8_substr(buf, open_start, open_end + 1)

                    results.append(
                        _utf8_substr(buf, open_start, open_end + 1)
                    )

                i = open_end + 1
                continue

            # -------------------------------------------------------------
            # Explicit self-closing element.
            #
            # Examples:
            #
            #   <foo />
            #   <custom/>
            #
            # -------------------------------------------------------------

            self_closing = is_self_closing(
                buf,
                open_start,
                open_end
            )

            if self_closing:

                if recursive or depth == 0:

                    if not find_all:
                        return _utf8_substr(buf, open_start, open_end + 1)

                    results.append(
                        _utf8_substr(buf, open_start, open_end + 1)
                    )

                i = open_end + 1
                continue

            # -------------------------------------------------------------
            # Normal opening/closing element.
            #
            # Search for the corresponding closing tag.
            # -------------------------------------------------------------

            if recursive or depth == 0:

                local_depth = 1
                j = open_end + 1

                while j < n:

                    # Find next '<'
                    while j < n and buf[j] != '<':
                        j += 1

                    if j >= n:
                        break

                    # -----------------------------------------------------
                    # Parse next tag.
                    # -----------------------------------------------------

                    inner_type = parse_tag(
                        buf,
                        j,
                        n,
                        &close_name_start,
                        &close_name_end,
                        &close_end
                    )

                    if inner_type == 0:
                        j += 1
                        continue

                    # -----------------------------------------------------
                    # Another opening tag with the same name.
                    # -----------------------------------------------------

                    if inner_type == 1:

                        # Ignore void elements.
                        if tag_equals(
                            buf,
                            close_name_start,
                            close_name_end,
                            tag_ptr,
                            tag_len
                        ):

                            if not is_void_tag(
                                buf + close_name_start,
                                close_name_end - close_name_start
                            ) and not is_self_closing(
                                buf,
                                j,
                                close_end
                            ):
                                local_depth += 1

                        j = close_end + 1
                        continue

                    # -----------------------------------------------------
                    # Closing tag.
                    # -----------------------------------------------------

                    if inner_type == 2:

                        if tag_equals(
                            buf,
                            close_name_start,
                            close_name_end,
                            tag_ptr,
                            tag_len
                        ):

                            local_depth -= 1

                            if local_depth == 0:

                                if not find_all:
                                    return _utf8_substr(buf, open_start, close_end + 1)

                                results.append(
                                    _utf8_substr(buf, open_start, close_end + 1)
                                )

                                break

                        j = close_end + 1
                        continue

                    j = close_end + 1

        # ---------------------------------------------------------------------
        # Move to the next opening tag.
        # ---------------------------------------------------------------------

        # Void/self-closing tags don't increase depth.
        if not is_void_tag(
            buf + name_start,
            name_end - name_start
        ) and not is_self_closing(
            buf,
            open_start,
            open_end
        ):
            depth += 1

        i = open_end + 1

    # -------------------------------------------------------------------------
    # Results
    # -------------------------------------------------------------------------

    if find_all:
        return results

    return None

# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
cdef inline bint _is_local_char(Py_UCS4 c):
    """Returns True if the code point is valid in an email local part."""
    return _is_ascii_word(c) or c == 46 or c == 43 or c == 45  # '.', '+', '-'


cdef inline bint _is_domain_char(Py_UCS4 c):
    """Returns True if the code point is valid in an email domain part."""
    return _is_ascii_word(c) or c == 46 or c == 45  # '.', '-'
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
cpdef inline list get_ips(str text):
    """
    Extracts valid IPv4 addresses from text.
    Validates each octet is 0-255. Respects word boundaries.
    ASCII only (the regex original's \\d also matches Unicode digits).
    Replacement for: re.findall(r"(?<![.\\d])(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})(?![.\\d])", text)
    """
    cdef Py_ssize_t i = 0
    cdef Py_ssize_t n = len(text)
    cdef list result = []
    cdef Py_ssize_t j
    cdef Py_ssize_t octet_start
    cdef unsigned short octet_val
    cdef Py_ssize_t octets_found = 0

    while i < n:
        if not _is_ascii_digit(<Py_UCS4>ord(text[i])):
            i += 1
            continue

        # Word boundary: no digit before
        if i > 0 and _is_ascii_digit(<Py_UCS4>ord(text[i - 1])):
            i += 1
            continue

        j = i
        octets_found = 0

        while j < n and octets_found < 4:
            octet_start = j
            octet_val = 0
            # Limit to 3 digits per octet (valid IPv4 octets: 0-255, max 3 digits)
            while j < n and (j - octet_start) < 3 and _is_ascii_digit(<Py_UCS4>ord(text[j])):
                octet_val = octet_val * 10 + (<unsigned short>(<int>ord(text[j]) - 48))
                j += 1

            if j == octet_start:
                break

            if octet_val > 255:
                break

            octets_found += 1

            if octets_found < 4:
                if j >= n or text[j] != '.':
                    break
                j += 1

        if octets_found == 4:
            # Word boundary: no digit or dot adjacent
            if i > 0 and (text[i - 1] == '.' or _is_ascii_digit(<Py_UCS4>ord(text[i - 1]))):
                i += 1
                continue
            if j < n and (text[j] == '.' or _is_ascii_digit(<Py_UCS4>ord(text[j]))):
                i += 1
                continue

            result.append(text[i:j])
            i = j
        else:
            i += 1

    return result
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
cpdef inline list get_emails(str text):
    """
    Extracts email addresses from text.
    Local part: ASCII word chars + "._+-".
    Domain: ASCII word chars + ".-", containing a dot, whose TLD is 2+
    word chars after the rightmost qualifying dot — matching the regex
    original exactly, including where the match ends (e.g. "a@b.com-"
    yields "a@b.com", "a@b.xc.d" yields "a@b.xc").
    ASCII only (the regex original's \\w also matches Unicode word chars).
    Replacement for: re.findall(r"[\\w.+-]+@[\\w.-]+\\.\\w{2,}", text)
    """
    cdef Py_ssize_t i = 0
    cdef Py_ssize_t n = len(text)
    cdef list result = []
    cdef Py_ssize_t scan_pos
    cdef Py_ssize_t at_pos
    cdef Py_ssize_t local_end
    cdef Py_ssize_t local_start
    cdef Py_ssize_t domain_end
    cdef Py_ssize_t k
    cdef Py_ssize_t w
    cdef Py_ssize_t match_end

    while i < n:
        # Find @ symbol
        scan_pos = i
        while i < n and text[i] != '@':
            i += 1
        if i >= n:
            break

        at_pos = i
        i += 1

        # Local part: maximal run of local chars ending just before '@'.
        # The run cannot extend before scan_pos: re.findall resumes
        # scanning right after the previous match end, so a candidate
        # match must start there or later.
        local_end = at_pos - 1
        while local_end >= scan_pos and _is_local_char(<Py_UCS4>ord(text[local_end])):
            local_end -= 1
        local_start = local_end + 1

        # The regex requires at least one local char before '@'
        if local_start >= at_pos:
            continue

        # Domain: maximal run of domain chars after '@'
        domain_end = i
        while domain_end < n and _is_domain_char(<Py_UCS4>ord(text[domain_end])):
            domain_end += 1

        # Find the rightmost dot in the domain that is followed by a run
        # of 2+ word chars (the regex's \.\w{2,}, matched greedily from
        # the left, so the rightmost qualifying dot wins). The match ends
        # at the end of that word run, not necessarily at the end of the
        # domain.
        match_end = -1
        k = domain_end - 1
        while k > i and match_end < 0:
            if text[k] == '.':
                w = k + 1
                while w < n and _is_ascii_word(<Py_UCS4>ord(text[w])):
                    w += 1
                if w - (k + 1) >= 2:
                    match_end = w
            k -= 1

        if match_end < 0:
            # No valid domain: every start position in the local run
            # (and '@' itself) fails, so the regex resumes at at_pos + 1.
            # (The inner '@' scan skips the domain run anyway, as it
            # cannot contain '@'.)
            i = at_pos + 1
            continue

        result.append(text[local_start:match_end])
        i = match_end

    return result
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
cpdef inline list get_mac_addrs(str text):
    """
    Extracts MAC addresses (XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX).
    Separators may be mixed and there are no word boundaries, matching
    the regex original exactly (e.g. 'ABCD:11:22:33:44:55:66' yields
    'CD:11:22:33:44:55').
    Replacement for: re.findall(r"[0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}", text)
    """
    cdef Py_ssize_t i = 0
    cdef Py_ssize_t n = len(text)
    cdef list result = []
    cdef Py_ssize_t p
    cdef Py_ssize_t pair
    cdef bint ok

    # A match is always exactly 17 characters: 6 hex pairs + 5 separators
    while i + 17 <= n:
        ok = (
            _is_ascii_hex(<Py_UCS4>ord(text[i])) and
            _is_ascii_hex(<Py_UCS4>ord(text[i + 1])) and
            (text[i + 2] == ':' or text[i + 2] == '-')
        )

        if ok:
            p = i + 3
            for pair in range(5):
                if not (
                    _is_ascii_hex(<Py_UCS4>ord(text[p])) and
                    _is_ascii_hex(<Py_UCS4>ord(text[p + 1]))
                ):
                    ok = False
                    break
                p += 2

                if pair < 4:
                    if text[p] != ':' and text[p] != '-':
                        ok = False
                        break
                    p += 1

        if ok:
            result.append(text[i:i + 17])
            # re.findall resumes right after the end of the match
            i += 17
        else:
            i += 1

    return result
# -----------------------------------------------------------------------------
