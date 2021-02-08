def freq(file):
	lf = {}
	for ch in file:
		try:
			lf[ch] += 1
		except:
			lf[ch] = 1

	print(lf)
	sorted_lf = sorted(lf.items(), key=lambda x:x[1], reverse=True)
	print(sorted_lf)

def remv_caps(file):
	final = ''
	for ch in file:
		if not ch.isupper():
			final += ch
	print(final)

def remv_small(file):
	final = ''
	for ch in file:
		if not ch.islower():
			final += ch
	print(final)

def remv_rep(file):
	final = ''
	for i in range(len(file) - 1):
		if file[i] == file[i+1]:
			i += 1
		else:
			final += file[i]
	print(final)

def dub(file):
	final = file[::5]
	print(final)

def get_hex(file):
	string = '0123456789abcdef'
	final = ''
	for ch in file:
		if ch in string:
			final += ch
	print(final)

if __name__ == '__main__':

	cipher = "2syusZZtTxpmmHLuikOLmiwXHgLoUNVGTLYQnIMnKHJOWWwmtyYUihHuNLyYWXUwoZOysnLZULGxxTqqkKuGnHTVPwyWlgHzUkZTJwGRWVlmgmYYiSYLmk9OmLwUoWYhuwXtRNIGPZOqVLnHQMwkyHmVNHRSYsgQoLsJyGuSLUGymlxNjLvYzkjHwvJIrHnmzyIyrlhuUqlINPLYKlLoqtPOyHZliHyvnRmltsX9f9e29b8cQzhuUgHhQqlgZkHRtjyJgqpRuyNHWKIHIptihWKuJGgGNqWuiuLPgXLVOYlpgLUkMTrsRGGYUYjtxjXzYWouZGpoLyskrzuSZWjtKrijrwzSmjOTNtIgJtXY017b7HzOGVUxvhPxjGGMXTsVxwOWMGNJsiJHpVKngtZprToOlGIOmXwuppONjTGLlwwYHXgYVOxVuMrSmxHIxSxnllVvOymHulySNsXwjiprzIzQuZgqSJla98f4b36110uzQQwJgIqXzgGwJzuynNjuVUMyiWgpHWWZjVNoOTVSRSUHmMozUOtpggYShQvJyYLkWXwlhmLROiHRyyuvYSluSknPommkLurGTMSMJLWvlhxPIMnwLVOVLuMHQR7c4ZWkpGtUHTTNiMoixiSOzjpnvliXsUltulZmZmlKwPHVrSrLxpszmnxJmlsKgkkhpXUkmwUlPUKhsGmiPLwuksNmjWuntYOqvmUjMpiqlqhzXtvsZhZTornJ5bUjOoOnPhNYzrkuJGruZzsIQLnIzGNTupyTVooQhlMGWJkHTphQSqpGgNnSPXPJqYtiHrrVNJwLpwKZruzZjTWUGpltPRMgrnyIUWwKiuxLsWXnLSqljHhRHktj"
	# remv_caps(file)
	# remv_small(file)
	# dub(file)
	get_hex(cipher)

# 299f9e29b8c017b7a98f4b361107c45b -> md5("0K")
# 0xL4ugh{0K}