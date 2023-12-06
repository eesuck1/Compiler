n -> 1
counter -> 5
test -> 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10

loop:
if counter == 1 then goto end

n -> n * counter
counter -> counter - 1

goto loop

end:
print(n)
print(test)