def solution(N, S):
    cnt = 0
    reserved_seats = set(S.split(' '))

    all_seats = [[str(r) + alpha for alpha in list(str('ABCDEFGHJK'))] for r in range(1, N+1)]
    # from pprint import pprint as pp
    # pp(all_seats)
    # print "{} have been reserved.".format(S)

    for r in all_seats:
    	if set(r[:3]).isdisjoint(reserved_seats):
    		cnt += 1
    	if set(r[3:6]).isdisjoint(reserved_seats) or set(r[4:7]).isdisjoint(reserved_seats):
    		cnt += 1
    	if set(r[7:]).isdisjoint(reserved_seats):
    		cnt += 1

    return cnt

print (solution(2, "1A 2F 1C"))
