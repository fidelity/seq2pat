# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

import numpy as np
from ortools.sat.python import cp_model


def print_vars(str, solver: cp_model.CpSolver, vars):
    print(str, end=" ")
    for x in vars:
        print(solver.Value(x), end=" ")
    print()


def get_indexed_vars(model: cp_model.CpModel, indices, name, P, attributes):
    """
    Helper function to create and return variables for
    vars = attributes[indices]

    :param model:
    :param indices:
    :param name:
    :param P:
    :param attributes:
    :return:

    """
    # Define variables from attributes
    vars = [model.NewIntVarFromDomain(cp_model.Domain.FromValues(attributes),
                                      name + str(i)) for i in P]

    # Link attributes[index_i] = vars[i]
    for i in P:
        model.AddElement(indices[i], attributes, vars[i])

    return vars


def add_avg_ct(model: cp_model.CpModel, indices, P, lb, ub, attributes):

    if lb is None and ub is None:
        return []

    # Average variables
    vars = get_indexed_vars(model, indices, "avg_", P, attributes)

    len_pattern = len(P)

    # Average constraint
    if lb is not None:
        model.Add(lb * len_pattern <= sum(vars))

    if ub is not None:
        model.Add(sum(vars) <= ub * len_pattern)

    return vars


def add_gap_ct(model: cp_model.CpModel, indices, P, lb, ub, attributes):
    if lb is None and ub is None:
        return []

    # Gap variables
    vars = get_indexed_vars(model, indices, "gap_", P, attributes)

    # Gap constraints
    for i in reversed(P):
        if i == 0:
            break

        if lb is not None:
            model.Add(lb <= vars[i] - vars[i-1])

        if ub is not None:
            model.Add(vars[i] - vars[i-1] <= ub)

    return vars


def add_median_ct(model: cp_model.CpModel, indices, P, lb, ub, attributes):

    if lb is None and ub is None:
        return [], []

    # Median variables
    vars = get_indexed_vars(model, indices, "median_", P, attributes)

    # Create sorted median variables
    sorted_index = [model.NewIntVar(0, len(P)-1, "sorted_index") for i in P]
    sorted_vars = [model.NewIntVarFromDomain(cp_model.Domain.FromValues(attributes),
                                             "sorted_median_" + str(i)) for i in P]

    # Link vars[sorted_index] = sorted_vars
    for i in P:
        model.AddElement(sorted_index[i], vars, sorted_vars[i])

    # Indexes are distinct
    model.AddAllDifferent(sorted_index)

    # Sort minFirst
    len_P = len(P)
    for i in P:
        if i == len_P - 1:
            break
        model.Add(sorted_vars[i] <= sorted_vars[i + 1])

    # Median constraint
    is_odd = len_P % 2 == 1
    if lb is not None:
        if is_odd:
            model.Add(lb <= sorted_vars[len_P//2])
        else:
            model.Add(lb * 2 <= sorted_vars[len_P//2] + sorted_vars[len_P//2 - 1])

    if ub is not None:
        if is_odd:
            model.Add(sorted_vars[len_P//2] <= ub)
        else:
            model.Add(sorted_vars[len_P//2] + sorted_vars[len_P//2 - 1] <= ub * 2)

    return vars, sorted_vars


def add_span_ct(model: cp_model.CpModel, indices, P, lb, ub, attributes):

    if lb is None and ub is None:
        return []

    # Span variables
    vars = get_indexed_vars(model, indices, "span_", P, attributes)

    # Minimum, maximum variables
    min_value = int(min(attributes))
    max_value = int(max(attributes))
    min_var = model.NewIntVar(min_value, max_value, "min_span")
    max_var = model.NewIntVar(min_value, max_value, "max_span")

    # Min/max constraint
    model.AddMaxEquality(max_var, vars)
    model.AddMinEquality(min_var, vars)

    # Span variable
    span_var = model.NewIntVar(min_value, max_value, "span_var")
    model.Add(max_var - min_var == span_var)

    # Span constraint
    if lb is not None:
        model.Add(lb <= span_var)

    if ub is not None:
        model.Add(span_var <= ub)

    return vars


def is_satisfiable(sequence, pattern):

    # Example Input for Testing. This will come from constraints
    ####################################################
    average_lb = 0
    average_ub = 10000
    average_attributes = list(np.array(sequence) * 1)

    gap_lb = None
    gap_ub = None
    gap_attributes = list(np.array(sequence) * 10)

    median_lb = 0
    median_ub = 1000
    median_attributes = list(np.array(sequence) * 100)

    span_lb = 0
    span_ub = 5000
    span_attributes = list(np.array(sequence) * 1000)
    ####################################################

    # Constraint model
    model = cp_model.CpModel()

    # Constants and ranges
    len_sequence = len(sequence)
    len_pattern = len(pattern)
    P = range(len_pattern)

    # Index variables for each element in the pattern pointing into the sequence
    # The domain of the index variable is from 0 to sequence_len-1
    index_vars = [model.NewIntVar(0, len_sequence - 1, "index_" + str(i)) for i in P]

    # Indexes are distinct
    model.AddAllDifferent(index_vars)

    # Link sequence[index_vars[i]] = pattern[i]
    for i in P:
        model.AddElement(index_vars[i], sequence, pattern[i])

    # Average constraint
    avg_vars = add_avg_ct(model, index_vars, P, average_lb, average_ub, average_attributes)

    # Gap constraint
    gap_vars = add_gap_ct(model, index_vars, P, gap_lb, gap_ub, gap_attributes)

    # Median constraint
    median_vars, sorted_median_vars = add_median_ct(model, index_vars, P, median_lb, median_ub, median_attributes)

    # Span constraint
    span_vars = add_span_ct(model, index_vars, P, span_lb, span_ub, span_attributes)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    print('%s found in %0.2fs' % (solver.StatusName(status), solver.WallTime()))
    print('%s branches %s conflicts' % (solver.NumBranches(), solver.NumConflicts()))

    # If solution found
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print_vars("index_vars: ", solver, index_vars)
        print_vars("avg_vars: ", solver, avg_vars)
        print_vars("gap_vars: ", solver, gap_vars)
        print_vars("median_vars: ", solver, median_vars)
        print_vars("sorted_median_vars: ", solver, sorted_median_vars)
        print_vars("span_vars: ", solver, span_vars)
        return True
    else:
        print('No solution found.')
        return False


is_satisfiable([2, 1, 3, 4], [2, 1, 3])