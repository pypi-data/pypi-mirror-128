# Minifiers
from minify_html import minify as rust_minifier

from .html import (
    html_minify as python_minifier,
    mangle_nbsp,
    unmangle_nbsp,
)

# Guess the file content
from .functions import guess

# Import helper functions
from .html import add_line_break


def minify(
    buffer: bytes,
    # Rust
    STRIP_WHITESPACE_RUST_DO_NOT_MINIFY_DOCTYPE: bool,
    STRIP_WHITESPACE_RUST_ENSURE_SPEC_CONPLIANT_UNQUOTED_ATTRIBUTE_VALUES: bool,
    STRIP_WHITESPACE_RUST_KEEP_CLOSING_TAGS: bool,
    STRIP_WHITESPACE_RUST_KEEP_COMMENTS: bool,
    STRIP_WHITESPACE_RUST_KEEP_HTML_AND_HEAD_OPENING_TAGS: bool,
    STRIP_WHITESPACE_RUST_KEEP_SPACES_BETWEEN_ATTRIBUTES: bool,
    STRIP_WHITESPACE_RUST_MINIFY_CSS: bool,
    STRIP_WHITESPACE_RUST_MINIFY_JS: bool,
    STRIP_WHITESPACE_RUST_REMOVE_BANGS: bool,
    STRIP_WHITESPACE_RUST_REMOVE_PROCESSING_INSTRUCTIONS: bool,
    # Python
    STRIP_WHITESPACE_PYTHON_REMOVE_COMMENTS: bool,
    STRIP_WHITESPACE_PYTHON_CONDENSE_STYLE_FROM_HTML: bool,
    STRIP_WHITESPACE_PYTHON_CONDENSE_SCRIPT_FROM_HTML: bool,
    STRIP_WHITESPACE_PYTHON_CLEAN_UNNEEDED_HTML_TAGS: bool,
    STRIP_WHITESPACE_PYTHON_CONDENSE_HTML_WHITESPACE: bool,
    STRIP_WHITESPACE_PYTHON_UNQUOTE_HTML_ATTRIBUTES: bool,
    # NBSP char
    STRIP_WHITESPACE_NBSP_MANGLE_CHARACTER: str,
) -> str:
    buffer_type: str = guess(buffer).lower()
    decompressed_buffer: str = ""
    return_buffer: bytes = b""

    if buffer_type == "gz":
        from .functions.decompressors import gz_decompress

        decompressed_buffer = gz_decompress(buffer)

    elif buffer_type == "br":
        from .functions.decompressors import br_decompress

        decompressed_buffer = br_decompress(buffer)

    elif buffer_type == "zstd":
        from .functions.decompressors import zstd_decompress

        decompressed_buffer = zstd_decompress(buffer)

    elif buffer_type == "plain":
        decompressed_buffer = buffer

    #   First change the &nbsp; into a special character so the other compressors cant minify that.
    first_iter = mangle_nbsp(
        decompressed_buffer.decode(),
        STRIP_WHITESPACE_NBSP_MANGLE_CHARACTER,
    )

    #   Rust based minifier. The most powerful one in here. 💪
    second_iter = rust_minifier(
        first_iter,
        do_not_minify_doctype=STRIP_WHITESPACE_RUST_DO_NOT_MINIFY_DOCTYPE,
        ensure_spec_compliant_unquoted_attribute_values=STRIP_WHITESPACE_RUST_ENSURE_SPEC_CONPLIANT_UNQUOTED_ATTRIBUTE_VALUES,
        keep_closing_tags=STRIP_WHITESPACE_RUST_KEEP_CLOSING_TAGS,
        keep_comments=STRIP_WHITESPACE_RUST_KEEP_COMMENTS,
        keep_html_and_head_opening_tags=STRIP_WHITESPACE_RUST_KEEP_HTML_AND_HEAD_OPENING_TAGS,
        keep_spaces_between_attributes=STRIP_WHITESPACE_RUST_KEEP_SPACES_BETWEEN_ATTRIBUTES,
        minify_css=STRIP_WHITESPACE_RUST_MINIFY_CSS,
        minify_js=STRIP_WHITESPACE_RUST_MINIFY_JS,
        remove_bangs=STRIP_WHITESPACE_RUST_REMOVE_BANGS,
        remove_processing_instructions=STRIP_WHITESPACE_RUST_REMOVE_PROCESSING_INSTRUCTIONS,
    )

    #   Rust minifier comes first to migrate some of the issues I faced.😛
    #   Specially the python module picks '\n in class=""
    #   So first remove all unnecessary whitespace before adding line_break
    third_iter = add_line_break(second_iter)

    #   Finally the python iterator.
    #   I don't know how this works.🤷
    #   So adding it at last
    fourth_iter = python_minifier(
        third_iter,
        STRIP_WHITESPACE_PYTHON_REMOVE_COMMENTS,
        STRIP_WHITESPACE_PYTHON_CONDENSE_STYLE_FROM_HTML,
        STRIP_WHITESPACE_PYTHON_CONDENSE_SCRIPT_FROM_HTML,
        STRIP_WHITESPACE_PYTHON_CLEAN_UNNEEDED_HTML_TAGS,
        STRIP_WHITESPACE_PYTHON_CONDENSE_HTML_WHITESPACE,
        STRIP_WHITESPACE_PYTHON_UNQUOTE_HTML_ATTRIBUTES,
    )

    #   Replace special character with &nbsp;
    last_iter = unmangle_nbsp(
        fourth_iter,
        STRIP_WHITESPACE_NBSP_MANGLE_CHARACTER,
    )
    last_iter = last_iter.encode()

    # Decompress
    if buffer_type == "gz":
        from .functions.compressors import gz_compress

        return_buffer = gz_compress(last_iter)

    elif buffer_type == "br":
        from .functions.compressors import br_compress

        return_buffer = br_compress(last_iter)

    elif buffer_type == "zstd":
        from .functions.compressors import zstd_compress

        return_buffer = zstd_compress(last_iter)

    elif buffer_type == "plain":
        return_buffer = last_iter

    return return_buffer
