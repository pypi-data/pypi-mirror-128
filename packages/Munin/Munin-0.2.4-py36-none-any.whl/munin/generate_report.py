#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple

import numpy
from apppath import ensure_existence

from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelBinarizer

from draugr.visualisation import confusion_matrix_plot, roc_plot
from munin.utilities import MetricEntry, generate_metric_table, plt_html, plt_html_svg

ReportEntry = namedtuple("ReportEntry", ("name", "figure", "prediction", "truth", "outcome", "explanation"))

__author__ = "Christian Heider Nielsen"
__doc__ = """
Created on 27/04/2019

@author: cnheider
"""

from pathlib import Path


def generate_html(
    file_name,
    template_page: str = "classification_report_template.html",
    template_path: Path = None,
    **kwargs,
):
    """"""
    if not template_path:
        template_path = Path(__file__).parent / "templates"

    from jinja2 import Environment, select_autoescape, FileSystemLoader

    with open(f"{file_name}.html", "w", encoding="utf-8") as f:
        f.writelines(
            Environment(
                loader=FileSystemLoader(str(template_path)),
                autoescape=select_autoescape(["html", "xml"]),
            )
            .get_template(template_page)
            .render(**kwargs)
        )


def generate_pdf(file_name):
    """"""
    import pdfkit

    pdfkit.from_file(f"{file_name}.html", f"{file_name}.pdf")


if __name__ == "__main__":

    def a(
        title: str = "Classification Report",
        out_path=Path.cwd() / "exclude",
        num_classes=3,
    ):
        """"""
        from matplotlib import pyplot

        do_generate_pdf = False
        pyplot.rcParams["figure.figsize"] = (3, 3)
        from warg.data_structures.named_ordered_dictionary import NOD

        ensure_existence(out_path)

        file_name = out_path / title.lower().replace(" ", "_")

        cell_width = (800 / num_classes) - 6 - 6 * 2

        pyplot.plot(numpy.random.random((3, 3)))

        GPU_STATS = ReportEntry(
            name=1,
            figure=plt_html_svg(size=[cell_width, cell_width]),
            prediction="a",
            truth="b",
            outcome="fp",
            explanation=None,
        )

        pyplot.plot(numpy.ones((9, 3)))

        b = ReportEntry(
            name=2,
            figure=plt_html(format="svg", size=[cell_width, cell_width]),
            prediction="b",
            truth="c",
            outcome="fp",
            explanation=None,
        )

        pyplot.plot(numpy.ones((5, 6)))

        c = ReportEntry(
            name=3,
            figure=plt_html(size=[cell_width, cell_width]),
            prediction="a",
            truth="a",
            outcome="tp",
            explanation=None,
        )

        d = ReportEntry(
            name="fas3",
            figure=plt_html(format="jpg", size=[cell_width, cell_width]),
            prediction="a",
            truth="a",
            outcome="tp",
            explanation=None,
        )

        e = ReportEntry(
            name="fas3",
            figure=plt_html(format="jpeg", size=[cell_width, cell_width]),
            prediction="c",
            truth="c",
            outcome="tn",
            explanation=plt_html(format="svg", size=[cell_width, cell_width]),
        )

        from sklearn import svm, datasets
        from sklearn.model_selection import train_test_split

        iris = datasets.load_iris()
        X = iris.data
        y = iris.target
        class_names = iris.target_names

        bina = LabelBinarizer()
        y = bina.fit_transform(y)
        n_classes = y.shape[1]

        x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=2)

        classifier = OneVsRestClassifier(svm.SVC(kernel="linear", probability=True))
        classifier.fit(x_train, y_train)
        y_pred = classifier.predict(x_test)

        y_p_max = y_pred.argmax(axis=-1)
        y_t_max = y_test.argmax(axis=-1)

        confusion_matrix = plt_html(
            confusion_matrix_plot(y_t_max, y_p_max, category_names=class_names),
            format="png",
            size=[800, 800],
        )
        predictions = [
            [GPU_STATS, b, d],
            [GPU_STATS, c, d],
            [GPU_STATS, c, b],
            [c, b, e],
        ]

        metrics = generate_metric_table(y_t_max, y_p_max, class_names)
        metric_fields = ("Metric", *MetricEntry._fields)

        roc_figure = plt_html(roc_plot(y_pred, y_test, n_classes), format="png", size=[800, 800])

        bundle = NOD.nod_of(title, confusion_matrix, metric_fields, metrics, predictions, roc_figure)

        generate_html(file_name, **bundle)
        if do_generate_pdf:
            generate_pdf(file_name)

    a()
