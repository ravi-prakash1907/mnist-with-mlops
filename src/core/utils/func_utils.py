import functools

class decorator(object):
    '''
        Base class for "polite" decorators.
        Handles decorators with or without parameters. (They work VERY differently!) 
        Adapted from https://gist.github.com/kylebgorman/5878715 and http://www.artima.com/weblogs/viewpost.jsp?thread=240845.

        Usage - subclass from decorator, and override _do_().
            class my_decorator(decorator):
                def _do_(self, instance, *args, **kwargs):
                    do_something_before_decorated_function()
                    result = self.function(instance, *args, **kwargs)
                    do_something_after_decorated_function()
                    return result
    '''

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            # The decorator was called without any arguments.
            self.function = args[0]
            self.args = None
            self.kwargs = None
        else:
            # The decorate was called with arguments. We'll have to wait until the call to __call__ to get the function to decorate.
            self.function = None
            self.args = args
            self.kwargs = kwargs

    def __doc__(self):
        return self.function.__doc__

    def __repr__(self):
        return repr(self.function)

    def __str__(self):
        return str(self.function)

    def __name__(self):
        return self.function.__name__

    def __call__(self, *args, **kwargs):
        if self.function:
            return self._do_(*args, **kwargs)
        else:
            self.function = args[0]

            def wrapped_function(instance, *wrapped_args, **wrapped_kwargs):
                return self._do_(instance, *wrapped_args, **wrapped_kwargs)

            return wrapped_function

    # Override this to act as a property.
    def __get__(self, instance, klass=None):
        return functools.partial(self.__call__, instance)

    # Override this!
    def _do_(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class memoized(decorator):
    '''
        Simple memoization (caching) decorator.
        NOTE: Does not handle keyword arguments.

        Usage:
            class MyClass(object):
                @memoized
                def name_of_method(self, arg1):
                    return something_that_takes_a_while_to_compute_or_has_side_effects(arg1)
            my_obj = MyClass()
            my_obj.name_of_method(123)
    '''

    def _do_(self, *args, **kwargs):
        if not hasattr(self, '_memoization_cache'):
            self._memoization_cache = {}
        if not self._memoization_cache.has_key((self.function.__name__, args)):
            self._memoization_cache[(self.function.__name__, args)] = self.function(*args, **kwargs)
        return self._memoization_cache[(self.function.__name__, args)]


class memoized_property(decorator):
    '''
        Simple memoization (caching) decorator for a method that takes no arguments and is used as a property.
        NOTE: This works only for read-only properties; it does not handle getters, setters, or deleters like the built-in @property decorator.

        Usage:
            class MyClass(object):
                @memoized_property
                def name_of_method(self):
                    return something_that_takes_a_while_to_compute_or_has_side_effects()
            my_obj = MyClass()
            my_obj.name_of_method
    '''

    def _do_(self, instance):
        if not hasattr(instance, '_memoization_cache'):
            instance._memoization_cache = {}
        if not instance._memoization_cache.has_key(self.function.__name__):
            instance._memoization_cache[self.function.__name__] = self.function(instance)
        return instance._memoization_cache[self.function.__name__]

    def __get__(self, instance, klass=None):
        return self.__call__(instance)


class class_property(decorator):
    '''
        Simple decorator for a class method that takes no arguments and is used as a property.
        NOTE: This works only for read-only properties; it does not handle getters, setters, or deleters like the built-in @property decorator.

        Usage:
            class MyClass(object):
                @class_property
                def name_of_method(cls):
                    return some_value
            MyClass.name_of_method
    '''

    def _do_(self, instance):
        return self.function(instance)

    def __get__(self, instance, klass):
        return self.__call__(klass)


class memoized_class_method(decorator):
    '''
        Simple memoization (caching) decorator for a class method.
        NOTE: Does not handle keyword arguments.

        Usage:
            class MyClass(object):
                @memoized_class_method
                def name_of_method(cls, arg):
                    return something_that_takes_a_while_to_compute_or_has_side_effects(arg)
            MyClass.name_of_method(123)
    '''

    def _do_(self, *args, **kwargs):
        if not hasattr(self, '_memoization_cache'):
            self._memoization_cache = {}
        if not self._memoization_cache.has_key((self.function.__name__, args)):
            self._memoization_cache[(self.function.__name__, args)] = self.function(*args)
        return self._memoization_cache[(self.function.__name__, args)]


class memoized_class_property(decorator):
    '''
        Simple memoization (caching) decorator for a class method that takes no arguments and is used as a property.
        NOTE: This works only for read-only properties; it does not handle getters, setters, or deleters like the built-in @property decorator.

        Usage:
            class MyClass(object):
                @memoized_class_property
                def name_of_method(cls):
                    return something_that_takes_a_while_to_compute_or_has_side_effects()
            MyClass.name_of_method

    '''

    def _do_(self, klass, *args, **kwargs):
        if not hasattr(klass, '_memoization_cache'):
            klass._memoization_cache = {}
        if not klass._memoization_cache.has_key(self.function.__name__):
            klass._memoization_cache[self.function.__name__] = self.function(klass)
        return klass._memoization_cache[self.function.__name__]

    def __get__(self, instance, klass):
        return self.__call__(klass)


import warnings


class deprecated(decorator):
    '''
        Decorator to declare that a function has been deprecated. Allows optionally providing a string with more information.

        Usage:
            class MyClass(object):
                @deprecated
                def some_function(self):
                    do_something()
                @deprecated('Use some_other_function().')
                def another_function(self):
                    do_something()

    '''

    def _do_(self, *args, **kwargs):
        if self.args:
            message = 'Function "%s" is deprecated - %s' % (self.function.__name__, self.args[0])
        else:
            message = 'Function "%s" is deprecated' % self.function.__name__
        print
        'WARNING: %s' % message
        warnings.warn_explicit(message,
                               category=DeprecationWarning,
                               filename=self.function.func_code.co_filename,
                               lineno=self.function.func_code.co_firstlineno + 1
                               )
        return self.function(*args, **kwargs)


if __name__ == '__main__':
    class MyClass(object):
        '''
            Test that we can use all the decorators defined in this file.
            NOTE: You'll need to manually check the output to make sure everything worked as expected.
        '''

        def __init__(self, x):
            self.x = x

        @class_property
        def class_property(self):
            print
            'Generating class_property - should see this each time we are called'
            return 'class_property'

        @memoized_class_method
        def memoized_class_method(self, arg1):
            print
            'Generating memoized_class_method(%s) - should only see this once for each set of arguments' % arg1
            return 'memoized_class_property(%s)' % arg1

        @memoized_class_property
        def memoized_class_property(self):
            print
            'Generating memoized_class_property - should only see this once'
            return 'memoized_class_property'

        @memoized
        def memoized_method(self, arg1, arg2):
            print
            'Generating memoized_method(%s, %s) - should only see this once for each set of arguments' % (arg1, arg2)
            return 'memoized_method(%s, %s) (x=%s)' % (arg1, arg2, self.x)

        @memoized_property
        def memoized_property(self):
            print
            'Generating memoized_property - should only see this once'
            return 'memoized_property (x=%s)' % self.x

        @deprecated
        def deprecated_method(self):
            print
            'Should see a deprecation warning when calling this.'
            return 'deprecated_method'

        @deprecated('custom deprecation message')
        def deprecated_method_with_custom_message(self):
            print
            'Should see a custom deprecation warning when calling this.'
            return 'deprecated_method_with_custom_message'