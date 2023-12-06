\\ Isak Volodymyr KI-303 Python Compiler Test Program

factorial -> 1
counter -> 5
result -> 0
n -> 10
a -> -1 * -2

\\ test -> 1 * 2 * 3 * 4 * 5 * 6 * 7 * 8 * 9 * 10

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
print(a)