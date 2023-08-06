# -*- coding: utf-8 -*-
"""
Contains the definition of the NoOpCommand class.
"""
import logging

from enhterm.command import Command

logger = logging.getLogger('et.unknown')


class UnknownCommand(Command):
    """
    This class .

    Attributes:

    """

    def __init__(self, unknown_content=None, *args, **kwargs):
        """
        Constructor.

        Arguments:

        """
        super().__init__(*args, **kwargs)
        self.unknown_content = unknown_content

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'UnknownCommand()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'UnknownCommand()'

    def execute(self):
        """
        Called by the command loop to do some work.

        The return value will be deposited by the command loop it into
        the `result` member.
        """
        return None

    def encode(self):
        """
        Called when a class instance needs to be serialized.

        .. note:
           The `result` and `uuid` members should not be serialized
           in case of :class:`~Command`.
        """
        return self.unknown_content

    def decode(self, raw_data):
        """
        Apply raw data to this instance.

        It is asserted that correct class has already been constructed
        and that it has `result` and `uuid` members set in case of
        :class:`~Command`..

        Raises:
            DecodeError:
                The implementation should raise this class or a
                subclass of it.

        Arguments:
            raw_data (bytes):
                The data to apply.
        """
        self.unknown_content = raw_data

    @classmethod
    def class_id(cls):
        """
        A unique identifier of the class.

        This value is used as a key when a constructor needs to
        be associated with a string
        (see :class:`enhterm.ser_deser.dsds.DictSerDeSer`).
        """
        return 'unknown'
