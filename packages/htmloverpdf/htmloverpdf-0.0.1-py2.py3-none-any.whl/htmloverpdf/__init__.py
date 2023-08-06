"""Render a HTML overlay over existing PDF files."""

import io
from copy import deepcopy

import cairo
import cairocffi  # type: ignore
import gi  # type: ignore
import weasyprint  # type: ignore
from lxml import html

gi.require_version("Poppler", "0.18")
from gi.repository import Gio, GLib, Poppler  # type: ignore  # noqa: E402


def render(src: str) -> memoryview:
    """Convert HTML to a PDF."""

    output = io.BytesIO()
    surface = cairo.PDFSurface(output, 595, 842)
    ctx = cairo.Context(surface)
    cffictx = cairocffi.Context._from_pointer(
        cairocffi.ffi.cast("cairo_t **", id(ctx) + object.__basicsize__)[0], incref=True
    )

    doc = html.parse(io.StringIO(src), html.HTMLParser())

    for pdf in doc.xpath("//img[substring(@src, string-length(@src) - 3)='.pdf']"):
        for prev in pdf.xpath("preceding-sibling::*"):
            pdf.getparent().remove(prev)
        pdfsrc = pdf.get("src")
        pdf.getparent().remove(pdf)
        section = deepcopy(doc)
        for nextpdf in section.xpath(
            "//img[substring(@src, string-length(@src) - 3)='.pdf']"
        ):
            for nextel in nextpdf.xpath("following-sibling::*"):
                nextpdf.getparent().remove(nextel)

        html_pages = weasyprint.HTML(string=html.tostring(section)).render().pages
        surface.set_size(
            html_pages[0].width * 72 / 96.0, html_pages[0].height * 72 / 96.0
        )

        if pdfsrc != "blank.pdf":
            with weasyprint.default_url_fetcher(str(pdfsrc))["file_obj"] as fetch:
                pdf_pages = Poppler.Document.new_from_stream(
                    Gio.MemoryInputStream.new_from_bytes(
                        GLib.Bytes.new_take(fetch.read())
                    ),
                    -1,
                    None,
                    None,
                )
        else:
            pdf_pages = None
        for pageno in range(
            max(pdf_pages.get_n_pages() if pdf_pages else 0, len(html_pages))
        ):
            if pdf_pages and pageno < pdf_pages.get_n_pages():
                pdf_pages.get_page(pageno).render_for_printing(ctx)
            if pageno < len(html_pages):  # pragma: no branch
                html_pages[pageno].paint(cffictx, scale=72 / 96.0)
            ctx.show_page()
    surface.finish()
    return output.getbuffer()
