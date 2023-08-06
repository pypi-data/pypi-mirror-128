# Copyright 2021 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#      https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

# pylint: disable=too-many-lines
"""Module for nodes that call straight through to TensorFlow functions."""

from typing import (
    List,
    Optional,
    Tuple,
    Union,
)

import forge
import numpy as np

from qctrlcommons.exceptions import QctrlException
from qctrlcommons.node.base import Node
from qctrlcommons.node.documentation import Category
from qctrlcommons.node.node_data import Tensor
from qctrlcommons.node.utils import validate_shape
from qctrlcommons.preconditions import (
    check_argument,
    check_argument_numeric,
)


class Sum(Node):
    """
    Returns the sum of all the elements in a tensor (or a list of tensors with the same shape),
    or the sum of a tensor along one or multiple axes.

    Parameters
    ----------
    input_tensor : np.ndarray or Tensor or list[Tensor]
        The tensor whose elements you want to sum. If you pass a list of tensors, they must all have
        the same shape, and are interpreted as being stacked along a new first dimension (for
        example, if you pass two 2D tensors of shape ``[3, 4]``, the result is equivalent to passing
        the stacked 3D tensor of shape ``[2, 3, 4]``).
    axis : int or list[int] or tuple[int], optional
        The dimension or dimensions along which you want to sum the tensor. Defaults to `None`, in
        which case this node sums along all axes of the tensor.
    keepdims : bool, optional
        Whether or not to retain summed axes in the output tensor. If true, each dimension in
        `axis` has size 1 in the result; otherwise, the dimensions in `axis` are removed from the
        result. Defaults to false.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The tensor obtained by summing the input tensor along the specified axes (or, if `axis` was
        `None`, the tensor obtained by summing the input tensor along all of the specified axes).

    See Also
    --------
    einsum : Tensor contraction via Einstein summation convention.
    """

    name = "sum"
    args = [
        forge.arg(
            "input_tensor",
            type=Union[np.ndarray, Tensor, List[Tensor]],
        ),
        forge.arg(
            "axis",
            type=Optional[Union[List[int], Tuple[int, ...]]],
            default=None,
        ),
        forge.arg(
            "keepdims",
            type=bool,
            default=False,
        ),
    ]
    rtype = Tensor
    categories = [Category.ARITHMETIC_FUNCTIONS, Category.MANIPULATING_TENSORS]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        input_tensor = kwargs.get("input_tensor")
        # Make a copy of the input, since we'll mutate it.
        axis = kwargs.get("axis")
        keepdims = kwargs.get("keepdims")

        check_argument_numeric(input_tensor, "input_tensor")
        if isinstance(input_tensor, list):
            shapes = [
                validate_shape(tensor, f"input_tensor[{n}]")
                for n, tensor in enumerate(input_tensor)
            ]
            for index, shape in enumerate(shapes[1:]):
                check_argument(
                    shape == shapes[0],
                    "All elements of the input_tensor list must have the same shape.",
                    {"input_tensor": input_tensor},
                    extras={
                        "input_tensor[0].shape": shapes[0],
                        f"input_tensor[{index}].shape": shape,
                    },
                )
            # Note that if the input is an empty list then the shape is somewhat ambiguous (it
            # could be an empty list of tensors of any shape), but for consistency with TF and NP
            # we interpret it as 1D.
            shape = (len(shapes), *shapes[0]) if shapes else ()
        else:
            shape = validate_shape(input_tensor, "input_tensor")

        # Validate and sanitize the reduction axes.
        if axis is None:
            axis = list(range(len(shape)))
        elif isinstance(axis, int):
            axis = [axis]
        else:
            axis = list(axis)
        for i, dimension in enumerate(axis):
            check_argument(
                -len(shape) <= dimension < len(shape),
                f"Elements of axis must be valid axes of the input_tensor (between {-len(shape)} "
                f"and {len(shape)-1}, inclusive).",
                {"input_tensor": input_tensor, "axis": axis},
            )
            if dimension < 0:
                axis[i] = dimension + len(shape)
        axis_set = set(axis)
        check_argument(
            len(axis_set) == len(axis),
            "Elements of axis must refer to unique dimensions of the input_tensor.",
            {"input_tensor": input_tensor, "axis": axis},
        )

        # Calculate the output shape.
        output_shape = []
        for i, size in enumerate(shape):
            if i not in axis_set:
                output_shape.append(size)
                continue
            if keepdims:
                output_shape.append(1)
                continue

        return Tensor(_operation, shape=tuple(output_shape))


class Reverse(Node):
    """
    Reverses a tensor along some specified dimensions.

    Parameters
    ----------
    tensor : np.ndarray or Tensor
        The tensor that you want to reverse.
    axis : list[int]
        The dimensions along which you want to reverse the tensor.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The reversed tensor.
    """

    name = "reverse"
    args = [
        forge.arg("tensor", type=Union[np.ndarray, Tensor]),
        forge.arg("axis", type=List[int]),
    ]
    rtype = Tensor
    categories = [Category.MANIPULATING_TENSORS]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        tensor = kwargs.get("tensor")
        check_argument_numeric(tensor, "tensor")
        shape = validate_shape(tensor, "tensor")
        return Tensor(_operation, shape=shape)


class Repeat(Node):
    """
    Repeats elements of a tensor.

    Parameters
    ----------
    input : np.ndarray or Tensor
        The tensor whose elements you want to repeat.
    repeats : int or list[int]
        The number of times to repeat each element. If you pass a single int or singleton list, that
        number of repetitions is applied to each element. Otherwise, you must pass a list with the
        same length as `input` along the specified `axis` (or the same total length as `input` if
        you omit `axis`).
    axis : int, optional
        The axis along which you want to repeat elements. If you omit this value then the input is
        first flattened, and the repetitions applied to the flattened array.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The repeated tensor. The result has the same shape as `input` except along `axis`, where its
        size is either the sum of `repeats` (if `repeats` is a list with at least two elements) or
        the product of the original size along `axis` with `repeats` (if `repeats` is a single int
        or singleton list). If `axis` is `None` then the output is 1D, with the sizes as described
        above applied to the flattened input tensor.
    """

    name = "repeat"
    args = [
        forge.arg("input", type=Union[np.ndarray, Tensor]),
        forge.arg("repeats", type=Union[int, List[int]]),
        forge.arg("axis", type=Optional[int], default=None),
    ]
    rtype = Tensor
    categories = [Category.MANIPULATING_TENSORS]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        tensor = kwargs.get("input")
        repeats = kwargs.get("repeats")
        axis = kwargs.get("axis")

        check_argument_numeric(tensor, "tensor")
        shape = validate_shape(tensor, "tensor")

        if axis is None:
            shape = (np.prod(shape),)
            axis = 0

        if axis < 0:
            axis = len(shape) + axis

        if isinstance(repeats, int):
            repeats = [repeats]

        if len(repeats) == 1:
            repeats = [repeats[0] for _ in range(shape[axis])]
        else:
            check_argument(
                len(repeats) == shape[axis],
                "Length of repeats must be one or must match length of input along axis.",
                kwargs,
                extras={"length of input along axis": shape[axis]},
            )

        return Tensor(
            _operation, shape=shape[:axis] + (sum(repeats),) + shape[axis + 1 :]
        )


class CumulativeSum(Node):
    """
    Calculates the cumulative sum of a tensor along a specified dimension.

    Parameters
    ----------
    x : np.ndarray or Tensor
        The tensor whose elements you want to sum. It must have at least
        one dimension.
    axis : int, optional
        The dimension along which you want to sum the tensor. Defaults to 0.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The cumulative sum of `x` along dimension `axis`.
    """

    name = "cumulative_sum"
    args = [
        forge.arg("x", type=Union[np.ndarray, Tensor]),
        forge.arg("axis", default=0, type=int),
    ]
    rtype = Tensor
    categories = [Category.ARITHMETIC_FUNCTIONS, Category.MANIPULATING_TENSORS]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        if len(shape) == 0:
            raise QctrlException(
                f"The shape of x={x_value} must have at least 1 dimension."
            )
        return Tensor(_operation, shape=shape)


class Transpose(Node):
    """
    Returns the input tensor with its dimensions reordered.

    Parameters
    ----------
    a : np.ndarray or Tensor
        The tensor whose dimensions you want to permute, :math:`x`.
    perm : list[int] or np.ndarray(int), optional
        The order of the input dimensions for the returned tensor. If you provide it, it must
        be a permutation of all integers between 0 and ``N-1``, where `N` is the rank of `a`.
        If you don't provide it, the order of the dimensions is inverted, that is to say,
        it defaults to ``[N-1, …, 1, 0]``.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The input tensor with its dimensions permuted. The `i`-th dimension of the returned tensor
        corresponds to the `perm[i]`-th input dimension.

    See Also
    --------
    adjoint : Hermitian adjoint of an operator.
    einsum : Tensor contraction via Einstein summation convention.

    """

    name = "transpose"
    args = [
        forge.arg("a", type=Union[np.ndarray, Tensor]),
        forge.arg(
            "perm",
            type=Optional[Union[List[int], np.ndarray]],
            default=None,
        ),
    ]
    rtype = Tensor
    categories = [Category.LINEAR_ALGEBRA, Category.MANIPULATING_TENSORS]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        a_value = kwargs.get("a")
        perm = kwargs.get("perm")
        check_argument_numeric(a_value, "a")
        check_argument_numeric(perm, "perm")
        a_shape = validate_shape(a_value, "a")
        if perm is None:
            shape = a_shape[::-1]
        else:
            sorted_perm = np.sort(np.array(perm) % len(perm))
            check_argument(
                np.all(sorted_perm == range(len(a_shape))),
                "The value of perm must be a valid permutation of the indices of a.",
                {"perm": perm},
                extras={"a.shape": a_shape},
            )
            shape = tuple(a_shape[dimension] for dimension in perm)
        return Tensor(_operation, shape=shape)


class Einsum(Node):
    r"""
    Performs tensor contraction via Einstein summation convention.

    Use this node to perform multi-dimensional, linear algebraic array operations between tensors.

    Parameters
    ----------
    equation : str
        The equation describing the tensor contraction.
        The format is the same as in NumPy's einsum.
    tensors : list[Tensor or np.ndarray]
        The tensors to be contracted.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The contracted Tensor.

    See Also
    --------
    matmul : Matrix multiplication between objects.
    sum : Sum elements in a tensor along one or multiple axes.
    trace : Element-wise trace of an object.
    transpose : Reorder the dimensions of a tensor.

    Notes
    -----
    You can use tensor contraction with Einstein summation convention to create a new tensor from
    its element-wise computation from other tensors. This applies to any tensor operation that you
    can write as an equation relating the elements of the result as sums over products of elements
    of the inputs.

    The element-wise equation of the operation is summarized by a string describing the Einstein
    summation to be performed on the inputs. For example, the matrix multiplication between two
    matrices can be written as

    .. math::
        R_{ik} = \sum_j P_{ij} Q_{jk} .

    To convert this element-wise equation to the appropriate string, you can:
    remove summations and variable names (`ik = ij * jk`),
    move the output to the right (`ij * jk = ik`), and
    replace "`*`" with "`,`" and "`=`" with "`->`" (`ij,jk->ik`).
    You can also use an ellipsis (...) to broadcast over unchanged dimensions.

    For more information about Einstein summation, see `Einstein notation on Wikipedia`_.

    .. _Einstein notation on Wikipedia:
        https://en.wikipedia.org/wiki/Einstein_notation

    Examples
    --------
    >>> # Diagonal of a matrix.
    >>> graph.einsum('ii->i', [np.ones([5,5])])
        <Tensor: name="einsum_#0", operation_name="einsum", shape=(5,)>

    >>> # Trace of a matrix.
    >>> graph.einsum('ii->', [np.ones([5,5])])
        <Tensor: name="einsum_#1", operation_name="einsum", shape=()>

    >>> # Sum over matrix axis.
    >>> graph.einsum('ij->i', [np.ones([10,5])])
        <Tensor: name="einsum_#2", operation_name="einsum", shape=(10,)>

    >>> # Sum over tensor axis ignoring leading dimensions.
    >>> graph.einsum('...ji->...i', [np.ones([2,3,4,5])])
        <Tensor: name="einsum_#3", operation_name="einsum", shape=(2, 3, 5)>

    >>> # Reorder tensor axes.
    >>> graph.einsum('ijkl->lkij', [np.ones([2,3,4,5])])
        <Tensor: name="einsum_#4", operation_name="einsum", shape=(5, 4, 2, 3)>

    >>> # Vector inner product.
    >>> graph.einsum('i,i->', [np.ones(5), np.ones(5)])
        <Tensor: name="einsum_#5", operation_name="einsum", shape=()>

    >>> # Matrix-vector multiplication.
    >>> graph.einsum('ij,j->i', [np.ones([4,5]), np.ones(5)])
        <Tensor: name="einsum_#6", operation_name="einsum", shape=(4,)>

    >>> # Vector outer product.
    >>> graph.einsum('i,j->ij', [np.ones([4]), np.ones([3])])
        <Tensor: name="einsum_#7", operation_name="einsum", shape=(4, 3)>

    >>> # Tensor contraction.
    >>> graph.einsum('ijk,jil->kl', [np.ones([3,4,5]), np.ones([4,3,2])])
        <Tensor: name="einsum_#8", operation_name="einsum", shape=(5, 2)>

    >>> # Trace along first two axes.
    >>> graph.einsum('ii...->i...', [np.ones([5,5,2,4])])
        <Tensor: name="einsum_#9", operation_name="einsum", shape=(5, 2, 4)>

    >>> # Matrix multiplication using the left-most indices.
    >>> graph.einsum('ij...,jk...->ik...', [np.ones([5,3,2,4]), np.ones([3,5,2,4])])
        <Tensor: name="einsum_#10", operation_name="einsum", shape=(5, 5, 2, 4)>
    """

    name = "einsum"
    args = [
        forge.arg("equation", type=str),
        forge.arg("tensors", type=List[Union[np.ndarray, Tensor]]),
    ]
    rtype = Tensor
    categories = [Category.MANIPULATING_TENSORS, Category.LINEAR_ALGEBRA]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        tensors = kwargs.get("tensors")

        check_argument(
            isinstance(tensors, list),
            "The tensors must be in a list.",
            {"tensors": tensors},
        )
        check_argument(
            all(isinstance(tensor, (Tensor, np.ndarray)) for tensor in tensors),
            "Each of the tensors must be a Tensor or a np.ndarray.",
            {"tensors": tensors},
        )

        equation = kwargs.get("equation")
        check_argument(
            isinstance(equation, str),
            "The equation must be a string.",
            {"equation": equation},
        )

        try:
            shape = np.einsum(
                equation, *[np.zeros(tensor.shape) for tensor in tensors]
            ).shape
        except ValueError:
            check_argument(
                False,
                "The equation is not valid or is incompatible with the inputs.",
                {"tensors": tensors, "equation": equation},
            )

        return Tensor(_operation, shape=shape)
