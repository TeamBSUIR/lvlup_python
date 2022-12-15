import base64
from io import BytesIO
import matplotlib.pyplot as plt


def get_months_numbs_and_names():
    """
    returns numbers and related month's names
    """
    months_dictionary = {
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
    return months_dictionary


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
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    data = [float(x) for x in sizes]
    labs = [x for x in labels]

    wedges, texts = ax.pie(data, textprops=dict(color="w"))

    ax.legend(
        wedges,
        labs,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    ax.set_title("Purchase statistics")

    fig.patch.set_facecolor("#b3d4e8")
    fig.patch.set_alpha(0.6)

    return get_graph()
