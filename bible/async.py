"""
    Copyright (c) 2018 Dane Henson (http://brainofdane.com)

    This file is part of Foo.

    Foo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foo.  If not, see <http://www.gnu.org/licenses/>.

    Authored by: Dane Henson <thegreatdane@gmail.com>
"""

import threading, gi

gi.require_version('Gtk', '3.0')
from gi.repository import GObject

# calls f on another thread
def async_call(f, on_done):
    """
    Starts a new thread that calls f and schedules on_done to be run (on the main
    thread) when GTK is not busy.
    Args:
        f (function): the function to call asynchronously. No arguments are passed
                      to it. f should not use any resources used by the main thread,
                      at least not without locking.
        on_done (function): the function that is called when f completes. It is
                            passed f's result as the first argument and whatever
                            was thrown (if anything) as the second. on_done is
                            called on the main thread, so it can access resources
                            on the main thread.
    Returns:
        Nothing.
    Raises:
        Nothing.
    """

    if not on_done:
        on_done = lambda r, e: None

    def do_call():
        result = None
        error = None

        try:
            result = f()
        except Exception, err:
            error = err

        GObject.idle_add(lambda: on_done(result, error))

    thread = threading.Thread(target = do_call)
    thread.start()

# free function decorator
def async_function(on_done = None):
    """
    A decorator that can be used on free functions so they will always be called
    asynchronously. The decorated function should not use any resources shared
    by the main thread.
    Example:
    @async_function(on_done = do_whatever_done)
    def do_whatever(look, at, all, the, pretty, args):
        # ...
    Args:
        on_done (function): the function that is called when the decorated function
                            completes. If omitted or set to None this will default
                            to a no-op. This function will be called on the main
                            thread.
                            on_done is called with the decorated function's result
                            and any raised exception.
    Returns:
        A wrapper function that calls the decorated function on a new thread.
    Raises:
        Nothing.
    """

    def wrapper(f):
        def run(*args, **kwargs):
            async_call(lambda: f(*args, **kwargs), on_done)
        return run
    return wrapper

# method decorator
def async_method(on_done = None):
    """
    A decorator that can be used on class methods so they will always be called
    asynchronously. The decorated function should not use any resources shared
    by the main thread.
    Example:
    @async_method(on_done = lambda self, result, error: self.on_whatever_done(result, error))
    def do_whatever(self, look, at, all, the, pretty, args):
        # ...
    Args:
        on_done (function): the function that is called when the decorated function
                            completes. If omitted or set to None this will default
                            to a no-op. This function will be called on the main
                            thread.
                            on_done is called with the class instance used, the
                            decorated function's result and any raised exception.
    Returns:
        A wrapper function that calls the decorated function on a new thread.
    Raises:
        Nothing.
    """

    if not on_done:
        on_done = lambda s, r, e: None

    def wrapper(f):
        def run(self, *args, **kwargs):
            async_call(lambda: f(self, *args, **kwargs), lambda r, e: on_done(self, r, e))
        return run
    return wrapper
