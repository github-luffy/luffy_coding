# -*- coding:utf-8 -*-


def compress_str(string):
	result = ''
	count = 1
	current = string[0]
	for ch in string[1:]:
		if ch == current:
			count += 1
		else:
			result += current + str(count)
			count = 1
			current = ch
	result += current + str(count)
	if len(result) >= len(string):
		return string
	return result


def compress_str1(string):
	result = []
	count = 1
	current = string[0]
	for ch in string[1:]:
		if ch == current:
			count += 1
		else:
			result.append(current)
			result.append(str(count))
			count = 1
			current = ch
	result.append(current)
	result.append(str(count))
	if len(result) >= len(string):
		return string
	return ''.join(result)


def check_str(string):
	if not string:
		return 0
	size = 2
	current = string[0]
	for ch in string[1:]:
		if ch != current:
			size += 2
			current = ch
	return size
	

def compress_str2(string):
	if check_str(string) >= len(string):
		return string
	result = []
	count = 1
	current = string[0]
	for ch in string[1:]:
		if ch == current:
			count += 1
		else:
			result.append(current)
			result.append(str(count))
			count = 1
			current = ch
	result.append(current)
	result.append(str(count))
	return ''.join(result)


if __name__ == '__main__':
	# print compress_str('aasd')
	# print compress_str1('aasd')
	list = ["aasd", "aabbbcccdddd", "aabccddssff"]
	for str_in_list in list:
		print compress_str2(str_in_list)
