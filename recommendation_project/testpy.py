
#print number from 1 to 100

# for i in range(1,100):
#     print(i)

#2. Print even numbers from 1 to 20


# for i in range(1,20):
#     if i%2==0:
#         print(i)
#Print odd numbers from 1 to 20
# for i in range(1,20):
#     if i%2!=0:
#         print(i)

#4. Find sum of numbers 1 to 100


# total = 0

# for i in range(1, 101):
#     total += i

# print(total)

#5. Print multiplication table of 5

# for i in range(1, 11):
#     print(i*5)

#Count numbers greater than 50

# numbers = [10, 55, 80, 23, 99,100,50, 49]
# count=0
# for num in numbers:
#     if num>=50:
#         count+=1
# print(count)
#Print all names from list

# name=['Alice', 'Bob', 'Charlie', 'David']
# for n in name:
#     print(n)

#Find largest number
numbers = [4, 9, 2, 15, 100]
k=numbers[0]
for num in numbers:
    if num>k:
        k=num
print(k)

#Find smallest number
numbers = [4, 9, 2, 15, 100]
k=numbers[0]
for num in numbers:
    if num<k:
        k=num
print(k)

#Count vowels in string
text = "batmania is the best movie"
v='aeiou'
count=0
for i in text:
    if i in v:
        count+=1
print(count)



