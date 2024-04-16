# -*- coding: utf-8 -*-

from idp.segment import segment_pdf
from idp.paths import dir_unit_test

dir_source = dir_unit_test / "source"
dir_tmp = dir_unit_test / "tmp"


def _test_segment_pdf():
    dir_tmp.remove_if_exists()
    pdf_segments = segment_pdf(
        pdf_content=dir_source.joinpath("f1040.pdf").read_bytes(),
        dir_tmp=dir_tmp,
    )


def test():
    _test_segment_pdf()


if __name__ == "__main__":
    from idp.tests import run_cov_test

    run_cov_test(__file__, "idp.segment", preview=False)
