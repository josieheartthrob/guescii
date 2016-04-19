def check(checks):
    try:
        for d in checks:
            d['function'](*d['args'])
    except AssertionError as e:
        raise e.args[0]

def obj_type(obj, type_obj, e):
    assert type(obj) == type_obj, e

def if_None(obj, e):
    assert obj is not None, e

def obj_callable(obj, e):
    assert callable(obj), e

def attribute(obj, attr, e):
    assert hasattr(obj, attr), e


def method(obj, attr, e):
    attribute(obj, attr, e)
    obj_callable(getattr(obj, attr), e)

def inside(iterator, container, e):
    for arg in (iterator, container):
        try:
            method(arg, '__iter__', TypeError)
        except TypeError:
            method(arg, '__getitem__', TypeError)
    for item in iterator:
        assert item in container, e

def functionality(function, e):
    if function:
        obj_callable(function, e)

def settings(settings):
    for attr in ('types', 'length', 'attempts'):
        attribute(settings, attr, TypeError)
        attr_type = type(getattr(settings, attr))
        type(attr_type, int, AttributeError)

def option(opt):
    if type(opt) != str:
        for attr in ('key', 'name'):
            attribute(opt, attr, TypeError)
            attr = getattr(opt, attr)
            obj_type(attr, str, AttributeError)
        obj_callable(opt, TypeError)

def options(opts):
    for attr in ('iteritems', 'keys'):
        method(opts, attr, AttributeError)
    for key, opt in opts.iteritems():
        option(opt)
        assert key == opt.key, KeyError

def order(order, opts):
    method(order, '__getitem__', TypeError)
    options(opts)
    inside(order, opts.keys(), ValueError)

def page(page):
    for attr in ('options', 'order'):
        attribute(page, attr, TypeError)
    options(page.options)
    order(page.order, page.options)
    obj_callable(page, TypeError)

def combo(combo, settings):
    type(combo, str, TypeError)
    settings(settings)
    assert len(combo) == settings.length, ValueError
    letters = string.lowercase[:settings.types]
    inside(answer, letters)

def hint(hint, chars, length):
    inside(set(hint), chars)
    assert len(hint) <= length, ValueError

def hints(hints, chars, length):
    try:
        method(hints, '__getitem__', TypeError)
    except TypeError:
        method(hints, '__iter__', TypeError)
    for hint in hints:
        hint(hint, chars, length)
