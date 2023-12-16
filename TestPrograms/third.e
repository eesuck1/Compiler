\\ Isak Volodymyr KI-303 Third Test Program

first -> 0
second -> 0
square -> 0
x -> 0
a -> 0
b -> 0

scan(first)
scan(second)

first_dummy -> first + 0

square_loop:

square -> first_dummy * first_dummy
print(square)
first_dummy -> first_dummy + 1

if first_dummy >= second then goto end_square_loop

goto square_loop

end_square_loop:

a_loop:

if a >= first then goto end

b -> 0
a -> a + 1

b_loop:

x -> x + 1
b -> b + 1

if b >= second then goto a_loop
goto b_loop

end:

print(x)