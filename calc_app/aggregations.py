from .models import ExpenseItem


def get_categories_costs(names):
    """
    calculates the purchases cost per category
    """
    name_dict = {name: 0 for name in names}
    for item in ExpenseItem.objects.all().select_related("category"):
        name_dict[item.category.name] += item.cost
    return list(name_dict.values())
