# -*- coding: utf-8 -*-
"""
Contains the definition of the EnhTerm class.
"""
import logging
from typing import Dict, Callable, Any

from enhterm.base import EtBase
from enhterm.ser_deser import SerDeSer
from enhterm.message import Message, TextParagraph
from enhterm.provider import Provider
from enhterm.runner import Runner
from enhterm.variables import VariablesMixin, add_cd_variable, add_cdn_variable
from enhterm.watcher import Watcher
from enhterm.watcher.echo import EchoWatcher
from enhterm.errors import QuitError


logger = logging.getLogger('et')

INITIAL_STATE = 0
PRE_LOOP_STATE = 1
GET_COMMAND_STATE = 2
PRE_COMMAND_STATE = 3
EXEC_COMMAND_STATE = 4
POST_LOOP_STATE = -1


class EnhTerm(VariablesMixin, EtBase):
    """
    Command interpreter.

    The command interpreter implementation is intended to be flexible,
    allowing customisation of individual parts while keeping the rest
    in place. Most of the tasks have an interface class that defines required
    methods and some implementations for common use cases.

    With flexibility in mind the methods of this class perform specific
    duties and can easily be reimplemented in a subclass:
    * :meth:`~cmd_loop` represents the main loop; re-implement if you \
      need complete control over it.
    * :meth:`~pre_loop` and :meth:`~post_loop` are called once each by \
      default implementation of :meth:`~cmd_loop`.
    * :meth:`~one_loop` represents a singly cycle in the main loop and will \
      call:
      * :meth:`~get_command` to retrieve next command;
      * :meth:`~pre_cmd` before executing the retrieved command;
      * :meth:`~execute_command` for obvious reasons;
      * :meth:`~post_cmd` after executing the command;

    Commands
    --------

    Each command to be executed is a subclass of the :class:`~Command` class.
    The interface is very simple, expecting the implementation to
    provide an :meth:`enhterm.command.Command.execute` method.

    For use cases when the commands are to be transmitted or stored
    the implementation also needs to have a
    :meth:`~enhterm.mixins.serializable.Serializable.class_id`, an
    :meth:`~enhterm.mixins.serializable.Serializable.encode` and a
    :meth:`~enhterm.mixins.serializable.Serializable.decode`.

    Providers
    ---------

    The interpreter relies on a stream of commands from a
    :class:`~Provider` class. Providers are arranged in a stack, with the
    top one being the active provider. Internally, the :meth:`~cmd_loop` method
    will repeatedly call the active provider to ask for next command.

    The class can be initialized with a list of providers in the constructor
    and more can be added later via :meth:`~install_provider`. Removing
    a provider is equally simple using :meth:`~uninstall_provider`.

    If a :class:`~Provider` returns `None` when asked for a command it
    will be automatically uninstalled and previous provider in the stack
    will be un-paused. For cases when the provider doesn't have a command
    to return and it cannot block for some reason it should return the
    :class:`~NoOpCommand` command.

    Messages
    --------

    In order to allow for various output formats and other features the code
    does not print directly to the console using traditional means
    such as `print` or `stdout`. Instead messages are being composed from
    a list of paragraphs and are forwarded to the command interpreter
    using the :meth:`~issue_message` method. Convenience methods
    such as :meth:`~info`, :meth:`~error` or :meth:`~warning` will create
    simple messages out of strings.

    Watchers
    --------

    Events received by the command interpreter are forwarded to special
    classes called watchers. The list of events includes the moment when
    main loop starts and ends, commands beginning and ending execution
    and a message being issued.

    In a simple implementation a message being issued while a command
    executes is received using :meth:`~issue_message` which informs
    the :class:`~EchoWatcher`, which prints the message to standard output.

    Packing and Unpacking
    ---------------------

    For times when a command interpreter sends the commands to another
    memory space for execution or when commands or messages need to be
    stored and recreated later the command interpreter can host a
    :class:`~SerDeSer` instance.

    Attributes:
        should_stop(bool):
            If set the main loop will be terminated when current cycle
            is completed.
        prompt (str):
            The text to present to the user on each command line.
        runner (Runner):
            The class that takes a command and translates it into actions.
            Default runner calls simply calls the
            :meth:`~enhterm.command.Command.execute` method of the
            :class:`~enhterm.command.Command`.
        provider_stack (list):
            The stack of providers, with the last one in the list being the
            active one (use :meth:`~provider` to retrieve it).
        watchers (list):
            The list of watchers to be informed about events of this
            command interpreter.
        ser_deser (SerDeSer):
            Intermediary for packing and unpacking commands.
    """

    def __init__(self, providers=None, watchers=None, runner=None,
                 prompt=None, ser_deser=None, *args, **kwargs):
        """
        Constructor.

        Arguments:
            providers (list of Provider, Provider):
                Subclasses of :class:`~enhterm.provider.Provider` which
                provide commands to be executed. For convenience the
                constructor also accepts sets and tuples of
                :class:`~enhterm.provider.Provider` instances, as well as
                a single :class:`~enhterm.provider.Provider`. By default
                the value is `None`.
                The constructor installs the providers in this list (calls install_provider).
            watchers (list of Watcher):
                Subclasses of :class:`~enhterm.watcher.Watcher` which
                are informed about events in this class. For convenience the
                constructor also accepts sets and tuples of
                :class:`~enhterm.watcher.Watcher` instances, as well as
                a single :class:`~enhterm.watcher.Watcher`. By default
                the value is `None`, so no watcher will be installed.
            runner (Runner):
                The class that takes a command and translates it into actions.
                Default runner calls simply calls the
                :meth:`~enhterm.command.Command.execute` method of the
                :class:`~enhterm.command.Command`.
            ser_deser (SerDeSer):
                Intermediary for packing and unpacking commands.
            variables:
        """
        super().__init__(*args, **kwargs)
        self.should_stop = False
        add_cd_variable(self)
        add_cdn_variable(self)
        self.prompt = prompt if prompt else "> "

        if runner:
            self.runner = runner
            self.runner.term = self
        else:
            self.runner = Runner(term=self)

        if ser_deser:
            self.ser_deser = ser_deser
            self.ser_deser.term = self
        else:
            self.ser_deser = SerDeSer(term=self)

        if providers is None:
            providers = []
        elif isinstance(providers, list):
            pass
        elif isinstance(providers, (set, tuple)):
            providers = [provider for provider in providers]
        elif isinstance(providers, Provider):
            providers.term = self
            providers = [providers]
        else:
            raise ValueError("providers argument needs to be a list")

        if watchers is None:
            self.watchers = [EchoWatcher()]
        elif isinstance(watchers, list):
            self.watchers = watchers
        elif isinstance(watchers, (set, tuple)):
            self.watchers = [watcher for watcher in watchers]
        elif isinstance(watchers, Watcher):
            self.watchers = [watchers]
        else:
            raise ValueError("watchers argument needs to be a list")

        self.state = INITIAL_STATE

        self.provider_stack = []
        for provider in providers:
            self.install_provider(provider)
        for watcher in self.watchers:
            watcher.term = self

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'EnhTerm()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'EnhTerm()'

    @property
    def provider(self):
        """ Get the active command provider. """
        return self.provider_stack[-1]

    def cmd_loop(self):
        """
        Repeatedly get a command and execute it (main loop).

        The method executes one :meth:`pre_loop`, one :meth:`post_loop`
        and a bunch of :meth:`one_loop` in-between, which is expected
        to return `False`` when it wants to break the main loop.
        """
        self.pre_loop_state = True
        self.pre_loop()

        while not self.should_stop:
            try:
                if not self.one_loop():
                    break
            except (SystemExit, SystemError, KeyboardInterrupt):
                self.should_stop = True

        self.post_loop_state = True
        self.post_loop()

    def one_loop(self):
        """
        :meth:`~cmd_loop` repeatedly calls this method.

        Returns:
            True
                The loop should continue.
            False
                The loop should stop.
        """
        
        self.get_command_state = True
        command = self.get_command()
        if command is None:
            self.should_stop = True
            return False

        self.pre_command_state = True
        command = self.pre_cmd(command)
        if command is None:
            self.should_stop = True
            return False

        self.execute_command_state = True
        try:
            command.result = self.execute_command(command)
        except QuitError:
            self.post_cmd(command)
            self.should_stop = True
            return False

        if not self.post_cmd(command):
            self.should_stop = True
            return False

        return True

    def pre_loop(self):
        """
        Method executed once when the :meth:`~cmd_loop()` method is called.

        Default implementation  notifies all watchers about this event.
        """
        for watcher in self.watchers:
            try:
                watcher.pre_loop()
            except (SystemExit, SystemError, KeyboardInterrupt):
                raise
            except Exception as exc:
                self.handle_watcher_exception(watcher, 'pre_loop', exc)

    def post_loop(self):
        """
        Method executed once when the :meth:`~cmd_loop()` method is
        about to return.

        Default implementation  notifies all watchers about this event.
        """
        for watcher in self.watchers:
            try:
                watcher.post_loop()
            except (SystemExit, SystemError, KeyboardInterrupt):
                raise
            except Exception as exc:
                self.handle_watcher_exception(watcher, 'post_loop', exc)

    def pre_cmd(self, command):
        """
        Method executed just before the command is executed.

        Default implementation notifies all watchers about this event.
        By design, these can only modify the command (they cannot return a
        different command). To gain the ability to return a different command
        this method needs to be reimplemented in a subclass.

        Arguments:
            command (Command):
                The command as procured by :meth:`get_command()'.

        Returns:
            command (Command):
                Default implementation simply returns same command.
                The subclass implementing this method can return any command
                it sees fit.
            None:
                If the implementation returns None the default
                implementation of :meth:`~cmd_loop` will set `should_stop`
                flag which terminates command loop.
        """
        for watcher in self.watchers:
            try:
                watcher.pre_cmd(command)
            except (SystemExit, SystemError, KeyboardInterrupt):
                raise
            except Exception as exc:
                self.handle_watcher_exception(watcher, 'pre_cmd', exc)
        return command

    def post_cmd(self, command):
        """
        Method executed just after a command dispatch is finished.

        Default implementation notifies all watchers about this event.
        By design, these can only modify the command (they cannot return a
        different command). To gain the ability to return a different command
        this method needs to be reimplemented in a subclass.

        Arguments:
            command (Command):
                The command that was just executed by
                :meth:`execute_command()'.

        Returns:
            True:
                The default implementation of :meth:`~cmd_loop` will
                continue the command loop if `True` is returned.
            False:
                The default implementation of :meth:`~cmd_loop` will
                set `should_stop` flag which terminates command loop
                in response to `False` being returned.
        """
        for watcher in self.watchers:
            try:
                watcher.post_cmd(command)
            except (SystemExit, SystemError, KeyboardInterrupt):
                raise
            except Exception as exc:
                self.handle_watcher_exception(watcher, 'post_cmd', exc)
        return True

    def get_command(self):
        """
        The method that obtains the next command to execute.

        The method asks current provider to
        :meth:`~enhterm.provider.Provider.get_command`. If the response is
        `None` then the provider is uninstalled via
        :meth:`~uninstall_provider` and next provider in the stack
        is asked the same thing. If no provider is left then None is returned,
        which terminates the command loop.

        Returns:
            command (Command):
                The command to be executed next.
            None:
                The default implementation of :meth:`~cmd_loop`
                will set `should_stop` flag which terminates command loop.
        """

        while True:
            if len(self.provider_stack) == 0:
                return None
            provider = self.provider

            try:
                command = provider.get_command()
            except (SystemExit, SystemError, KeyboardInterrupt):
                raise
            except Exception as exc:
                self.handle_provider_exception(provider, 'get_command', exc)
                command = None

            if command is None:
                self.uninstall_provider(provider)
            else:
                return command

    def execute_command(self, command):
        """
        The method executes the next command.

        Default implementation asks the `runner` to execute the command.
        Default :class:`~enhterm.runner.Runner` will call the
        :meth:`~enhterm.command.Command.execute` method of the
        :class:`~enhterm.command.Command`.

        Arguments:
            command (Command):
                The command to be executed.

        Returns:
            type:
                The result is whatever the command returns.
                The :meth:`~cmd_loop` will deposit this in `result` member
                of the :class:`~enhterm.command.Command`.
        """
        command.term = self
        if command.provider is None:
            command.provider = self.provider
        return self.runner(command)

    def install_provider(self, provider):
        """
        Adds a command provider to the stack and makes it active.

        Arguments:
            provider (Provider):
                The provider to install.
        """
        old_provider = None
        if len(self.provider_stack) > 0:
            old_provider = self.provider
            try:
                old_provider.pause(provider)
            except (SystemExit, SystemError, KeyboardInterrupt):
                raise
            except Exception as exc:
                self.handle_provider_exception(provider, 'pause', exc)
                self.uninstall_provider(old_provider)
                if len(self.provider_stack) > 0:
                    old_provider = self.provider
        try:
            provider.term = self
            provider.start(old_provider)
            self.provider_stack.append(provider)
        except (SystemExit, SystemError, KeyboardInterrupt):
            raise
        except Exception as exc:
            self.handle_provider_exception(provider, 'start', exc)

    def uninstall_provider(self, provider):
        """
        Remove a provider from the stack.

        The provider if first stopped, then it is removed from the stack.
        If it is the active provider then next provider in the stack is made
        active and it is informed about the event via
        :meth:`~enhterm.provider.Provider.unpause`.

        Arguments:
            provider (Provider):
                The provider to remove.
        """
        try:
            provider.stop()
            provider.term = None
        except (SystemExit, SystemError, KeyboardInterrupt):
            raise
        except Exception as exc:
            self.handle_provider_exception(provider, 'stop', exc)

        if provider == self.provider:
            self.provider_stack.pop()
            if len(self.provider_stack) == 0:
                return
            provider = self.provider

            try:
                provider.unpause()
            except (SystemExit, SystemError, KeyboardInterrupt):
                raise
            except Exception as exc:
                self.handle_provider_exception(provider, 'stop', exc)
                self.uninstall_provider(provider)
        else:
            self.provider_stack.remove(provider)

    def handle_watcher_exception(self, watcher, location, exc):
        """
        Method informed that one of the watchers has raised an exception.

        Default implementation simply logs the error at `WARNING` level.

        Arguments:
            watcher (Watcher):
                The watcher that raised the exception.
            location (str):
                The name of the method where this was caught.
            exc (Exception):
                The exception that was raised.
        """
        logger.warning("Exception thrown by %r in %r",
                       watcher, location, exc_info=True)

    def handle_provider_exception(self, provider, location, exc):
        """
        Method informed that one of the watchers has raised an exception.

        Default implementation of this method simply logs the error at
        `ERROR` level. Note, however, that the provider is uninstalled
        by the caller.

        Arguments:
            provider (Provider):
                The provider that raised the exception.
            location (str):
                The name of the method where this was caught.
            exc (Exception):
                The exception that was raised.
        """
        logger.error("Exception thrown by %r in %r",
                     provider, location, exc_info=True)

    @property
    def pre_loop_state(self):
        return self.state == PRE_LOOP_STATE

    @pre_loop_state.setter
    def pre_loop_state(self, value):
        self.state = PRE_LOOP_STATE

    @property
    def get_command_state(self):
        return self.state == GET_COMMAND_STATE

    @get_command_state.setter
    def get_command_state(self, value):
        self.state = GET_COMMAND_STATE

    @property
    def pre_command_state(self):
        return self.state == PRE_COMMAND_STATE

    @pre_command_state.setter
    def pre_command_state(self, value):
        self.state = PRE_COMMAND_STATE

    @property
    def execute_command_state(self):
        return self.state == EXEC_COMMAND_STATE

    @execute_command_state.setter
    def execute_command_state(self, value):
        self.state = EXEC_COMMAND_STATE

    @property
    def post_loop_state(self):
        return self.state == POST_LOOP_STATE

    @post_loop_state.setter
    def post_loop_state(self, value):
        self.state = POST_LOOP_STATE

    def info(self, text, severity=logging.INFO):
        """
        Issue an informative message.

        The method creates a :class:`~Message` with a single
        :class:`~TextParagraph` which it forwards to :meth:`~issue_message`.

        Arguments:
            text (str):
                The content of the message.
            severity (int):
                The severity of this message. One of the logging constants
                can be used here.
        """
        message = Message(term=self, severity=severity, paragraphs=[
            TextParagraph(text)
        ])
        self.issue_message(message)

    def warning(self, text):
        """
        Issue a warning message.

        The method creates a :class:`~Message` with a single
        :class:`~TextParagraph` which it forwards to :meth:`~issue_message`.

        Arguments:
            text (str):
                The content of the message.
        """
        message = Message(term=self, severity=logging.WARNING, paragraphs=[
            TextParagraph(text)
        ])
        self.issue_message(message)

    def error(self, text: str):
        """
        Issue an error message.

        The method creates a :class:`~Message` with a single
        :class:`~TextParagraph` which it forwards to :meth:`~issue_message`.

        Arguments:
            text (str):
                The content of the message.
        """
        message = Message(term=self, severity=logging.ERROR, paragraphs=[
            TextParagraph(text)
        ])
        self.issue_message(message)

    def issue_message(self, message):
        """
        The terminal is issuing a message.

        All the output destined to the user should go through this method.

        Default implementation informs all watchers about the message.
        """
        if message.term is None:
            message.term = self
        for watcher in self.watchers:
            try:
                watcher.message_issued(message)
            except (SystemExit, SystemError, KeyboardInterrupt):
                raise
            except Exception as exc:
                self.handle_watcher_exception(watcher, 'message_issued', exc)
