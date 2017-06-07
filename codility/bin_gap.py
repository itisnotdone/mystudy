def solution(N):
    zeros = set(str(bin(N))[2:].split('1'))
    # print(zeros)
    zeros.discard('')

    maxnum = 0
    if zeros:
    	final = []
    	for each in zeros:
    		final.append(len(each))
    	maxnum = max(final)

    return maxnum

print (solution(51712))
