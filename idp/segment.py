# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from io import BytesIO

# This is the PyMuPDF import name
import fitz
from pathlib_mate import Path, T_PATH_ARG


@dataclasses.dataclass
class PdfSegments:
    pdf_pages: T.List[fitz.Document]
    pdf_paths: T.List[Path]
    png_pages: T.List[fitz.Pixmap]
    png_paths: T.List[Path]


def _segment_pdf(
    pdf_content: bytes,
    dir_tmp: Path,
    convert_to_png: bool = True,
    pix_map_dpi: int = 200,
) -> PdfSegments:
    """
    Split the PDF into individual pages
    """

    pdf = fitz.Document(stream=pdf_content)

    # --------------------------------------------------------------------------
    # Repair any issues (hopefully) before we hit them
    # See this https://github.com/pymupdf/PyMuPDF/issues/856
    # --------------------------------------------------------------------------
    buffer = BytesIO()
    # write the document to in-memory buffer
    buffer.write(pdf.write(clean=True, garbage=4))
    new_content = buffer.getvalue()
    buffer.close()

    pdf_cleaned = fitz.Document(stream=new_content)

    # --------------------------------------------------------------------------
    # Split PDF into pages
    # --------------------------------------------------------------------------

    # PyMuPDF doesn't support writing to buffer directly,
    # If you want to write it to S3, then you have to write it to local FS,
    # and then upload it to S3.
    pdf_pages: T.List[fitz.Document] = list()
    pdf_paths: T.List[Path] = list()
    png_pages: T.List[fitz.Pixmap] = list()
    png_paths: T.List[Path] = list()

    for page_num, page in enumerate(pdf_cleaned, start=1):
        # extract page as PDF
        pdf_page = fitz.Document()
        pdf_page.insert_pdf(
            pdf_cleaned,
            from_page=page_num - 1,
            to_page=page_num - 1,
        )
        path_page = dir_tmp / f"{page_num}.pdf"
        pdf_page.save(path_page.abspath)

        pdf_pages.append(pdf_page)
        pdf_paths.append(path_page)

        # extract page as image
        if convert_to_png:
            pix: fitz.Pixmap = page.get_pixmap(dpi=pix_map_dpi)
            path_img = dir_tmp / f"{page_num}.png"
            pix.save(path_img.abspath, output="png")
            png_pages.append(pix)
            png_paths.append(path_img)

    return PdfSegments(
        pdf_pages=pdf_pages,
        pdf_paths=pdf_paths,
        png_pages=png_pages,
        png_paths=png_paths,
    )


def segment_pdf(
    pdf_content: bytes,
    dir_tmp: T_PATH_ARG,
    convert_to_png: bool = True,
    pix_map_dpi: int = 200,
    cleanup_tmp_dir: bool = True,
) -> PdfSegments:
    dir_tmp = Path(dir_tmp)
    if dir_tmp.exists():
        raise FileExistsError(f"Directory {dir_tmp.abspath} already exists")
    dir_tmp.mkdir_if_not_exists()
    try:
        return _segment_pdf(
            pdf_content=pdf_content,
            dir_tmp=dir_tmp,
            convert_to_png=convert_to_png,
            pix_map_dpi=pix_map_dpi,
        )
    except Exception as e:
        if cleanup_tmp_dir:
            dir_tmp.remove_if_exists()
        raise e


def segment_email():
    raise NotImplementedError


def segment_word():
    raise NotImplementedError


def segment_excel():
    raise NotImplementedError


def segment_ppt():
    raise NotImplementedError
