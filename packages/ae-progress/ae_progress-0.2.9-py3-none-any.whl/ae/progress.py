"""
display progress of long running processes
==========================================

this module is simplifying the display of progress messages on the command console/shell of your OS for long running
processes.


basic usage of progress portion
-------------------------------

create an instance of the :class:`Progress` for each process/thread your application spawns::

    from ae.core import SubApp
    from ae.progress import Progress

    app = SubApp(...)
    ...
    progress = Progress(app, ...)

now you can call the :meth:`~Progress.next` method within your long running process on each processed item/percentage::

    while process_is_not_finished:
        ...
        progress.next()

optionally you can request to print an end-message by calling the :meth:`~Progress.finished` method of your
:class:`Progress` instance as soon as the process is finished::

    ...
    progress.finished()

the above code snippets are printing a start message to your console at the instantiation of :class:`Progress`. then
every call of the method :meth:`~Progress.next` will print the next message and finally the method
:meth:`~Progress.finished` will print an end message.

to use the integrated error counter and automatic printout of an error message to the console, pass the message text of
any occurring error to the argument :paramref:`~Progress.next.error_msg` of :meth:`~Progress.next` or
:meth:`~Progress.finished`.


progress instantiation
----------------------

the :paramref:`first argument <Progress.app_base>` expects the
instance of the application class (either :class:`~ae.core.AppBase`,
:class:`~ae.core.SubApp` or :class:`~ae.console.ConsoleApp`) that spawns the process.

the next three arguments are configuring a run or item counter. and the other arguments may be used to adopt the format
of the displayed messages to your needs.


process run counter
^^^^^^^^^^^^^^^^^^^

depending on the type of process you want to show progress differently, e.g. on each processed item or after passing a
certain percentage value and either as incrementing or decrementing number. for that :class:`Progress` provides a
counter which can be flexible configured with the arguments :paramref:`~Progress.start_counter` and
:paramref:`~Progress.total_count`.

specifying only :paramref:`~Progress.start_counter` results in a countdown. e.g. to display the number of items waiting
to be processed::.

    progress = Progress(app, number_of_items_to_be_processed)

by only specifying :paramref:`~Progress.total_count` you get an incremental process run counter::

    progress = Progress(app, total_count=number_of_items_to_be_processed)

to display a percentage on the console in 5 percent steps specify :paramref:`~Progress.total_count`
as 100 percent and :paramref:`~Progress.delta` as +5::

    progress = Progress(app, total_count=100, delta=5)


individual message templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

progress displays 5 types of messages on the console. to overwrite one of the generic default message templates, simply
pass your template on instantiation of :class:`Progress` into the argument that is displayed underneath directly after
the message type:

* *start* - :paramref:`~Progress.start_msg`
    start message printed on process start and class instantiation
* *next* - :paramref:`~Progress.next_msg`
    next run message (printed on each call of :meth:`~Progress.next`)
* *end* - :paramref:`~Progress.end_msg`
    finished message (printed on call of :meth:`~Progress.finished`)
* *error* - :paramref:`~Progress.err_msg`
    error message on any occurring error (printed on each call of
    either :meth:`~Progress.next` or :meth:`~Progress.finished`)
* *nothing-to_do* - :paramref:`~Progress.nothing_to_do_msg`
    nothing-to-do message printed on process start (class instantiation) if total count is zero

the following table shows which progress state placeholders you can use in which message type:

.. list-table::
    :header-rows: 1
    :stub-columns: 1
    :widths: 15 30

    * - *placeholder*
      - *available in message type*
    * - run_counter
      - *start, next, end, error*
    * - total_count
      - *start, next, end, error*
    * - processed_id
      - *next, end, error*
    * - err_counter
      - *next, end, error*
    * - err_msg
      - *next, end, error*

.. hint::
   only the *nothing-to-do* message type does not provide any placeholders.

"""
from typing import Optional

# noinspection PyProtectedMember
from ae.core import AppBase, _LOGGER        # type: ignore      # mypy


__version__ = '0.2.9'


class Progress:
    """ display progress on the console/log output for a long running tasks.
    """
    def __init__(
            self, app_base: AppBase,
            start_counter: int = 0, total_count: int = 0, delta: int = -1,
            # templates to display messages on process start, run, end, on error if nothing-to-do
            start_msg: str = "", next_msg: Optional[str] = "",
            end_msg: str = "Finished processing of {total_count} having {err_counter} failures:¡{err_msg}!",
            err_msg: str = "{err_counter} errors on processing {total_count} items, current={run_counter}:¡{err_msg}!",
            nothing_to_do_msg: str = ''):
        """ prepare print-outs for a new progress (long running process with incrementing or decrementing item counter).

        :param app_base:            instance of the application class that is spawning the long-running process.
        :param start_counter:       process item counter start value.
                                    counter decrements on each call of :meth:`~Progress.next` (if
                                    :paramref:`~Progress.total_count` not specified).
        :param total_count:         number of items that will be processed with an incrementing counter.
                                    by passing a positive integer the process item counter will be incremented
                                    on each call of :meth:`~Progress.next`.
        :param delta:               difference to decrement/increment on each call of :meth:`~Progress.next`.
        :param start_msg:           start message template with placeholders.
        :param next_msg:            next message - if an empty string get passed then a default message
                                    will be provided with placeholders - pass None if you want to suppress the
                                    print-out of a next message.
        :param end_msg:             end message template with placeholders, pass None if you want to suppress the
                                    print-out of an end message (in this case only a new line will be printed).
        :param err_msg:             error message template with placeholders.
        :param nothing_to_do_msg:   message template printed-out if the values of the two arguments
                                    :paramref:`~Progress.start_counter` and :paramref:`~Progress.total_count` are
                                    not specified or are both less or equal to zero.
        """
        self._app: AppBase = app_base                       #: used :class:`application class <core.AppBase>` instance
        if next_msg == "":
            next_msg = "Processing '{processed_id}': " + \
                       ("left" if start_counter > 0 and total_count == 0 else "item") + \
                       " {run_counter} of {total_count}. {err_counter} errors:¡{err_msg}!"

        def _complete_msg_prefix(msg, pch='#'):
            return (pch in msg and msg) or msg and " " + pch * 3 + "  " + msg or ""

        self._next_msg = _complete_msg_prefix(next_msg)     #: next message template
        self._end_msg = _complete_msg_prefix(end_msg)       #: end message template
        self._err_msg = _complete_msg_prefix(err_msg, '*')  #: error message template

        self._err_counter = 0                               #: error counter
        self._run_counter = start_counter - delta           #: item, percentage or run counter
        self._total_count = start_counter                   #: total count of item/percentage/run counter
        self._delta = delta                                 #: delta value to increment/decrement run counter
        if total_count > 0:  # incrementing run_counter
            self._run_counter = start_counter
            self._total_count = total_count
            self._delta = abs(delta)
        elif start_counter <= 0:
            if nothing_to_do_msg:
                self._app.po(_complete_msg_prefix(nothing_to_do_msg), logger=_LOGGER)
            return  # RETURN -- empty set - nothing to process

        if start_msg:
            self._app.po(_complete_msg_prefix(start_msg).format(run_counter=self._run_counter + self._delta,
                                                                total_count=self._total_count), logger=_LOGGER)

    def next(self, processed_id: str = '', error_msg: str = '', next_msg: str = '', delta: int = 0):
        """ log the processing of the next item of this long-running task.

        :param processed_id:    id(s) of the next item (to be displayed on console/logging output).
        :param error_msg:       pass the error message to display if the next item produced any errors. if an error
                                message get passed then the :attr:`~Progress._err_counter` will be incremented.
        :param next_msg:        message to output (use instance message if not passed/empty).
        :param delta:           delta for decrement/increment process run counter (use instance default if not passed).
        """
        self._run_counter += delta or self._delta
        if error_msg:
            self._err_counter += 1

        params = dict(run_counter=self._run_counter, total_count=self._total_count, processed_id=processed_id,
                      err_counter=self._err_counter, err_msg=error_msg)
        if error_msg and self._err_msg:
            self._app.po(self._err_msg.format(**params), logger=_LOGGER)

        if not next_msg:
            next_msg = self._next_msg
        if next_msg:
            # using print_out()/po() with end parameter instead of leading \r will NOT get displayed within PyCharm,
            # .. also not with flush - see http://stackoverflow.com/questions/34751441/
            # when-writing-carriage-return-to-a-pycharm-console-the-whole-line-is-deleted
            # .. po('   ', pend, end='\r', flush=True)
            next_msg = '\r' + next_msg
            self._app.po(next_msg.format(**params), logger=_LOGGER)

    def finished(self, processed_id: str = '', error_msg: str = ''):
        """ display end of processing for the current item.

        :param processed_id:    id(s) of the next item (to be displayed on console/logging output).
        :param error_msg:       optional error message to display if current items produced any error. if an error
                                message get passed then the :attr:`~Progress._err_counter` will be incremented.
        """
        if error_msg:
            self._err_counter += 1
            if self._end_msg:
                self._app.po(self._err_msg.format(
                    run_counter=self._run_counter, total_count=self._total_count, processed_id=processed_id,
                    err_counter=self._err_counter, err_msg=error_msg),
                             logger=_LOGGER)
        self._app.po(self.get_end_message(error_msg=error_msg), logger=_LOGGER)

    def get_end_message(self, processed_id: str = '', error_msg: str = '') -> str:
        """ determine message text for finishing the currently processed item.

        :param processed_id:    id(s) of the next item (to be displayed on console/logging output).
        :param error_msg:       optional error message to display if current items produced any error.
        :return:                message text to display.
        """
        return self._end_msg.format(
            run_counter=self._run_counter, total_count=self._total_count, processed_id=processed_id,
            err_counter=self._err_counter, err_msg=error_msg)
