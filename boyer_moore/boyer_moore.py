#!/usr/bin/env python3

import random, timeit

ALPHABET = 'abcdefghijklmnopqrstuvwxyz.,?! '

def last_ocurrence_idx(word, c):
	for i in range(len(word)-1, -1, -1):
		if word[i] == c:
			return i
	return -1

def L_dict(word):
	ret = {}
	for a in ALPHABET:
		ret[a] = last_ocurrence_idx(word, a)
	return ret

def np_match(n, p, word, start):
	assert(len(n) == 1)

	p_len = len(p)
	word_len = len(word)

	if start >= 0 and word_len > 0 and word[start] == n: return False

	for i, p_char in enumerate(p):
		word_idx = start + i + 1
		if word_idx < 0: continue
		if word_idx >= word_len: return False
		if word[word_idx] != p_char: return False

	return True

def rightmost_np_match(i, n, p, word):
	for j in range(i, -len(word)-1, -1):
		if np_match(n, p, word, j):
			return j
	assert False

# todo: rewrite from O(n^2) to O(n)

def SS_arr(word):
	ret = []
	for i in range(len(word)):
		n = word[i]
		p = word[i+1:]

		ret += [rightmost_np_match(i, n, p, word)]

	return ret


def boyer_moore(pattern, text):
	L = L_dict(pattern)
	S = SS_arr(pattern)

	m = len(pattern)
	n = len(text)

	i = m - 1
	j = m - 1

	while i < n and j >= 0:
		if text[i] == pattern[j]:
			i -= 1
			j -= 1
		else:
			i = i + m - 1 - min(L[text[i]], S[j])
			j = m - 1

	return j == -1

# todo: these don't actually work...

def boyer_moore_good_suffix_only(pattern, text):
	S = SS_arr(pattern)

	m = len(pattern)
	n = len(text)

	i = m - 1
	j = m - 1

	while i < n and j >= 0:
		if text[i] == pattern[j]:
			i -= 1
			j -= 1
		else:
			i = i + m - 1 - min(-1, S[j])
			j = m - 1

	return j == -1


def boyer_moore_bad_char_only(pattern, text):
	L = L_dict(pattern)

	m = len(pattern)
	n = len(text)

	i = m - 1
	j = m - 1

	while i < n and j >= 0:
		if text[i] == pattern[j]:
			i -= 1
			j -= 1
		else:
			i = i + m - 1 - min(-1, L[text[i]])
			j = m - 1

	return j == -1

def naive_exact_match(pattern, text, i):
	for j in range(0, len(pattern)):
		if pattern[j] != text[i + j]: return False
	return True

def naive_match(pattern, text):
	for i in range(0, len(text) - len(pattern)):
		if naive_exact_match(pattern, text, i):
			return True
	return False

def check(m, n):
	pattern = ' '.join(random.choice(ALPHABET) for _ in range(m))
	text = ' '.join(random.choice(ALPHABET) for _ in range(n))

	res = pattern in text

	assert res == boyer_moore(pattern, text)
	assert res == boyer_moore_bad_char_only(pattern, text)
	assert res == boyer_moore_good_suffix_only(pattern, text)
	assert res == naive_match(pattern, text)

	substr_start = random.randint(0, n - m)
	substr = text[substr_start:substr_start + m]

	assert boyer_moore(substr, text)
	assert boyer_moore_bad_char_only(substr, text)
	assert boyer_moore_good_suffix_only(substr, text)
	assert naive_match(substr, text)


assert tuple(SS_arr('bonobobo')) == (-6, -5, -4, -3, 2, -1, 2, 6)
for _ in range(0):
	check(4, 20000)

with open('./alice.txt') as alice_file:
	alice = alice_file.readlines()

alice = ' '.join(alice)
alice = alice.replace('\n', ' ')
alice = alice.lower()
alice = ''.join(c for c in alice if c in ALPHABET)

PATTERN_LENGTH = 100

offset = len(alice) - random.randint(PATTERN_LENGTH, 2*PATTERN_LENGTH)

def time_bm():
	boyer_moore(alice[offset:offset+PATTERN_LENGTH], alice)

def time_bm_gs():
	boyer_moore_good_suffix_only(alice[offset:offset+PATTERN_LENGTH], alice)

def time_bm_bc():
	boyer_moore_bad_char_only(alice[offset:offset+PATTERN_LENGTH], alice)

def time_native():
	alice[offset:offset+PATTERN_LENGTH] in alice

def time_naive():
	naive_match(alice[offset:offset+PATTERN_LENGTH], alice)

# print('        native', timeit.timeit(time_native, number=1))
print('         naive', '%f' % timeit.timeit(time_naive, number=1))
print('   boyer_moore', '%f' % timeit.timeit(time_bm, number=1))
# print('boyer_moore_gs', '%f' % timeit.timeit(time_bm_gs, number=1))
# print('boyer_moore_bc', '%f' % timeit.timeit(time_bm_bc, number=1))