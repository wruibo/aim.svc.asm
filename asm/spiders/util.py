"""
    util for spider
"""


def json(text, schar=None, echar=None):
    """
        'xxxx(<json string>)'
    :return:
        json对象
    """
    # only eval string between schar and echar
    spos = 0 if schar is None else text.find(schar)
    epos = len(text) if echar is None else text.rfind(echar)
    if spos!=0 or epos!=len(text):
        text = text[spos+1:epos]

    # eval json object
    obj = eval(text, type('Dummy', (dict,), dict(__getitem__=lambda s, n: n))())
    return obj
