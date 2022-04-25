# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

from ortools.sat.python import cp_model

import sequential.seq2pat as sp


def _print_vars(str, solver: cp_model.CpSolver, vars):
    print(str, end=" ")
    for x in vars:
        print(solver.Value(x), end=" ")
    print()


def _add_lex_order(model, vars):
    # Sort minFirst
    size = len(vars)
    for i, x in enumerate(vars):
        if i == size - 1:
            break
        model.Add(vars[i] <= vars[i + 1])


def _add_element_ct(model: cp_model.CpModel, input_array, target_array):

    # Range
    R = range(len(target_array))

    # The domain of the index variable is from 0 to input_array-1
    index_vars = [model.NewIntVar(0, len(input_array) - 1, "index_" + str(i)) for i in R]

    # Link sequence[index_vars[i]] = pattern[i]
    for i in R:
        model.AddElement(index_vars[i], input_array, target_array[i])

    # Indexes are distinct
    model.AddAllDifferent(index_vars)

    return index_vars


def _get_indexed_vars(model: cp_model.CpModel, indices, name, attributes):
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

    # Range
    R = range(len(indices))

    # Define variables from attributes
    vars = [model.NewIntVarFromDomain(cp_model.Domain.FromValues(attributes),
                                      name + str(i)) for i in R]

    # Link attributes[index_i] = vars[i]
    for i in R:
        model.AddElement(indices[i], attributes, vars[i])

    return vars


def _add_avg_ct(model: cp_model.CpModel, indices, lb, ub, attributes):

    if lb is None and ub is None:
        return []

    size = len(indices)

    # Average variables
    vars = _get_indexed_vars(model, indices, "avg_", attributes)

    # Average constraint
    if lb is not None:
        model.Add(lb * size <= sum(vars))

    if ub is not None:
        model.Add(sum(vars) <= ub * size)

    return vars


def _add_gap_ct(model: cp_model.CpModel, indices, lb, ub, attributes):
    if lb is None and ub is None:
        return []

    # Range
    R = range(len(indices))

    # Gap variables
    vars = _get_indexed_vars(model, indices, "gap_", attributes)

    # Gap constraints
    for i in reversed(R):
        if i == 0:
            break

        if lb is not None:
            model.Add(lb <= vars[i] - vars[i-1])

        if ub is not None:
            model.Add(vars[i] - vars[i-1] <= ub)

    return vars


def _add_median_ct(model: cp_model.CpModel, indices, lb, ub, attributes):

    # Range
    size = len(indices)
    R = range(len(indices))

    if lb is None and ub is None:
        return [], []

    # Median variables
    vars = _get_indexed_vars(model, indices, "median_", attributes)

    # Sorted version of median variables
    sorted_vars = [model.NewIntVarFromDomain(cp_model.Domain.FromValues(attributes),
                                             "sorted_median_" + str(i)) for i in R]

    # Link median vars and sorted median vars
    sorted_index = _add_element_ct(model, vars, sorted_vars)

    # Sort vars
    _add_lex_order(model, sorted_vars)

    # Median constraint
    is_odd = size % 2 == 1
    if lb is not None:
        if is_odd:
            model.Add(lb <= sorted_vars[size//2])
        else:
            model.Add(lb * 2 <= sorted_vars[size//2] + sorted_vars[size//2 - 1])

    if ub is not None:
        if is_odd:
            model.Add(sorted_vars[size//2] <= ub)
        else:
            model.Add(sorted_vars[size//2] + sorted_vars[size//2 - 1] <= ub * 2)

    return vars, sorted_vars


def _add_span_ct(model: cp_model.CpModel, indices, lb, ub, attributes):

    if lb is None and ub is None:
        return []

    # Span variables
    vars = _get_indexed_vars(model, indices, "span_", attributes)

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


def is_satisfiable(sequence, pattern, seq_ind, constraints):

    # # Example Input for Testing. This will come from constraints
    # ####################################################
    # average_lb = 0
    # average_ub = 2
    # average_attributes = list(np.array(sequence) * 1)
    #
    # gap_lb = 0
    # gap_ub = 100
    # gap_attributes = list(np.array(sequence) * 10)
    #
    # median_lb = 0
    # median_ub = 1000
    # median_attributes = list(np.array(sequence) * 100)
    #
    # span_lb = 0
    # span_ub = 100000
    # span_attributes = list(np.array(sequence) * 1000)
    # ####################################################

    # Constraint model
    model = cp_model.CpModel()

    # Index variables point into the sequence sequence[index_i] = pattern_i
    index_vars = _add_element_ct(model, sequence, pattern)

    # Indexes are ordered
    _add_lex_order(model, index_vars)

    if constraints:
        for constraint in constraints:

            if isinstance(constraint, sp._Constraint.Average):
                average_ub = constraint.upper_bound
                average_lb = constraint.lower_bound

                attrs = constraint.attribute.values[seq_ind]

                # Average constraint
                avg_vars = _add_avg_ct(model, index_vars, average_lb, average_ub, attrs)

            if isinstance(constraint, sp._Constraint.Gap):
                gap_ub = constraint.upper_bound
                gap_lb = constraint.lower_bound

                attrs = constraint.attribute.values[seq_ind]

                # Gap constraint
                gap_vars = _add_gap_ct(model, index_vars, gap_lb, gap_ub, attrs)

            if isinstance(constraint, sp._Constraint.Median):
                median_ub = constraint.upper_bound
                median_lb = constraint.lower_bound

                attrs = constraint.attribute.values[seq_ind]

                # Median constraint
                median_vars, sorted_median_vars = _add_median_ct(model, index_vars, median_lb, median_ub, attrs)

            if isinstance(constraint, sp._Constraint.Span):
                span_ub = constraint.upper_bound
                span_lb = constraint.lower_bound

                attrs = constraint.attribute.values[seq_ind]

                # Span constraint
                span_vars = _add_span_ct(model, index_vars, span_lb, span_ub, attrs)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # print('%s found in %0.2fs' % (solver.StatusName(status), solver.WallTime()))
    # print('%s branches %s conflicts' % (solver.NumBranches(), solver.NumConflicts()))

    # If solution found
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # _print_vars("index_vars: ", solver, index_vars)
        # _print_vars("avg_vars: ", solver, avg_vars)
        # _print_vars("gap_vars: ", solver, gap_vars)
        # _print_vars("median_vars: ", solver, median_vars)
        # _print_vars("sorted_median_vars: ", solver, sorted_median_vars)
        # _print_vars("span_vars: ", solver, span_vars)
        return True
    else:
        # print('No solution found.')
        return False
