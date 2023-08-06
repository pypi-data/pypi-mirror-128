from dataclasses import dataclass
from textwrap import dedent

import itertools
import re
import typing

from momotor.bundles import RecipeBundle, ConfigBundle, BundleFormatError
from momotor.bundles.utils.option import OptionProviders, OptionDefinition, OptionNameDomain

__all__ = [
    'StepTasksType', 'StepTaskNumberType', 'StepTaskId',
    'task_number_from_id', 'task_id_from_number',
    'step_tasks_option',
    'get_step_tasks_option', 'STEP_TASKS_OPTION_NAME',
    'iter_task_numbers', 'iter_task_ids', 'get_task_id_lookup'
]

STEP_TASKS_OPTION_NAME = OptionNameDomain('tasks', 'step')

step_tasks_option = OptionDefinition(
    name=STEP_TASKS_OPTION_NAME.name,
    domain=STEP_TASKS_OPTION_NAME.domain,
    type='str',
    doc=dedent("""\
        Enable multiple tasks for this step. If not provided, a single task is generated for this step.
        
        This option can directly define the number of tasks, but the actual number of tasks can also be defined
        in the top-level options of the recipe or the options of the configuration bundle.
        
        The following table describes the various values that are valid for this option:
        
        ============ ============================
        Tasks option Recipe/config option allowed
        ============ ============================
        ``*``        Any dimensions allowed (e.g. ``2``, ``2.2`` etc)
        ``?``        A single dimension required (e.g. ``1``, ``2``)
        ``?.?``      Two dimensions required (e.g. ``1.1``, ``2.2``)
        ``?.?.?``    Three dimensions required (e.g. ``1.2.3``, ``2.2.2``)
        ``?.*``      At least two dimensions required (e.g. ``1.2``, ``1.2.3``)
        ``4.?``      Exactly two dimensions required, and the first must be ``4`` (e.g. ``4.1``, ``4.2``)
        ``4.*``      At least two dimensions required, and the first must be ``4`` (e.g. ``4.1``, ``4.2.3``)
        ``4.4``      A fixed dimension. Config option not required, but if provided, MUST equal ``4.4``
        ============ ============================
    
        There is no limit to the number of dimensions allowed.
    """),
    location=('config', 'recipe', 'step')
)


StepTasksType = typing.Tuple[int, ...]
StepTaskNumberType = typing.Optional[typing.Tuple[int, ...]]


def task_id_from_number(task_number: typing.Optional[typing.Iterable[int]]) -> str:
    return '.'.join(str(t) for t in task_number) if task_number else ''


def task_number_from_id(task_id: typing.Optional[str]) -> StepTaskNumberType:
    return tuple(int(p) for p in task_id.split('.')) if task_id else None


@dataclass(frozen=True)
class StepTaskId:
    """ A step-id and task-number pair
    """
    step_id: str
    task_number: StepTaskNumberType

    def __str__(self):
        if self.task_number:
            return self.step_id + '.' + task_id_from_number(self.task_number)
        else:
            return self.step_id


# Validator for the definition option in the <step> node
TASKS_DEF_RE = re.compile(r'^((([1-9]\d*)|[?])\.)*(([1-9]\d*)|[?*])$')


def get_step_tasks_option(recipe: RecipeBundle, config: typing.Optional[ConfigBundle], step_id: str) \
        -> typing.Optional[StepTasksType]:
    """ Get the 'tasks' option for a single step

    This gets the value of the 'tasks' option in the 'step' domain from the step, recipe or config.

    A step supporting sub-tasks must define the option in the recipe. The option definition in the recipe declares
    what is supported. The format for the definition is as follows:

    ============ ============================
    Tasks option Recipe/config option allowed
    ============ ============================
    ``*``        Any dimensions allowed (e.g. ``2``, ``2.2`` etc)
    ``?``        A single dimension required (e.g. ``1``, ``2``)
    ``?.?``      Two dimensions required (e.g. ``1.1``, ``2.2``)
    ``?.?.?``    Three dimensions required (e.g. ``1.2.3``, ``2.2.2``)
    ``?.*``      At least two dimensions required (e.g. ``1.2``, ``1.2.3``)
    ``4.?``      Exactly two dimensions required, and the first must be ``4`` (e.g. ``4.1``, ``4.2``)
    ``4.*``      At least two dimensions required, and the first must be ``4`` (e.g. ``4.1``, ``4.2.3``)
    ``4.4``      A fixed dimension. Config option not required, but if provided, MUST equal ``4.4``
    ============ ============================

    There is no limit to the number of dimensions allowed.

    Values in the config take priority over values in the recipe. If the option in the recipe contains dimension
    placeholders ``?`` or ``*``, the option in the config must fill in those values.

    :param recipe: the recipe bundle
    :param config: (optional) the config bundle
    :param step_id: the id of the step
    :return: the tasks option, parsed into a tuple of ints
    """
    step = recipe.steps[step_id]
    value_def = step_tasks_option.resolve(
        OptionProviders(step=step)
    )

    value = step_tasks_option.resolve(
        OptionProviders(recipe=recipe, config=config),
        {'recipe': step_id, 'config': step_id}
    )

    if value_def is None:
        if value is None:
            return None
        else:
            raise BundleFormatError(f"Step {step_id!r}: {STEP_TASKS_OPTION_NAME} option not supported")

    if not TASKS_DEF_RE.match(value_def):
        raise BundleFormatError(f"Step {step_id!r}: invalid {STEP_TASKS_OPTION_NAME} option"
                                f" definition {value_def!r}")

    value_def_parts = value_def.split('.')
    if value_def_parts[-1] == '*':
        wildcard = True
        value_def_parts.pop()
    else:
        wildcard = False

    if not wildcard and '?' not in value_def_parts:
        # Fixed dimension -- value is optional but must be equal to value_def if provided
        if value and value != value_def:
            raise BundleFormatError(f"Step {step_id!r}: {STEP_TASKS_OPTION_NAME} option value {value!r} "
                                    f"does not match definition {value_def!r}")

        return task_number_from_id(value_def)

    elif not value:
        # Missing value option
        raise BundleFormatError(f"Step {step_id!r}: missing required {STEP_TASKS_OPTION_NAME} option")

    else:
        step_tasks = []
        try:
            for pos, part in enumerate(value.split('.')):
                try:
                    part_def = value_def_parts[pos]
                except IndexError:
                    if not wildcard:
                        raise ValueError
                    part_def = '?'

                if part_def not in {'?', part}:
                    raise ValueError

                step_tasks.append(int(part))

        except ValueError:
            raise BundleFormatError(f"Step {step_id!r}: {STEP_TASKS_OPTION_NAME} option value {value!r} "
                                    f"does not match definition {value_def!r}")

        return tuple(step_tasks)


def iter_task_numbers(sub_tasks: StepTasksType) -> typing.Generator[StepTaskNumberType, None, None]:
    """ Generate all the task-numbers for the subtasks.

    >>> list(iter_task_numbers(tuple()))
    [None]

    >>> list(iter_task_numbers((1,)))
    [(0,)]

    >>> list(iter_task_numbers((3,)))
    [(0,), (1,), (2,)]

    >>> list(iter_task_numbers((2, 2)))
    [(0, 0), (0, 1), (1, 0), (1, 1)]

    >>> list(iter_task_numbers((2, 3)))
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]

    :param sub_tasks: sequence of integers with the number of sub-tasks for each level
    :return: the task numbers
    """
    if sub_tasks:
        yield from itertools.product(*(range(st) for st in sub_tasks))
    else:
        yield None


def iter_task_ids(step_id: str, sub_tasks: StepTasksType) -> typing.Generator[StepTaskId, None, None]:
    """ Generate all the task-ids for the subtasks.

    >>> list(str(t) for t in iter_task_ids('step', tuple()))
    ['step']

    >>> list(str(t) for t in iter_task_ids('step', (2,)))
    ['step.0', 'step.1']

    >>> list(str(t) for t in iter_task_ids('step', (2, 2)))
    ['step.0.0', 'step.0.1', 'step.1.0', 'step.1.1']

    :param step_id: the id of the step
    :param sub_tasks: sequence of integers with the number of sub-tasks for each level
    :return: the task numbers
    """
    for task_number in iter_task_numbers(sub_tasks):
        yield StepTaskId(step_id, task_number)


def get_task_id_lookup(task_ids: typing.Iterable[StepTaskId]) -> typing.Dict[str, StepTaskId]:
    """ Convert an iterable of :py:const:`StepTaskId` objects into a lookup table to convert a string representation of
    a task-id to the :py:const:`StepTaskId`

    >>> get_task_id_lookup({StepTaskId('step', (0, 0))})
    {'step.0.0': StepTaskId(step_id='step', task_number=(0, 0))}

    :param task_ids: the task ids to convert
    :return: the lookup table
    """
    return {
        str(task_id): task_id
        for task_id in task_ids
    }
