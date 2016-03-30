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
    assert hasattr(order, '__getitem__'), TypeError
    assert callable(order.__getitem__), AttributeError
    for c in order:
        assert c in options.keys()

def check_functionality(function):
    if function:
        check_callable(function, TypeError)

def check_page(page):
    for attribute in ('options', 'order'):
        check_attribute(page, attribute, TypeError)
    check_options(page.options)
    check_order(page.order, page.options)
    check_method(page, '__str__', TypeError)
