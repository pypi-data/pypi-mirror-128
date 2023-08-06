# -*- coding: utf-8 -*-
"""
Contains the definition of the Command class.
"""
import logging
from uuid import uuid4

from enhterm.base import EtBase
from enhterm.mixins.serializable import Serializable

logger = logging.getLogger('et.c')


class Command(Serializable, EtBase):
    """
    A command.

    The only requirement for implementations of this class is to implement
    the :meth:`~execute` method. The command loop will take the returned
    value of this method and deposit it into the `result` member.

    An implementation can be as simple as:
    >>> from enhterm.command import Command
    >>> class PrintCommand(Command):
    >>>     def execute(self):
    >>>         print("Hello world")

    Attributes:
        term (EnhTerm):
            The terminal that is executing this command. Prior to
            :meth:`~execute` this value is set by the terminal.
        provider:
            The :class:`~enhterm.provider.Provider` instance that generated
            this command. The terminal only sets this value to point to the
            active provider if it is found to be `None` prior to :meth:`~execute`.
        result:
            The result of :meth:`~execute`, `None` until then.
        uuid:
            Unique identifier of this instance.
    """

    def __init__(self, term=None, provider=None, *args, **kwargs):
        """ Constructor. """
        super().__init__(*args, **kwargs)
        self.term = term
        self.provider = provider
        self.result = None
        self.uuid = uuid4()

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return f'Command({self.uuid})'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return f'Command(term={self.term}, ' \
            f'provider={self.provider}, ' \
            f'result={self.result}, uuid={self.uuid})'

    def execute(self):
        """
        Called by the command loop to do some work.

        The return value will be deposited by the command loop it into
        the `result` member.
        """
        raise NotImplementedError
