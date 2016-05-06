class Option(object):
    """An option to display and call.

    Options can be displayed to the user by printing them. They can also be
    called for their functionality.

    Public Properties:
        key ---- the string that should be used as a key to access
                   the option when creating an option dictionary.
        name --- the string display to the user as the option's name."""

    #-----Public properties-----

    # Immutable
    @property
    def key(self):
        return self._key

    @property
    def name(self):
        return self._name


    #-----Private properties-----

    @property
    def _function(self):
        # The functionality of the option
        return self.__function


    #-----Magic methods-----

    def __init__(self, key, name, function):
        """Create an option object

        Arguments:
            key --------- a string to access the option from a
                            dictionary.
            name -------- a string to display as the option name.
            function ---- a callable object that gives the option
                            functionality.
        """
        # Defensive programming
        try:
            assert type(key) in (str, int, float, long), TypeError(
                'key must be a string or number')
            assert type(name) is str, TypeError('name must be a string')
            assert callable(function), TypeError(
                'function must be a callable object')
        except AssertionError as e:
            raise e.args[0]

        self._key = key
        self._name = name
        self.__function = function

    def __str__(self):
        return '> {0.key} - {0.name}'.format(self)

    def __call__(self, *args, **kwargs):
        return self._function(*args, **kwargs)

def test():
    from subprocess import call
    def f(something):
        call('cls', shell=True)
        print something
    option = Option('h', 'say hello', f)
    key = ''
    while key != 'h':
        call('cls', shell=True)
        print option
        key = raw_input('\n> ')
    option('Hello, world.')

if __name__ == '__main__':
    test()
