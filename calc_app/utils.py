import base64
from io import BytesIO
import matplotlib.pyplot as plt


def get_month_name(month_number):
    """
    returns the name of the month given in number
    """
    dct = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }
    return dct[month_number]


def get_months_numbs_and_names():
    """
    returns numbers and related month's names
    """
    months = {}
    for i in range(1, 13):
        months[i] = get_month_name(i)
    return months


def get_graph():
    """
    returns graph image
    """
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph


def get_plot(sizes, labels):
    """
    builds and returns graph
    """
    plt.switch_backend("AGG")
    plt.figure(figsize=(9, 5))
    figure, axes = plt.subplots()
    axes.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    axes.axis("equal")
    figure.patch.set_facecolor("#b3d4e8")
    figure.patch.set_alpha(0.6)
    graph = get_graph()
    return graph
