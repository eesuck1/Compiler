\\ Isak Volodymyr KI-303 Python Compiler Test Program

factorial -> 1
counter -> 5

result -> 0
n -> 10

\\ scan(a)
print(a)

\\ scan($7)
print($7)

test -> 1 * 2 * 3 * 4 * 5 * 6 * 7 * 8 * 9 * 10
print(test)


test_brackets -> ((1 + 2) * (10 / 2)) * (7 / 3) % 7
\\ 15 * 2 % 7 = 30 % 7 = 2
print(test_brackets)

division -> 1000 / (5 / 4)
print(division)

loop:
if n == 0 then goto power_end

result -> result + n * n
n -> n - 1

goto loop

power_end:

factorial_loop:
if counter == 1 then goto end

factorial -> factorial * counter
counter -> counter - 1

goto factorial_loop

end:
print(result)
print(factorial)