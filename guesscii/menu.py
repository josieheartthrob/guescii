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
    def __options(self):
        """A dictionary where each key is a string and each item is an option object."""
        return self.___parent

    @property
    def __option_order(self):
        """An ordered list of options keys."""
        return self.___option_order

    #--------------------------------------------------------------------------


    # -----Public method prescriptors-----

    def __get_choice(self):
        # Display the menu
        subprocess.call("cls", shell=True)
        print self
        option = raw_input("> ")
        if option not in self.__option_order:
            raise ValueError
        return self.__parent.options[option]

    def __change_settings(self):
        raise NotImplementedError
        restore_defaults = ''
        while restore_defaults not in ('y', 'n'):
            restore_defaults =  raw_input('restore_defaults? y | n\n\n>')


        types = raw_input('amount of guessing letters > ')
        length = raw_input('combination length > ')
        attempts = raw_input('attempts allowed > ')

    # def customize_settings():
    #     """returns a settings dictionary"""
    #
    #     restore_defaults = raw_input("restore defaults? y | n\n\n> ")
    #     while restore_defaults not in ("y", "n"):
    #         restore_defaults = raw_input(
    #             "invalid input\nplease type \"y\" or \"n\":\n\n> ")
    #
    #     if restore_defaults == "n":
    #         settings = {"guess types": 0, "combination length": 0, "guesses": 0}
    #         settings["guess types"] = ensure_int(
    #             "amount of guess types: ", sign="positive")
    #         settings["combination length"] = ensure_int(
    #             "length of each guess: ", sign="positive")
    #         settings["guesses"] = ensure_int(
    #             "amount of guesses: ", sign="positive")
    #     else:
    #         settings = get_defaults()
    #     return settings


    # -----Magic methods-----

    def __init__(self, options, order=["n", "q", "\n", "s", "h", "i"]):
        """Assumes options is a dictionary.

        Each key  is a string, and if the item  is an object the key is
            the same as the relative item's key attribute
        Each item is either an option object or a string."""
        # Defensive programming
        try:
            # check options
            assert hasattr(options, 'iteritems'), TypeError
            assert callable(options.iteritems), AttributeError
            for key, option in options.iteritems():
                assert type(key) == str, TypeError
                if type(option) != str:
                    for attribute in ('key', 'name'):
                        assert hasattr(option, attribute), TypeError
                        option_attribute = getattr(option, attribute)
                        assert type(option_attribute), TypeError
                    assert key == option.key
                    assert callable(option)

            # check order
            assert hasattr(order, '__getitem__'), TypeError
            assert callable(order, '__getitem__'), AttributeError
            for c in order:
                assert type(c) == str
                assert c in options.keys()

        except AssertionError as e:
            raise e.args[0]

        # Initialize attributes
        self.___options = options
        self.___option_order = order

    def __str__(self):
        s = "[Menu]\n\n"
        for key in self.__option_order:
            s += self.__options[key].__str__() + "\n"
        return s
