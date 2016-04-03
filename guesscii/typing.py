def check_type(obj, type_, e):
    assert type(obj) == type_, e

def check_None(obj, e):
    assert obj is not None, e

def check_callable(obj, e):
    assert callable(obj), e

def check_attribute(obj, attribute, e):
    assert hasattr(obj, attribute), e


def check_method(obj, attribute, e):
    check_attribute(obj, attribute, e)
    check_callable(getattr(obj, attribute), e)

def check_inside(iterator, container, e):
    for arg in (iterator, container):
        try:
            check_method(arg, '__iter__', TypeError)
        except TypeError:
            check_method(arg, '__getitem__', TypeError)
    for item in iterator:
        assert item in container, e

def check_functionality(function, e):
    if function:
        check_callable(function, e)


def check_settings(settings):
    for attribute in ('types', 'length', 'attempts'):
        check_attribute(settings, attribute, TypeError)
        attribute_type = type(getattr(settings, attribute))
        check_type(attribute_type, int, AttributeError)

def check_option(option):
    if type(option) != str:
        for attribute in ('key', 'name'):
            check_attribute(option, attribute, TypeError)
            attribute = getattr(option, attribute)
            check_type(attribute, str, AttributeError)
        check_callable(option, TypeError)

def check_options(options):
    for attribute in ('iteritems', 'keys'):
        check_attribute(options, 'iteritems', TypeError)
        check_callable(options.iteritems, AttributeError)
    for key, option in options.iteritems():
        check_option(option)
        assert key == option.key, KeyError

def check_order(order, options):
    check_method(order, '__getitem__', TypeError)
    check_options(options)
    check_inside(order, options.keys())

def check_page(page):
    for attribute in ('options', 'order'):
        check_attribute(page, attribute, TypeError)
    check_options(page.options)
    check_order(page.order, page.options)
    check_callable(page, TypeError)

def check_combo(combo, settings):
    check_type(combo, str, TypeError)
    check_settings(settings)
    assert len(combo) == settings.length, ValueError
    letters = string.lowercase[:settings.types]
    check_inside(answer, letters)

def check_hint(hint, chars, length):
    check_inside(set(hint), chars)
    assert len(hint) <= length, ValueError

def check_hints(hints, chars, length):
    try:
        check_method(hints, '__getitem__', TypeError)
    except TypeError:
        check_method(hints, '__iter__', TypeError)
    for hint in hints:
        check_hint(hint, chars, length)
