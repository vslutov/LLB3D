# -*- coding: utf-8 -*-

"""Test case for ast."""

from pytest import raises

from .. import ast

def test_frosen_dict():
    """Test frozen dict."""
    frozen_dict = ast.FrozenDict(a=10, b=20)
    assert len(frozen_dict) == 2
    assert ['a', 'b'] == sorted(frozen_dict)
    assert frozen_dict['a'] == 10
    assert frozen_dict['b'] == 20

    with raises(KeyError):
        print(frozen_dict['c'])

    assert frozen_dict != {'a': 10, 'b': 20}

    other_frozen_dict = ast.FrozenDict(a=10, b=20)

    assert hash(frozen_dict) == hash(other_frozen_dict)
    assert frozen_dict == other_frozen_dict

def test_abstract_literal():
    """Test abstract literal."""
    value = 10
    lit = ast.Literal(value)
    assert lit['value'] == value
    assert str(lit) == str(value)
    assert repr(lit) == 'Literal(10)'

def test_integer_literal():
    """Test abstract literal."""
    value = 10

    lit = ast.IntLiteral(value)
    assert lit['value'] == value
    assert str(lit) == str(value)
    assert repr(lit) == 'IntLiteral({value})'.format(value=value)

    with raises(TypeError):
        ast.IntLiteral('string')

def test_float_literal():
    """Test float literal."""
    value = 10.0

    lit = ast.FloatLiteral(value)
    assert lit['value'] == value
    assert str(lit) == str(value)
    assert repr(lit) == 'FloatLiteral({value})'.format(value=value)

    with raises(TypeError):
        ast.FloatLiteral('string')

def test_string_literal():
    """Test string literal."""
    value = 'abacaba'

    lit = ast.StrLiteral(value)
    assert lit['value'] == value
    assert str(lit) == str(value)
    assert repr(lit) == "StrLiteral('{value}')".format(value=value)

    with raises(TypeError):
        ast.StrLiteral(10)

def test_unary_operator():
    """Test unary operator."""
    right = ast.IntLiteral(20)
    operator = '-'

    expr = ast.UnaryOp(operator, right)
    assert expr['op'] is operator
    assert expr['right'] is right
    assert str(expr) == '-20'
    assert repr(expr) == "UnaryOp('-', {right})".format(right=repr(right))

    with raises(TypeError):
        ast.UnaryOp(operator, 'not an expression')

def test_binary_operator():
    """Test binary operator."""
    left = ast.IntLiteral(10)
    right = ast.IntLiteral(20)
    operator = '+'

    expr = ast.BinaryOp(operator, left, right)
    assert expr['op'] is operator
    assert expr['left'] is left
    assert expr['right'] is right
    assert str(expr) == '(10 + 20)'
    assert repr(expr) == "BinaryOp('+', {left}, {right})".format(left=repr(left), right=repr(right))

    with raises(TypeError):
        ast.BinaryOp(operator, left, 'not an expression')

def test_procedure():
    """Test procedure."""
    procedure = ast.Identifier('Graphics')
    args = (ast.IntLiteral(800), ast.IntLiteral(600))

    statement = ast.ProcedureCall(procedure, args)
    assert statement['procedure'] is procedure
    assert statement['args'] is args
    assert str(statement) == 'Graphics 800, 600'
    assert repr(statement) == ("ProcedureCall({procedure}, {args})"
                               .format(procedure=repr(procedure), args=repr(args)))

    with raises(TypeError):
        ast.ProcedureCall(procedure, 'not an expression')
