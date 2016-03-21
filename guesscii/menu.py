import subprocess
from option import Option

class Menu(object):
    """An interface class that displays information to the user and ac-
    cesses data from its parent Guesscii instance."""

    #-----Public methods-----

    @property
    def get_choice(self):
        """Display the menu to the screen and wait for the user to ent-
        er a valid option.

        Return the user's chosen option."""
        return self.__get_choice

    @property
    def change_settings(self):
        """Not implemented."""
        return self.__change_settings

    #-----Private properties-----

    # Immutable
    @property
    def __parent(self):
        """The parent guesscii object."""
        return self.___parent

    @property
    def __options(self):
        """An ordered list of options keys."""
        return self.___options

    #--------------------------------------------------------------------------


    # -----Public method prescriptors-----

    def __get_choice(self):
        # Display the menu
        subprocess.call("cls", shell=True)
        print self
        option = raw_input("> ")
        if option not in self.__options:
            raise ValueError
        return self.__parent.options[option]

    def __change_settings(self):
        raise NotImplementedError


    # -----Magic methods-----

    def __init__(self, parent):
        """Assumes parent is a Guesscii object."""
        # Defensive programming
        try:
            assert hasattr(parent, 'options'), TypeError
            assert hasattr(parent.options, 'iteritems'), AttributeError
            assert callable(parent.options.iteritems), AttributeError
            for key, option in parent.options.iteritems():
                assert hasattr(key, '__str__'), TypeError
                assert callable(key.__str__), AttributeError
                for attribute in ('key', 'name'):
                    assert hasattr(option, attribute), TypeError
                    option_attribute = getattr(option, attribute)
                    assert hasattr(option_attribute, '__str__'), TypeError
                    assert callable(option.__str__), AttributeError
                assert key == option.key

        except AssertionError as e:
            raise e.args[0]

        self.___parent = parent
        self.___options = ["n", "q", "\n" "s", "h", "i"]

    def __str__(self):
        s = "[Menu]\n\n"
        for key in self.options:
            s += self.parent.options[key].__str__() + "\n"
        return s
