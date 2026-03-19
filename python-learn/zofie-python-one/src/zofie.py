#!/usr/bin/, input_int_arra



# Python program to take integer input  in Python

# input size of the list
n = int(input("Enter the size of list : "))
# store integers in a list using map, split and strip functions
lst = list(map(int, input(
    "Enter the integer elements of list(Space-Separated): ").strip().split()))[:n]
print('The list is:', lst)   # printing the list