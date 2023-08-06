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


def apply_task_number(depend_id: str, task_id: StepTaskId) -> str:
    """ Replace ``$`` references in dependency strings with their value from the `task_id` parameter,
    e.g. ``$0`` in `depend_id` will be replaced with ``task_id.task_number[0]``

    Special value ``$@`` will be replaced with the full task number.

    Raises :py:exc:`~momotor.bundles.exception.InvalidDependencies` if `depend_id` contains invalid
    references.

    Examples:

    >>> tid = StepTaskId('step', (1, 2, 3))
    >>> apply_task_number('test', tid)
    'test'

    >>> apply_task_number('test.$0', tid)
    'test.1'

    >>> apply_task_number('test.$0.$1', tid)
    'test.1.2'

    >>> apply_task_number('test.$1.$2', tid)
    'test.2.3'

    >>> apply_task_number('test.$@', tid)
    'test.1.2.3'

    >>> apply_task_number('test.$X', tid)
    Traceback (most recent call last):
    ...
    momotor.bundles.exception.InvalidDependencies: Task 'step.1.2.3' has invalid dependency 'test.$X'

    >>> apply_task_number('test.$9', tid)
    Traceback (most recent call last):
    ...
    momotor.bundles.exception.InvalidDependencies: Task 'step.1.2.3' has invalid dependency 'test.$9'

    """
    if '.$' in depend_id:
        task_number = task_id.task_number

        def _replace(part):
            if part == '@':
                return task_id_from_number(task_number)
            else:
                return str(task_number[int(part)])

        try:
            return '.'.join(
                _replace(part[1:]) if part.startswith('$') else part
                for part in depend_id.split('.')
            )
        except (ValueError, IndexError, TypeError):
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


def _get_full_deps(
            step_dep_info: typing.Mapping[str, typing.Tuple[typing.Sequence[str], typing.Optional[StepTasksType]]]
        ) -> typing.Dict[StepTaskId, typing.FrozenSet[StepTaskId]]:

    # collect all step and task ids
    step_ids: typing.FrozenSet[str] = frozenset(step_dep_info.keys())  # all step ids
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
                depend_id_str = apply_task_number(depend_id_str, task_id)
                if depend_id_str in task_ids_str:
                    dep_id = task_ids_str[depend_id_str]
                    task_dependencies.append(dep_id)
                    step_dependencies.append(dep_id)
                elif depend_id_str in step_ids:
                    dep_ids = step_task_ids.get(depend_id_str)
                    task_dependencies.extend(dep_ids)
                    step_dependencies.extend(dep_ids)
                else:
                    raise InvalidDependencies(
                        f"Task {task_id!r} depends on non-existent tasks {depend_id_str!r}"
                    )

            dependencies[task_id] = frozenset(task_dependencies)

        dependencies[StepTaskId(step_id, None)] = frozenset(step_dependencies)

    # collect the full and reverse dependencies
    #  full dependencies include the dependencies of all dependencies
    full_deps = {}

    def _collect(tid: StepTaskId, previous: typing.FrozenSet[StepTaskId]) -> typing.FrozenSet[StepTaskId]:
        if tid in full_deps:
            return full_deps[tid]

        previous = previous | {tid}
        task_deps = set(dependencies[tid])
        for full_dep_id in dependencies[tid]:
            if full_dep_id in previous:
                raise CircularDependencies("Recipe contains circular reference in task dependencies")

            task_deps |= _collect(full_dep_id, previous)

        return frozenset(task_deps)

    for task_id in task_ids:
        full_deps[task_id] = _collect(task_id, frozenset())

    return full_deps


def _get_direct_deps(
    task_id: StepTaskId,
    step_dep_info: typing.Mapping[str, typing.Tuple[typing.Sequence[str], typing.Optional[StepTasksType]]]
) -> typing.FrozenSet[StepTaskId]:

    # collect all step and task ids
    step_ids: typing.FrozenSet[str] = frozenset(step_dep_info.keys())  # all step ids
    step_task_ids: typing.Dict[str, typing.FrozenSet[StepTaskId]] = {}  # task ids for each step
    task_ids = deque()  # all task ids
    for step_id, (step_deps, tasks) in step_dep_info.items():
        ids = list(iter_task_ids(step_id, tasks))
        step_task_ids[step_id] = frozenset(ids)
        task_ids.extend(ids)

    task_ids_str: typing.Dict[str, StepTaskId] = get_task_id_lookup(task_ids)

    task_dependencies = deque()
    for depend_id_str in step_dep_info[task_id.step_id][0]:
        depend_id_str = apply_task_number(depend_id_str, task_id)
        if depend_id_str in task_ids_str:
            task_dependencies.append(task_ids_str[depend_id_str])
        elif depend_id_str in step_ids:
            task_dependencies.extend(step_task_ids.get(depend_id_str))
        else:
            raise InvalidDependencies(
                f"Task {task_id!r} depends on non-existent tasks {depend_id_str!r}"
            )

    return frozenset(task_dependencies)


def get_full_task_dependencies(recipe: RecipeBundle, config: typing.Optional[ConfigBundle]) \
        -> typing.Dict[StepTaskId, typing.FrozenSet[StepTaskId]]:
    """ Generate the full dependency tree for all steps in the recipe.
    For each task, it lists the all tasks that it depends on, including dependencies of dependencies

    :param recipe: the recipe containing the steps
    :param config: (optionally) the config containing step options
    :return: the tasks to tasks mapping. the ordering is guaranteed to be same as the order of the steps in the recipe
    """

    return _get_full_deps(_extract_deps(recipe, config))


def reverse_task_dependencies(dependencies: typing.Dict[StepTaskId, typing.Iterable[StepTaskId]]) \
        -> typing.Dict[StepTaskId, typing.FrozenSet[StepTaskId]]:
    """ Reverses the dependency tree generated by
    :py:func:`~momotor.bundles.utils.dependencies.get_task_dependencies`,
    i.e. it lists for each step which other steps depend on it.

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
        rdep_id: frozenset(deps)
        for rdep_id, deps in rdeps.items()
    }


def get_task_dependencies(recipe: RecipeBundle, config: typing.Optional[ConfigBundle], task_id: StepTaskId) \
        -> typing.FrozenSet[StepTaskId]:
    """ Get direct dependencies for a single task

    :param recipe: the recipe containing the steps
    :param config: (optionally) the config containing step options
    :param task_id: the task to generate the dependencies of
    :return: the dependencies
    """

    return _get_direct_deps(task_id, _extract_deps(recipe, config))
