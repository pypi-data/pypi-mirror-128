```sh
pip install args_to_db
```

## Data Generation Tool for Argument Optimisation

<span style="color:#4078c0">args_to_db</span> is an attempt to generalize and simplify the process of running a programm in different modes or configurations and combining the resulting datasets to allow for further analysis.

The functionality is separated into three different (independently usable) parts:

### Command Construction
Given a programm/script which is highly dependent on parameters and arguments, which we want to run for swarm of different settings, yielding datasets for further analysis.

Argument construction is made easy with the interfaces `cmd, option, flag` which are the intended way of constructing `Command` and `CommandList` objects.

```python
from args_to_db import cmd, flag, option

py = cmd('python')
# > py=[['python']]

script = cmd('script.py')
# > py=[['script.py']]

data = option('--input', ['file1.csv', 'file2.csv'])
# > data=[['--input', 'file1.csv'],
#         ['--input', 'file2.csv']]

opt_flags = flag('-O') + flag('-r')
# > opt_flags=[[],
#              ['-r'],
#              ['-O'],
#              ['-O', '-r']]

log_flag = flag('--log', vary=False)
# > log_flag=[['--log']]

cmds = py + script + data + opt_flags + log_flag
# > cmds=[['python', 'script.py', '--input', 'file1.csv', '--log'],
#         ['python', 'script.py', '--input', 'file1.csv', '-r', '--log'],
#         ['python', 'script.py', '--input', 'file1.csv', '-O', '--log'],
#         ['python', 'script.py', '--input', 'file1.csv', '-O', '-r', '--log'],
#         ['python', 'script.py', '--input', 'file2.csv', '--log'],
#         ['python', 'script.py', '--input', 'file2.csv', '-r', '--log'],
#         ['python', 'script.py', '--input', 'file2.csv', '-O', '--log'],
#         ['python', 'script.py', '--input', 'file2.csv', '-O', '-r', '--log']]
```

The `CommandList` objects are arrays of commands (which themselves are arrays again), they behave like normal python arrays except for the differnt usage of the `+` and `+=` operators.

### Command Execution
A given `CommandList` object may then be executed with `run`, providing the user with a live interface in the terminal of execution states and parallelisation control of the execution.
```python
run(cmds, threads=4)
# runs all specified commands with up to 4 concurrent threads.
```

### Data Collection
Data may be produced by the programm/script independently of being called with <span style="color:#4078c0">args_to_db</span>, which is therefore completely optional.
But functionality is provided to make data collection and combination straight forward and as easy as possible for fast results.

```python
args = argparse.ArgumentParser().parse_args()
config = config_from_args(args, __file__)
write_results(config, {'solver_solve_time': solve_time})
```

This produces an output which is then later on combined with the others by the `run` task - note the native support of `argparse` objects which are often used for argument/parameter parsing.
