from fractions import Fraction


def string_to_float(string):
    return float(sum(Fraction(s) for s in string.split()))


def clear_layout(layout):
    for i in reversed(range(layout.count())): 
        widget = layout.itemAt(i).widget()
        if widget:
            widget.deleteLater()
