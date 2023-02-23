# -*- coding: utf-8 -*-
# author:杜顺东
# time:2023/2/11 17:19
# email:my_dsd@126.com

# encoding: utf-8

import ast
import builtins
import collections
import json
import re
import types
builtin_str = str
str = str
bytes = bytes
basestring = (str, bytes)
numeric_types = (int, float)
integer_types = (int,)
from automaticTestingFramework.get_eval_data import builtin

# use $$ to escape $ notation
dolloar_regex_compile = re.compile(r"\$\$")
# variable notation, e.g. ${var} or $var
variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")
# function notation, e.g. ${func1($var_1, $var_3)}
function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\w\.\-/\s=,]*)\)\}")

""" Store parse failed api/testcase/testsuite file path
"""
parse_failed_testfiles = {}


def get_parse_failed_testfiles():
    return parse_failed_testfiles


def parse_string_value(str_value):
    """ parse string to number if possible
    e.g. "123" => 123
         "12.2" => 12.3
         "abc" => "abc"
         "$var" => "$var"
    """
    try:
        return ast.literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        # e.g. $var, ${func}
        return str_value


def is_var_or_func_exist(content):
    """ check if variable or function exist
    """
    if not isinstance(content, basestring):
        return False

    try:
        match_start_position = content.index("$", 0)
    except ValueError:
        return False

    while match_start_position < len(content):
        dollar_match = dolloar_regex_compile.match(content, match_start_position)
        if dollar_match:
            match_start_position = dollar_match.end()
            continue

        func_match = function_regex_compile.match(content, match_start_position)
        if func_match:
            return True

        var_match = variable_regex_compile.match(content, match_start_position)
        if var_match:
            return True

        return False


def regex_findall_functions(content):
    """ extract all functions from string content, which are in format ${fun()}

    Args:
        content (str): string content

    Returns:
        list: functions list extracted from string content

    Examples:
        regex_findall_functions("${func(5)}")
        ["func(5)"]

        regex_findall_functions("${func(a=1, b=2)}")
        ["func(a=1, b=2)"]

        regex_findall_functions("/api/1000?_t=${get_timestamp()}")
        ["get_timestamp()"]

        regex_findall_functions("/api/${add(1, 2)}")
        ["add(1, 2)"]

        regex_findall_functions("/api/${add(1, 2)}?_t=${get_timestamp()}")
        ["add(1, 2)", "get_timestamp()"]

    """
    try:
        return function_regex_compile.findall(content)
    except TypeError:
        return []



def get_uniform_comparator(comparator):
    """ convert comparator alias to uniform name
    """
    if comparator in ["eq", "equals", "==", "is"]:
        return "equals"
    elif comparator in ["lt", "less_than"]:
        return "less_than"
    elif comparator in ["le", "less_than_or_equals"]:
        return "less_than_or_equals"
    elif comparator in ["gt", "greater_than"]:
        return "greater_than"
    elif comparator in ["ge", "greater_than_or_equals"]:
        return "greater_than_or_equals"
    elif comparator in ["ne", "not_equals"]:
        return "not_equals"
    elif comparator in ["str_eq", "string_equals"]:
        return "string_equals"
    elif comparator in ["len_eq", "length_equals", "count_eq"]:
        return "length_equals"
    elif comparator in ["len_gt", "count_gt", "length_greater_than", "count_greater_than"]:
        return "length_greater_than"
    elif comparator in ["len_ge", "count_ge", "length_greater_than_or_equals",
                        "count_greater_than_or_equals"]:
        return "length_greater_than_or_equals"
    elif comparator in ["len_lt", "count_lt", "length_less_than", "count_less_than"]:
        return "length_less_than"
    elif comparator in ["len_le", "count_le", "length_less_than_or_equals",
                        "count_less_than_or_equals"]:
        return "length_less_than_or_equals"
    else:
        return comparator




###############################################################################
##  parse content with variables and functions mapping
###############################################################################



def load_module_functions(module):
    """ load python module functions.

    Args:
        module: python module

    Returns:
        dict: functions mapping for specified python module

            {
                "func1_name": func1,
                "func2_name": func2
            }

    """
    module_functions = {}

    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item

    return module_functions


def load_builtin_functions():
    """ load builtin module functions
    """
    return load_module_functions(builtin)

def get_mapping_function(function_name, functions_mapping):
    """ get function from functions_mapping,
        if not found, then try to check if builtin function.

    Args:
        function_name (str): function name
        functions_mapping (dict): functions mapping

    Returns:
        mapping function object.

    Raises:
        exceptions.FunctionNotFound: function is neither defined in debugtalk.py nor builtin.

    """
    if function_name in functions_mapping:
        return functions_mapping[function_name]

    # elif function_name in ["parameterize", "P"]:
    #     return loader.load_csv_file
    #
    # elif function_name in ["environ", "ENV"]:
    #     return utils.get_os_environ
    #
    # elif function_name in ["multipart_encoder", "multipart_content_type"]:
    #     # extension for upload test
    #     from httprunner.ext import uploader
    #     return getattr(uploader, function_name)

    try:
        # check if HttpRunner builtin functions
        built_in_functions = load_builtin_functions()
        return built_in_functions[function_name]
    except KeyError:
        pass

    try:
        # check if Python builtin functions
        return getattr(builtins, function_name)
    except AttributeError:
        pass

    #raise exceptions.FunctionNotFound("{} is not found.".format(function_name))


def parse_function_params(params):
    """ parse function params to args and kwargs.

    Args:
        params (str): function param in string

    Returns:
        dict: function meta dict

            {
                "args": [],
                "kwargs": {}
            }

    Examples:
        >>> parse_function_params("")
        {'args': [], 'kwargs': {}}

        >>> parse_function_params("5")
        {'args': [5], 'kwargs': {}}

        >>> parse_function_params("1, 2")
        {'args': [1, 2], 'kwargs': {}}

        parse_function_params("a=1, b=2")
        {'args': [], 'kwargs': {'a': 1, 'b': 2}}

        parse_function_params("1, 2, a=3, b=4")
        {'args': [1, 2], 'kwargs': {'a':3, 'b':4}}

    """
    function_meta = {
        "args": [],
        "kwargs": {}
    }

    params_str = params.strip()
    if params_str == "":
        return function_meta

    args_list = params_str.split(',')
    for arg in args_list:
        arg = arg.strip()
        if '=' in arg:
            key, value = arg.split('=')
            function_meta["kwargs"][key.strip()] = parse_string_value(value.strip())
        else:
            function_meta["args"].append(parse_string_value(arg))

    return function_meta


class LazyFunction(object):
    """ call function lazily.
    """

    def __init__(self, function_meta, functions_mapping=None, check_variables_set=None):
        """ init LazyFunction object with function_meta

        Args:
            function_meta (dict): function name, args and kwargs.
                {
                    "func_name": "func",
                    "args": [1, 2]
                    "kwargs": {"a": 3, "b": 4}
                }

        """
        self.functions_mapping = functions_mapping or {}
        self.check_variables_set = check_variables_set or set()
        self.cache_key = None
        self.__parse(function_meta)

    def __parse(self, function_meta):
        """ init func as lazy functon instance

        Args:
            function_meta (dict): function meta including name, args and kwargs
        """
        self._func = get_mapping_function(
            function_meta["func_name"],
            self.functions_mapping
        )
        self.func_name = self._func.__name__
        self._args = prepare_lazy_data(
            function_meta.get("args", []),
            self.functions_mapping,
            self.check_variables_set
        )
        self._kwargs = prepare_lazy_data(
            function_meta.get("kwargs", {}),
            self.functions_mapping,
            self.check_variables_set
        )

        # if self.func_name == "load_csv_file":
        #     if len(self._args) != 1 or self._kwargs:
        #         raise exceptions.ParamsError("P() should only pass in one argument!")
        #     self._args = [self._args[0]]
        # elif self.func_name == "get_os_environ":
        #     if len(self._args) != 1 or self._kwargs:
        #         raise exceptions.ParamsError("ENV() should only pass in one argument!")
        #     self._args = [self._args[0]]

    def get_args(self):
        return self._args

    def update_args(self, args):
        self._args = args

    def __repr__(self):
        args_string = ""

        if self._args:
            str_args = [str(arg) for arg in self._args]
            args_string += ", ".join(str_args)

        if self._kwargs:
            args_string += ", "
            str_kwargs = [
                "{}={}".format(key, str(value))
                for key, value in self._kwargs.items()
            ]
            args_string += ", ".join(str_kwargs)

        return "LazyFunction({}({}))".format(self.func_name, args_string)

    def __prepare_cache_key(self, args, kwargs):
        return self.func_name, repr(args), repr(kwargs)

    def to_value(self, variables_mapping=None):
        """ parse lazy data with evaluated variables mapping.
            Notice: variables_mapping should not contain any variable or function.
        """
        variables_mapping = variables_mapping or {}
        args = parse_lazy_data(self._args, variables_mapping)
        kwargs = parse_lazy_data(self._kwargs, variables_mapping)
        self.cache_key = self.__prepare_cache_key(args, kwargs)
        return self._func(*args, **kwargs)


cached_functions_mapping = {}
""" cached function calling results.
"""


class LazyString(object):
    """ evaluate string lazily.
    """

    def __init__(self, raw_string, functions_mapping=None, check_variables_set=None, cached=False):
        """ make raw_string as lazy object with functions_mapping
            check if any variable undefined in check_variables_set
        """
        self.raw_string = raw_string
        self.functions_mapping = functions_mapping or {}
        self.check_variables_set = check_variables_set or set()
        self.cached = cached
        self.__parse(raw_string)

    def __parse(self, raw_string):
        """ parse raw string, replace function and variable with {}

        Args:
            raw_string(str): string with functions or varialbes
            e.g. "ABC${func2($a, $b)}DE$c"

        Returns:
            string: "ABC{}DE{}"
            args: ["${func2($a, $b)}", "$c"]

        """
        self._args = []

        def escape_braces(origin_string):
            return origin_string.replace("{", "{{").replace("}", "}}")

        try:
            match_start_position = raw_string.index("$", 0)
            begin_string = raw_string[0:match_start_position]
            self._string = escape_braces(begin_string)
        except ValueError:
            self._string = escape_braces(raw_string)
            return

        while match_start_position < len(raw_string):

            # Notice: notation priority
            # $$ > ${func($a, $b)} > $var

            # search $$
            dollar_match = dolloar_regex_compile.match(raw_string, match_start_position)
            if dollar_match:
                match_start_position = dollar_match.end()
                self._string += "$"
                continue

            # search function like ${func($a, $b)}
            func_match = function_regex_compile.match(raw_string, match_start_position)
            if func_match:
                function_meta = {
                    "func_name": func_match.group(1)
                }
                function_meta.update(parse_function_params(func_match.group(2)))
                lazy_func = LazyFunction(
                    function_meta,
                    self.functions_mapping,
                    self.check_variables_set
                )
                self._args.append(lazy_func)
                match_start_position = func_match.end()
                self._string += "{}"
                continue

            # search variable like ${var} or $var
            var_match = variable_regex_compile.match(raw_string, match_start_position)
            if var_match:
                var_name = var_match.group(1) or var_match.group(2)
                # check if any variable undefined in check_variables_set
                # if var_name not in self.check_variables_set:
                #     raise exceptions.VariableNotFound(var_name)

                self._args.append(var_name)
                match_start_position = var_match.end()
                self._string += "{}"
                continue

            curr_position = match_start_position
            try:
                # find next $ location
                match_start_position = raw_string.index("$", curr_position + 1)
                remain_string = raw_string[curr_position:match_start_position]
            except ValueError:
                remain_string = raw_string[curr_position:]
                # break while loop
                match_start_position = len(raw_string)

            self._string += escape_braces(remain_string)

    def __repr__(self):
        return "LazyString({})".format(self.raw_string)

    def to_value(self, variables_mapping=None):
        """ parse lazy data with evaluated variables mapping.
            Notice: variables_mapping should not contain any variable or function.
        """
        variables_mapping = variables_mapping or {}

        args = []
        for arg in self._args:
            if isinstance(arg, LazyFunction):
                if self.cached and arg.cache_key and arg.cache_key in cached_functions_mapping:
                    value = cached_functions_mapping[arg.cache_key]
                else:
                    value = arg.to_value(variables_mapping)
                    cached_functions_mapping[arg.cache_key] = value
                args.append(value)
            # else:
            #     # variable
            #     var_value = get_mapping_variable(arg, variables_mapping)
            #     args.append(var_value)

        if self._string == "{}":
            return args[0]
        else:
            return self._string.format(*args)


def prepare_lazy_data(content, functions_mapping=None, check_variables_set=None, cached=False):
    """ make string in content as lazy object with functions_mapping

    Raises:
        exceptions.VariableNotFound: if any variable undefined in check_variables_set

    """
    # TODO: refactor type check
    if content is None or isinstance(content, (numeric_types, bool, type)):
        return content

    elif isinstance(content, (list, set, tuple)):
        return [
            prepare_lazy_data(
                item,
                functions_mapping,
                check_variables_set,
                cached
            )
            for item in content
        ]

    elif isinstance(content, dict):
        parsed_content = {}
        for key, value in content.items():
            parsed_key = prepare_lazy_data(
                key,
                functions_mapping,
                check_variables_set,
                cached
            )
            parsed_value = prepare_lazy_data(
                value,
                functions_mapping,
                check_variables_set,
                cached
            )
            parsed_content[parsed_key] = parsed_value

        return parsed_content

    elif isinstance(content, basestring):
        # content is in string format here
        if not is_var_or_func_exist(content):
            # content is neither variable nor function
            # replace $$ notation with $ and consider it as normal char.
            # e.g. abc => abc, abc$$def => abc$def, abc$$$$def$$h => abc$$def$h
            return content.replace("$$", "$")

        functions_mapping = functions_mapping or {}
        check_variables_set = check_variables_set or set()
        content = LazyString(content, functions_mapping, check_variables_set, cached)

    return content

def ensure_mapping_format(variables):
    """ ensure variables are in mapping format.

    Args:
        variables (list/dict): original variables

    Returns:
        dict: ensured variables in dict format

    Examples:
        variables = [
                {"a": 1},
                {"b": 2}
            ]
        print(ensure_mapping_format(variables))
            {
                "a": 1,
                "b": 2
            }

    """
    if isinstance(variables, list):
        variables_dict = {}
        for map_dict in variables:
            variables_dict.update(map_dict)

        return variables_dict

    elif isinstance(variables, dict):
        return variables

    # else:
    #     raise exceptions.ParamsError("variables format error!")

def parse_lazy_data(content, variables_mapping=None):
    """ parse lazy data with evaluated variables mapping.
        Notice: variables_mapping should not contain any variable or function.
    """
    # TODO: refactor type check
    if content is None or isinstance(content, (numeric_types, bool, type)):
        return content

    elif isinstance(content, LazyString):
        variables_mapping = ensure_mapping_format(variables_mapping or {})
        return content.to_value(variables_mapping)

    elif isinstance(content, (list, set, tuple)):
        return [
            parse_lazy_data(item, variables_mapping)
            for item in content
        ]

    elif isinstance(content, dict):
        parsed_content = {}
        for key, value in content.items():
            parsed_key = parse_lazy_data(key, variables_mapping)
            parsed_value = parse_lazy_data(value, variables_mapping)
            parsed_content[parsed_key] = parsed_value

        return parsed_content

    return content


def eval_lazy_data(content, variables_mapping=None, functions_mapping=None):
    """ evaluate data instantly.
        Notice: variables_mapping should not contain any variable or function.
    """
    variables_mapping = variables_mapping or {}
    check_variables_set = set(variables_mapping.keys())
    return parse_lazy_data(
        prepare_lazy_data(
            content,
            functions_mapping,
            check_variables_set
        ),
        variables_mapping
    )







if __name__ == '__main__':
    a = eval_lazy_data('${add(6,5,4)}')
    print(a)
