# -*- coding: utf-8 -*-

import typing as T

import enum


class DocTypeEnum(str, enum.Enum):
    """
    Document type enum.
    """

    pdf = "pdf"
    jpg = "jpg"
    png = "png"
    bmp = "bmp"
    gif = "gif"
    tiff = "tiff"
    text = "text"
    word = "word"
    excel = "excel"
    ppt = "ppt"
    json = "json"
    csv = "csv"
    tsv = "tsv"
    unknown = "unknown"

    @classmethod
    def detect_doc_type(cls, filename: str) -> str:
        parts = filename.split(".")
        if len(parts) == 1:
            return cls.unknown.value
        else:
            return ext_to_doc_type_mapper.get(parts[-1].lower(), cls.unknown)


ext_to_doc_type_mapper: T.Dict[str, DocTypeEnum] = {
    "pdf": DocTypeEnum.pdf,
    "jpg": DocTypeEnum.jpg,
    "jpeg": DocTypeEnum.jpg,
    "png": DocTypeEnum.png,
    "bmp": DocTypeEnum.bmp,
    "gif": DocTypeEnum.gif,
    "tiff": DocTypeEnum.tiff,
    "txt": DocTypeEnum.text,
    "doc": DocTypeEnum.word,
    "docx": DocTypeEnum.word,
    "xls": DocTypeEnum.excel,
    "xlsx": DocTypeEnum.excel,
    "ppt": DocTypeEnum.ppt,
    "pptx": DocTypeEnum.ppt,
    "json": DocTypeEnum.json,
    "csv": DocTypeEnum.csv,
    "tsv": DocTypeEnum.tsv,
}


class ContentTypeEnum(str, enum.Enum):
    """
    S3 ContextType metadata enum.

    Ref:

    - https://www.ibm.com/docs/en/aspera-on-cloud?topic=SS5W4X/dita/content/aws_s3_content_types.htm
    """

    # pure text
    text_plain = "text/plain"

    # image
    image_png = "image/png"
    image_jpg = "image/jpeg"
    image_bmp = "image/bmp"
    image_tiff = "image/tiff"
    image_gif = "image/gif"

    # document
    ms_word = "application/msword"
    ms_ppt = "application/mspowerpoint"
    ms_excel = "application/x-msexcel"

    pdf = "	application/pdf"

    # archive
    zip = "application/zip"
    gzip = "application/x-gzip"
    tar = "application/x-tar"
    tgz = "application/x-compressed"

    # data format
    json = "application/json"
    csv = "text/csv"


doc_type_to_content_type_mapper: T.Dict[str, T.Optional[str]] = {
    DocTypeEnum.pdf.value: ContentTypeEnum.pdf.value,
    DocTypeEnum.jpg.value: ContentTypeEnum.image_jpg.value,
    DocTypeEnum.png.value: ContentTypeEnum.image_png.value,
    DocTypeEnum.bmp.value: ContentTypeEnum.image_bmp.value,
    DocTypeEnum.gif.value: ContentTypeEnum.image_gif.value,
    DocTypeEnum.tiff.value: ContentTypeEnum.image_tiff.value,
    DocTypeEnum.text.value: ContentTypeEnum.text_plain.value,
    DocTypeEnum.word.value: ContentTypeEnum.ms_word.value,
    DocTypeEnum.excel.value: ContentTypeEnum.ms_excel.value,
    DocTypeEnum.ppt.value: ContentTypeEnum.ms_ppt.value,
    DocTypeEnum.json.value: ContentTypeEnum.json.value,
    DocTypeEnum.csv.value: ContentTypeEnum.csv.value,
    DocTypeEnum.tsv.value: ContentTypeEnum.csv.value,
    DocTypeEnum.unknown.value: None,
}
