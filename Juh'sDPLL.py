#!/usr/bin/env python
# coding=utf-8

import sudoku

def trataFormula(f):
	# faz uma lista de dicionários, onde cada dicionário é uma cláusula
	clause = {}
	formula = []
	i = 0
	s = ''
	tamanho = len(f)
	while i < tamanho:
		if f[i] != 'v' and f[i] != '^':
			s = s + f[i]
			i = i+1
		elif f[i] == 'v':
			clause[s] = '*'
			s = ''
			i = i+1
		elif f[i] == '^':
			clause[s] = '*'
			s = ''
			formula.append(clause)
			clause = {}
			i = i+1

	clause[s] = '*'
	formula.append(clause)
	
	return formula


def hasUnitClause(f):

	unitClause = ''

	for c in f:
		for l in c:
			if len(c) == 1:
				unitClause = l
				break

	return unitClause


def simplifica(f):

	unitClause = hasUnitClause(f)
	while unitClause: #f possui alguma cláusula unitária L
		#apaga de f toda cláusula que contém L
		for c in f:
			if c.has_key(unitClause):
				f.remove(c)
		#apaga ¬L das cláusulas restantes
		for c in f:
			if unitClause[0] == '~':
				if c.has_key(unitClause[1:]):
					del c[unitClause[1:]]
			else:
				if c.has_key('~'+unitClause):
					del c['~'+unitClause]

		unitClause = hasUnitClause(f)

	return f


def dpll(formula):
	
	form_simple = simplifica(formula)
	if form_simple == []:
		return True
	else: #se form_simple contém uma cláusula vazia:
		for c in form_simple: 
			if len(c) == 0:
				return False
	#escolha um literal L com v(L) == "*"
	for c in form_simple:
		for l, v in c.items():
			if v == '*':
				literal = l

	c1 = {literal: '*'}
	if literal[0] == '~':
		c2 = {literal[1:]: '*'}
	else:	
		c2 = {'~'+literal: '*'}

	form_simple1 = list(form_simple)
	form_simple1.append(c1)
	form_simple2 = list(form_simple)
	form_simple2.append(c2)

	if dpll(form_simple1) == True:
		for c in val:
			for l, v in c.items():
				if l == literal:
					c[l] = 'V'
				elif l == '~'+literal or l == literal[1:]:
					c[l] = 'F'
				else:
					c[l] = 'V'
		return True
	elif dpll(form_simple2) == True:
		return True
	else:
		return False
		


#f = '~qvpvr^~pvq^r'	#True
#f = '~x1^x1vx2^x1vx3^~x2v~x3v~x4v~x5^~x1vx4' #True
#f = 'pvqv~rv~q'	#True
f = '~qv~pvr'		#True
#f = '~q1vp1vr12^~p1vq1^r12'	#True
#f = 'pvq^~pvq^pv~q^~pv~q'	#False

f2 = trataFormula(f)
val = list(f2)
print 'Fórmula:\n', f2
resultado = dpll(f2)

print resultado
print '\nValoração válida:\n', val

"""

formula_sudoku = sudoku.sudoku_clauses('sudoku1.txt')
resultado = dpll(formula_sudoku)
print resultado

"""


