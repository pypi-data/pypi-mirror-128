"""Provides functions for working with intervals.

Note: this is analogous to "domain" in Grasshopper which refers to
the term's meaning in relation to topological space,
not necessarily the domain of a function.
"""

def value_in_interval(param, interval, param_interval=(0, 1)):
  value = scale_list([param], param_interval, interval)[0]
  return value


def scale_list(input_list, source, target):
  """Scale values in input_list with source range to match target range."""
  
  output_list = []

  for n in input_list:
    shift = n - min(source)
    src_range = max(source) - min(source)
    target_range = max(target) - min(target)
    transformed = (shift / src_range) * target_range + min(target)
    output_list.append(transformed)

  return output_list


def consecutive_intervals(target, pattern, symmetrical=False, absolute=False):
  """Returns consecutive value pairs representing U or V spans.

  Pattern is a list of spans, either in absolute units or 
  to be proportionally allocated across the target interval.
  If the symmetrical flag is True, the input pattern will be mirrored.
  """

  if symmetrical:
    pattern_reversed = list(reversed(pattern))
    pattern = pattern + pattern_reversed

  result = []
  acc = target[0]

  for i, p in enumerate(pattern):

    if absolute:
      subspan = p
    else:
      span = interval_length(target)
      pattern_total = sum(pattern)
      subspan = span * (p / pattern_total)

    interval = (acc, acc + subspan)
    result.append(interval)
    acc += subspan

  return result


def interval_from_list(input_list, zero=False):
  l_min = min(input_list)
  l_max = max(input_list)
  
  if zero: result = (0, l_max)
  else: result = (l_min, l_max)
  
  return result


def interval_length(interval):
  return max(interval) - min(interval)


def reparameterize_list(input_list, target=(0, 1)):
  """Reparameterize values in input_list"""
  
  list_total = sum(input_list)
  result = [v / list_total for v in input_list]
  result = scale_list(result, (0, 1), target)
  
  return result
