#!/usr/bin/env python3

# https://www.youtube.com/watch?v=4n7NPk5lwbI

import random

ALPHABET = 'abcdefghijklmnopqrstuv'

def bwm(text):
	ret = []

	for _ in range(len(text)):
		ret += [text]
		text = text[1:] + text[0]

	return ret

def bwt(text):
	sorted_bwm = sorted(bwm(text))
	return ''.join(_[-1] for _ in sorted_bwm)

def b_order(text):

	alphabet = set(text)

	next_idx = {}

	for c in alphabet:
		next_idx[c] = 0

	ret = []

	for c in text:
		ret += [(c, next_idx[c])]
		next_idx[c] += 1

	return ret

def inv_bwt(text):
	L = b_order(text)
	F = sorted(L)

	idx_in_F = {}

	for i, e in enumerate(F):
		idx_in_F[e] = i

	current_char = ('$', 0)

	ret = ''

	for _ in range(len(L)):
		char, _ = current_char
		ret += char

		current_char = L[idx_in_F[current_char]]



	return ret[::-1]

def check(s):
	assert s == inv_bwt(bwt(s))

def check_random(n):
	s = ''.join(random.choice(ALPHABET) for _ in range(n))
	s = s + '$'
	check(s)

check('alf_eats_alfafa$')
check('abaaba$')

for _ in range(1000):
	check_random(100)
