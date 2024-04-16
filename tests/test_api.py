# -*- coding: utf-8 -*-

from idp import api


def test():
    _ = api


if __name__ == "__main__":
    from idp.tests import run_cov_test

    run_cov_test(__file__, "idp.api", preview=False)
