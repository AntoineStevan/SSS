import argparse
import difflib


def strad(string):
    """
        Converts a string into its representation, i.e. integer, float or bool, if possible.

        Args:
            string (str): the string representation one wants to convert to its 'true' value.

        Return:
            (str, int, float, bool) the 'true' value of the input string representation.
    """
    if string.__class__.__name__ != "str":
        return string

    if string in ["True", "False"]:
        return bool(string)

    if string.isdigit():
        return int(string)

    elif string.replace('.', '', 1).isdigit():
        return float(string)

    return string


class StoreDictKeyPair(argparse.Action):
    """
        A wrapper of the Action class from the argparse module. Allows to store argument in dictionaries.
    """

    def __init__(self, option_strings, dest, nargs='*', **kwargs):
        """
            A constructor for the StoreDictKeyPair class.

            Args:
                option_strings (list of strings): given by the parser -> all the possible flag names.
                dest (str): given by the parser -> the name of the destination of the dictionary.
                nargs (str): given by the parser -> the string representing the number of arguments possible.
                kwargs (dict[str, any]): given by the parser -> all the other arguments used by the parser
                    (choices, help, ...)

            Return:
                (StoreDictKeyPair) the constructed object.
        """
        # it is the default parameter which tells if the overall flag is activated or not.
        self.on = None if "default" not in kwargs else bool(kwargs["default"])

        super(StoreDictKeyPair, self).__init__(option_strings, dest, nargs=nargs, **kwargs)

        # build the default dictionary using strings in choices, of the form "name:type:default".
        self.default = {}
        self._types = []
        if self.choices is not None:
            for choice in self.choices:
                name, typ, default = choice.split(':')  # split the strings.
                self._types.append(typ)  # store the type.
                self.default[name] = default  # make a new name-default pair.
        self.choices = None  # erase useless choices.

        self._nb_propositions = 2  # the number of choices printed by the auto completion on typos.

        # build the format.
        self.format = None
        if len(self.default) != 0:
            self.format = f"python path/to/main.py [*] "
            _arg_format = "{}=<{}> ({})"
            _full_arg_format = ("{: >" + str(len(self.format)) + "}").format('') + _arg_format
            self.format = "".join(
                [self.format + _arg_format] + ['\n' + _full_arg_format] * (len(self.default.keys()) - 1))
            self.format += " [--other-flags]"

            values = [None] * len(self.default.keys()) * 3
            values[0::3] = self.default.keys()
            values[1::3] = self.default.values()
            values[2::3] = self._types
            self.format = self.format.format(*values)

        # add the activation field.
        if self.on is not None:
            self.default["on"] = self.on

    def __call__(self, parser, namespace, values, option_string=None):
        """
            Called when the parser parses the arguments.

            Args:
                parser (ArgumentParser): the actual parser.
                namespace (Namespace): the namespace of the parser, used to attribute the built dictionary to
                    destination.
                values (list of str): all the values given by the user.
                option_string (str): the user chosen option string.

            Return:
                (None)

            Throws:
                (ValueError) raised when input is not of the form KEY=VAL, treated as a Warning.
                (TypeError) raised when a user chosen key is not available.
        """
        my_dict = dict(self.default)
        k = ''
        for kv in values:
            try:
                k, v = kv.split("=")
                if len(self.default) != 0:
                    if k not in self.default.keys():
                        raise TypeError()
                my_dict[k] = v
            except ValueError:
                warning_msg = f"usage of {' or '.join(self.option_strings)} ([*]):" + '\n' + self.format
                raise Warning("CUSTOM" + warning_msg)
            except TypeError:
                error_msg = f"unknown argument name '{k}' for {' and '.join(self.option_strings)}\n"
                matches = difflib.get_close_matches(k, self.default.keys(), n=self._nb_propositions)
                if matches:
                    error_msg += f"\tdid you mean: {' or '.join(matches)}?"
                else:
                    error_msg += f"possible argument names for " + \
                                 "{}:\n\t{}".format(' and '.join(self.option_strings), ", ".join(self.default.keys()))
                raise ValueError("CUSTOM" + error_msg)
        # my_dict["on"] = True

        for k, v in my_dict.items():
            my_dict[k] = strad(v)

        setattr(namespace, self.dest, my_dict)
