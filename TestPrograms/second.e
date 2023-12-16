\\ Isak Volodymyr KI-303 Second Test Program

first -> 0
second -> 0
third -> 0
zero -> 0
ten -> 10
one -> 1
minus_one -> -1

scan(first)
scan(second)
scan(third)

if first <= second then goto first_smaller
if first <= third then goto first_smaller

print(first)

first_smaller:

if second <= third then goto second_smaller

print(second)

second_smaller:

print(third)


if first != second then goto not_equal
if first != third then goto not_equal
if second != third then goto not_equal

print(one)
goto end_first

not_equal:
print(zero)

end_first:

if first <= -1 then goto minus
if second <= -1 then goto minus
if third <= -1 then goto minus

print(zero)

goto end_second

minus:

print(minus_one)

end_second:

sum -> second + third + 1

if first <= second then goto less

print(ten)
goto end

less:

print(zero)

end:
