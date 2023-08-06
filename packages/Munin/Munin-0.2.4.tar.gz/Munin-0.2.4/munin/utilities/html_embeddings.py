#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Christian Heider Nielsen"
__doc__ = """
Created on 27/04/2019

@author: cnheider
"""

from collections import namedtuple
from io import BytesIO, StringIO
from typing import Any, Sequence, Tuple

from matplotlib import pyplot
from matplotlib.figure import Figure
from warg.data_structures.named_ordered_dictionary import NOD

MetricEntry = namedtuple("MetricEntry", ("Description", "Math", "Values", "Aggregated"))


def generate_metric_table(
    truths: Sequence, predictions: Sequence, categories: Sequence, decimals: int = 1
) -> Sequence[MetricEntry]:
    """

    :param truths:
    :param predictions:
    :param categories:
    :param decimals:
    :return:
    """
    import numpy
    from pycm import ConfusionMatrix

    cm = ConfusionMatrix(actual_vector=truths, predict_vector=predictions)
    cm.relabel({k: v for k, v in zip(range(len(categories)), categories)})

    support = MetricEntry(
        "Occurrence of each class (P)",
        generate_math_html("TP+FN"),
        {k: numpy.round(v, decimals) for k, v in cm.P.items()},
        numpy.round(sum(cm.P.values()) / len(categories), decimals),
    )

    sensitivity = MetricEntry(
        "True Positive Rate (TPR)",
        generate_math_html("\dfrac{TP}{TP+FN}"),
        {k: numpy.round(v, decimals) for k, v in cm.TPR.items()},
        numpy.round(sum(cm.TPR.values()) / len(categories), decimals),
    )

    specificity = MetricEntry(
        "True Negative Rate (TNR)",
        generate_math_html("\dfrac{TN}{TN+FP}"),
        {k: numpy.round(v, decimals) for k, v in cm.TNR.items()},
        numpy.round(sum(cm.TNR.values()) / len(categories), decimals),
    )

    precision = MetricEntry(
        "Positive Predictive Rate (PPV)",
        generate_math_html("\dfrac{TP}{TP+FP}"),
        {k: numpy.round(v, decimals) for k, v in cm.PPV.items()},
        numpy.round(sum(cm.PPV.values()) / len(categories), decimals),
    )

    npv = MetricEntry(
        "Negative Predictive Value (NPV)",
        generate_math_html("\dfrac{TP}{TP+FP}"),
        {k: numpy.round(v, decimals) for k, v in cm.NPV.items()},
        numpy.round(sum(cm.NPV.values()) / len(categories), decimals),
    )

    accuracy = MetricEntry(
        "Trueness",
        generate_math_html("\dfrac{TP+TN}{TP+TN+FP+FN}"),
        {k: numpy.round(v, decimals) for k, v in cm.ACC.items()},
        numpy.round(sum(cm.ACC.values()) / len(categories), decimals),
    )

    f1_score = MetricEntry(
        "Harmonic mean of precision and sensitivity",
        generate_math_html("2*\dfrac{PPV*TPR}{PPV+TPR}"),
        {k: numpy.round(v, decimals) for k, v in cm.F1.items()},
        numpy.round(sum(cm.F1.values()) / len(categories), decimals),
    )

    mcc = MetricEntry(
        "Matthews correlation coefficient",
        generate_math_html("\dfrac{TP*TN-FP*FN}{\sqrt{(TP+FP)(TP+FN)(TN+FP)(TN+FN)}}"),
        {k: numpy.round(v, decimals) for k, v in cm.MCC.items()},
        numpy.round(sum(cm.MCC.values()) / len(categories), decimals),
    )

    roc_auc = MetricEntry(
        "Receiver Operating Characteristics (ROC), "
        "Sensitivity vs (1 − Specificity), "
        "(True Positive Rate vs False Positive Rate), "
        "Area Under the Curve (AUC)",
        generate_math_html("\dfrac{TNR+TPR}{2}"),
        {k: numpy.round(v, decimals) for k, v in cm.AUC.items()},
        numpy.round(sum(cm.AUC.values()) / len(categories), decimals),
    )

    return NOD.nod_of(
        support, sensitivity, specificity, precision, npv, accuracy, f1_score, mcc, roc_auc,
    ).as_flat_tuples()


def generate_math_html(equation: str = "e^x", inline: bool = True, html_classes: str = "math_span") -> str:
    """
    For inline math, use \(...\).
    For standalone math, use $$...$$, \[...\] or \begin...\end.
    md = markdown.Markdown(extensions=['mdx_math'])
    md.convert('$$e^x$$')

    :param html_classes:
    :param equation:
    :param inline:
    :return:"""
    import markdown

    md = markdown.Markdown(extensions=["mdx_math"], extension_configs={"mdx_math": {"add_preview": True}})
    if inline:
        stripped = md.convert(f"\({equation}\)").lstrip("<p>").rstrip("</p>")
        return f'<span class="{html_classes}"><{stripped}></span>'
    return md.convert(f"$${equation}$$")


def generate_qr(data: Any) -> str:
    """

    :return:
    """
    import pyqrcode
    import io
    import base64

    code = pyqrcode.create(data)
    stream = io.BytesIO()
    code.png(stream, scale=6)
    return base64.b64encode(stream.getvalue()).decode("ascii")


def plt_html_svg(fig: Figure = None, *, size: Tuple[int, int] = (400, 400), dpi: int = 100) -> str:
    """

    if figure not supplied it USEs lastest figure of pyplot

    :param fig:
    :param size:
    :param dpi:
    :return:
    """
    fig_file = StringIO()
    if fig is None:  # USE lastest figure
        pyplot.savefig(fig_file, format="svg", dpi=dpi)
    else:
        fig.savefig(fig_file, format="svg", dpi=dpi)
    return f'<svg width="{size[0]}" height="{size[1]}" {fig_file.getvalue().split("<svg")[1]}'


def plt_html(
    fig: Figure = None,
    *,
    title: str = "image",
    format: str = "png",
    size: Tuple[int, int] = (400, 400),
    dpi: int = 100,
):
    """

    if figure not supplied it USEs lastest figure of pyplot

    :param fig:
    :param title:
    :param format:
    :param size:
    :param dpi:
    :return:
    """
    if format == "svg":
        return plt_html_svg(fig, size=size, dpi=dpi)

    import base64

    fig_file = BytesIO()
    if fig is None:  # USE lastest figure
        pyplot.savefig(fig_file, format=format, dpi=dpi)
    else:
        fig.savefig(fig_file, format=format, dpi=dpi)
    fig_file.seek(0)  # rewind to beginning of file
    b64_img = base64.b64encode(fig_file.getvalue()).decode("ascii")
    return (
        f"<img "
        f'width="{size[0]}" '
        f'height="{size[1]}" '
        f'src="data:image/{format};base64,{b64_img}" '
        f'alt="{title}"/><br>'
    )
