import operator
from collections import deque

import re
import typing

from momotor.bundles import RecipeBundle, ConfigBundle
from momotor.bundles.exception import CircularDependencies, InvalidDependencies
from momotor.bundles.utils.tasks import get_step_tasks_option, iter_task_numbers, \
    iter_task_ids, StepTaskId, get_task_id_lookup, StepTasksType, task_id_from_number

__all__ = [
    'apply_task_number', 'make_result_id_re',
    'get_full_task_dependencies', 'reverse_task_dependencies', 'get_task_dependencies'
]


TASK_OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
    '%': operator.mod,
}
TASK_OPER_RE = re.compile(
    rf'({"|".join(re.escape(oper) for oper in TASK_OPERATORS.keys())})'
)


def apply_task_number(depend_id: str, task_id: StepTaskId) -> str:
    """ Replace ``$`` references in dependency strings with their value from the `task_id` parameter,
    e.g. ``$0`` in `depend_id` will be replaced with ``task_id.task_number[0]``

    Simple arithmetic on the values can be done, available operators are ``+``, ``-``, ``*``, ``/`` and ``%``, for
    the usual operations `add`, `subtract`, `multiply`, `integer division` and `modulo`.
    Arithmetic operations are evaluated from left to right, there is no operator precedence.

    When subtraction results in a negative value or division in infinity, this will not directly throw an exception,
    but instead will generate an invalid task-id containing ``#NEG`` or ``#INF``.

    Special value ``$@`` will be replaced with the full task number.

    Raises :py:exc:`~momotor.bundles.exception.InvalidDependencies` if `depend_id` contains invalid
    references or is syntactically incorrect.

    Examples:

    >>> tid = StepTaskId('step', (0, 1, 2))
    >>> apply_task_number('test', tid)
    'test'

    >>> apply_task_number('test.$0', tid)
    'test.0'

    >>> apply_task_number('test.$0.$1', tid)
    'test.0.1'

    >>> apply_task_number('test.$1.$2', tid)
    'test.1.2'

    >>> apply_task_number('test.$0-1.$1-1.$2-1', tid)
    'test.#NEG.0.1'

    >>> apply_task_number('test.$0+1.$1+1.$2+1', tid)
    'test.1.2.3'

    >>> apply_task_number('test.$0*2.$1*2.$2*2', tid)
    'test.0.2.4'

    >>> apply_task_number('test.$0/2.$1/2.$2/2', tid)
    'test.0.0.1'

    >>> apply_task_number('test.$0%2.$1%2.$2%2', tid)
    'test.0.1.0'

    >>> apply_task_number('test.$0*2+1.$1*2+1.$2*2+1', tid)
    'test.1.3.5'

    >>> apply_task_number('test.$0+1*2.$1+1*2.$2+1*2', tid)
    'test.2.4.6'

    >>> apply_task_number('test.$0+$1+$2', tid)
    'test.3'

    >>> apply_task_number('test.$1/0', tid)
    'test.#INF'

    >>> apply_task_number('test.$@', tid)
    'test.0.1.2'

    >>> apply_task_number('test.$X', tid)
    Traceback (most recent call last):
    ...
    momotor.bundles.exception.InvalidDependencies: Task 'step.0.1.2' has invalid dependency 'test.$X'

    >>> apply_task_number('test.$1$2', tid)
    Traceback (most recent call last):
    ...
    momotor.bundles.exception.InvalidDependencies: Task 'step.0.1.2' has invalid dependency 'test.$1$2'

    >>> apply_task_number('test.$1^4', tid)
    Traceback (most recent call last):
    ...
    momotor.bundles.exception.InvalidDependencies: Task 'step.0.1.2' has invalid dependency 'test.$1^4'

    >>> apply_task_number('test.$9', tid)
    Traceback (most recent call last):
    ...
    momotor.bundles.exception.InvalidDependencies: Task 'step.0.1.2' has invalid dependency 'test.$9'

    """
    if '.$' in depend_id:
        task_number = task_id.task_number
        if task_number:
            task_lookup = {
                f'${idx}': value
                for idx, value in enumerate(task_number)
            }
        else:
            task_lookup = {}

        def _replace(section):
            if section == '$@':
                # expand `$@` into the full task number string
                return task_id_from_number(task_number)
            elif section in {'*', '?'}:
                # ignore wildcards
                return section

            parts = deque(TASK_OPER_RE.split(section))

            result, oper = None, None
            try:
                while parts:
                    value = parts.popleft()
                    try:
                        value = task_lookup[value]
                    except KeyError:
                        value = int(value)

                    result = TASK_OPERATORS[oper](result, value) if oper else value

                    if parts:
                        oper = parts.popleft()

            except ZeroDivisionError:
                return '#INF'

            if result is None:
                raise ValueError

            elif result < 0:
                return '#NEG'

            return str(result)

        try:
            return '.'.join(
                _replace(part) if idx else part
                for idx, part in enumerate(depend_id.split('.'))
            )
        except (ValueError, IndexError, TypeError) as e:
            raise InvalidDependencies(
                f"Task '{task_id!s}' has invalid dependency '{depend_id!s}'"
            )

    return depend_id


def make_result_id_re(selector: str) -> "typing.re.Pattern":
    """ Make a regex that matches a result-id to the `selector`.

    Uses a glob-like pattern matching on the dot-separated elements of the selector.
    For the first element (the step-id part), a ``*`` will match zero or more characters except ``.``
    For all the other elements (the task number parts), a ``*`` matches one or more elements starting at that position
    and a ``?`` matches a single element in that position.

    Special selector ``**`` matches all step-ids and task-numbers, i.e. it produces a regex that matches anything.

    This method does *not* apply any task numbers, apply
    :py:meth:`~momotor.bundles.utils.dependencies.apply_task_number` to the selector before calling this function for
    that if needed.

    Examples:

    >>> make_result_id_re('test').match('test') is not None
    True

    >>> make_result_id_re('test').match('test.1') is not None
    False

    >>> make_result_id_re('test').match('testing') is not None
    False

    >>> make_result_id_re('test.1').match('test.2') is not None
    False

    >>> make_result_id_re('test.2').match('test.2.3') is not None
    False

    >>> make_result_id_re('test.2.3').match('test.2.3') is not None
    True

    >>> make_result_id_re('test.?').match('test.2.3') is not None
    False

    >>> make_result_id_re('test.?.?').match('test.2.3') is not None
    True

    >>> make_result_id_re('test.?.?.?').match('test.2.3') is not None
    False

    >>> make_result_id_re('test.*').match('test.2.3') is not None
    True

    >>> make_result_id_re('test.?.*').match('test.2.3') is not None
    True

    >>> make_result_id_re('test.?.?.*').match('test.2.3') is not None
    False

    >>> make_result_id_re('*').match('test') is not None
    True

    >>> make_result_id_re('*').match('test.2.3') is not None
    False

    >>> make_result_id_re('*.*').match('test.2.3') is not None
    True

    >>> make_result_id_re('test*').match('testing') is not None
    True

    >>> make_result_id_re('*sti*').match('testing') is not None
    True

    >>> make_result_id_re('*sting').match('testing') is not None
    True

    >>> make_result_id_re('te*ng').match('testing') is not None
    True

    >>> make_result_id_re('test*').match('tasting') is not None
    False

    >>> make_result_id_re('test*').match('testing.1') is not None
    False

    >>> make_result_id_re('test*.*').match('testing.1') is not None
    True

    >>> make_result_id_re('**').match('testing') is not None
    True

    >>> make_result_id_re('**').match('testing.1') is not None
    True

    :param selector: selector to match
    :return: a compiled regular expression (a :py:func:`re.compile` object) for the selector
    """
    if selector == '**':
        regex = r'^.*$'

    else:
        regex_parts = deque()

        first = True
        for selector_part in selector.split('.'):
            if first and '*' in selector_part:
                regex_part = r'[^.]*'.join(re.escape(step_id_part) for step_id_part in selector_part.split('*'))
            elif selector_part == '*':
                regex_part = r'\d+(?:\.(\d+))*'
            elif selector_part == '?':
                regex_part = r'\d+'
            else:
                regex_part = re.escape(selector_part)

            regex_parts.append(regex_part)
            first = False

        regex = r'^' + r'\.'.join(regex_parts) + r'$'

    return re.compile(regex)


def _extract_deps(recipe: RecipeBundle, config: typing.Optional[ConfigBundle]) \
        -> typing.Mapping[str, typing.Tuple[typing.Sequence[str], typing.Optional[StepTasksType]]]:
    """ Extract step dependency info from recipe and config
    """
    return {
        step_id: (
            tuple(step.get_dependencies_ids()),
            get_step_tasks_option(recipe, config, step_id)
        )
        for step_id, step in recipe.steps.items()
    }


def _collect_dependency_matches(depend_id_str: str, task_id: StepTaskId, task_ids_map: typing.Dict[str, StepTaskId]) \
        -> typing.Generator[StepTaskId, None, None]:

    applied_id = apply_task_number(depend_id_str, task_id)
    if '#' in applied_id:
        # A `#` in the applied_id indicates an arithmetic error
        # Ignoring these allows tasks to depend on a previous task, with the first task not having such
        # dependency
        return

    task_id = task_ids_map.get(applied_id)
    if task_id:
        # non-wildcard match
        yield task_id
        return

    applied_id_re = make_result_id_re(applied_id)
    exists = False
    for task_id_str, task_id in task_ids_map.items():
        if applied_id_re.fullmatch(task_id_str):
            exists = True
            yield task_id

    if not exists:
        raise InvalidDependencies(
            f"Task {task_id!r} depends on non-existent task(s) {depend_id_str!r}"
        )


def _reorder_taskids(task_ids: typing.Container[StepTaskId], ordering: typing.Iterable[StepTaskId]) \
        -> typing.Tuple[StepTaskId, ...]:

    # Convert a container of StepTaskIds into a tuple, using the order given by `ordering`
    return tuple(
        task_id
        for task_id in ordering
        if task_id in task_ids
    )


def _get_full_deps(
            step_dep_info: typing.Mapping[str, typing.Tuple[typing.Sequence[str], typing.Optional[StepTasksType]]]
        ) -> typing.Dict[StepTaskId, typing.Tuple[StepTaskId, ...]]:

    # collect all step and task ids
    # step_ids: typing.FrozenSet[str] = frozenset(step_dep_info.keys())  # all step ids
    step_task_ids: typing.Dict[str, typing.Sequence[StepTaskId]] = {}  # task ids for each step

    task_ids = deque()  # all task ids
    for step_id, (depends, tasks) in step_dep_info.items():
        ids = list(iter_task_ids(step_id, tasks))
        step_task_ids[step_id] = ids
        task_ids.extend(ids)

    task_ids_str: typing.Dict[str, StepTaskId] = get_task_id_lookup(task_ids)

    # collect all task ids and collect direct dependencies for all steps and tasks
    dependencies: typing.Dict[StepTaskId, typing.FrozenSet[StepTaskId]] = {}  # direct dependencies of each task
    for step_id, (depends, tasks) in step_dep_info.items():
        step_dependencies = deque()  # dependencies of all tasks for this step

        for task_number in iter_task_numbers(tasks):
            task_id = StepTaskId(step_id, task_number)
            task_dependencies = deque()  # dependencies of this task
            for depend_id_str in depends:
                task_dependencies.extend(
                    _collect_dependency_matches(depend_id_str, task_id, task_ids_str)
                )

            dependencies[task_id] = frozenset(task_dependencies)
            step_dependencies.extend(task_dependencies)

        dependencies[StepTaskId(step_id, None)] = frozenset(step_dependencies)

    # collect the full dependencies
    deps_cache: typing.Dict[StepTaskId, typing.Tuple[StepTaskId, ...]] = {}

    def _collect(tid: StepTaskId, previous: typing.FrozenSet[StepTaskId]) -> typing.Tuple[StepTaskId, ...]:
        if tid not in deps_cache:
            previous = previous | {tid}
            full_task_deps = set(dependencies[tid])
            for full_dep_id in dependencies[tid]:
                if full_dep_id in previous:
                    raise CircularDependencies("Recipe contains circular reference in task dependencies")

                full_task_deps.update(_collect(full_dep_id, previous))

            deps_cache[tid] = _reorder_taskids(full_task_deps, task_ids)

        return deps_cache[tid]

    return {
        task_id: _collect(task_id, frozenset())
        for task_id in task_ids
    }


def _get_direct_deps(
    task_id: StepTaskId,
    step_dep_info: typing.Mapping[str, typing.Tuple[typing.Sequence[str], typing.Optional[StepTasksType]]]
) -> typing.Tuple[StepTaskId, ...]:

    # collect all step and task ids
    # step_ids: typing.FrozenSet[str] = frozenset(step_dep_info.keys())  # all step ids
    step_task_ids: typing.Dict[str, typing.FrozenSet[StepTaskId]] = {}  # task ids for each step
    task_ids = deque()  # all task ids
    for step_id, (step_deps, tasks) in step_dep_info.items():
        ids = list(iter_task_ids(step_id, tasks))
        step_task_ids[step_id] = frozenset(ids)
        task_ids.extend(ids)

    task_ids_str: typing.Dict[str, StepTaskId] = get_task_id_lookup(task_ids)

    task_dependencies: typing.Set[StepTaskId] = set()
    for depend_id_str in step_dep_info[task_id.step_id][0]:
        task_dependencies.update(
            _collect_dependency_matches(depend_id_str, task_id, task_ids_str)
        )

    return _reorder_taskids(task_dependencies, task_ids)


def get_full_task_dependencies(recipe: RecipeBundle, config: typing.Optional[ConfigBundle]) \
        -> typing.Dict[StepTaskId, typing.Tuple[StepTaskId, ...]]:
    """ Generate the full dependency tree for all steps in the recipe.
    For each task, it lists the all tasks that it depends on, including dependencies of dependencies

    Task ordering is preserved: the tasks listed in the result, both the the dict keys and the tuple values,
    are in the same order as the definitions in the recipe.

    :param recipe: the recipe containing the steps
    :param config: (optionally) the config containing step options
    :return: the tasks to tasks mapping. the ordering is guaranteed to be same as the order of the steps in the recipe
    """

    return _get_full_deps(_extract_deps(recipe, config))


def reverse_task_dependencies(dependencies: typing.Dict[StepTaskId, typing.Iterable[StepTaskId]]) \
        -> typing.Dict[StepTaskId, typing.Tuple[StepTaskId, ...]]:
    """ Reverses the dependency tree generated by
    :py:func:`~momotor.bundles.utils.dependencies.get_task_dependencies`,
    i.e. it lists for each step which other steps depend on it.

    Task ordering is preserved: the tasks listed in the result, both the the dict keys and the tuple values,
    are in the same order as in the `dependencies` argument.

    :param dependencies: the task dependencies
    :return: the reverse dependencies
    """
    rdeps = {
        task_id: deque()
        for task_id in dependencies.keys()
    }

    for dep_id, deps in dependencies.items():
        for dep in deps:
            rdeps[dep].append(dep_id)

    return {
        rdep_id: _reorder_taskids(deps, dependencies.keys())
        for rdep_id, deps in rdeps.items()
    }


def get_task_dependencies(recipe: RecipeBundle, config: typing.Optional[ConfigBundle], task_id: StepTaskId) \
        -> typing.Tuple[StepTaskId, ...]:
    """ Get direct dependencies for a single task.

    Task ordering is preserved: the tasks listed in the result are in the same order as the definitions in the recipe.s

    :param recipe: the recipe containing the steps
    :param config: (optionally) the config containing step options
    :param task_id: the task to generate the dependencies of
    :return: the dependencies
    """

    return _get_direct_deps(task_id, _extract_deps(recipe, config))
