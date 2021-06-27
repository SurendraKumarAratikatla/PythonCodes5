# Array subsequences function
def subsequences(a, b):
    sub_list = []
    list_values = [a[i:j:k] for k in range(1, len(a)) for i in range(len(a)) for j in range(b, len(a) + 1) if len(a[i:j:k]) == b and sum(a[i:j:k]) <= 1000]
    for sub in list_values:
        if sub not in sub_list:
            sub_list.append(sub)
    return len(sub_list)

# input
a = input("A = ")
b = int(input("B = "))

a = eval(a)  # converting sting to list
count = 0

# validations
if 1 <= len(a) <= 20 and 1 <= b <= len(a):
    for i in a:
        if 1 <= i <= 1000:
            count += 1
    if count == len(a):
        print(subsequences(a, b))
    else:
        print("Given array value is out of boundary, it should be in 1 <= A[i] <= 1000, please maintain correctly")
else:
    print("Given 'a' or 'b' value out of boundary, A length should be in 1 <= A <= 20  and  B should be in 1 <= N <= A")
