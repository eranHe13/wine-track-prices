import difflib



'''
script for validate the input wine name and the result wine name to check for correct result
atleast 85%
'''

def compute_similarity(input_string, reference_string):
#The ndiff method returns a list of strings representing the differences between the two input strings.
    diff = difflib.ndiff(input_string, reference_string)
    diff_count = 0
    for line in diff:
      # a "-", indicating that it is a deleted character from the input string.
        if line.startswith("-"):
            diff_count += 1
# calculates the similarity by subtracting the ratio of the number of deleted characters to the length of the input string from 1
    return 1 - (diff_count / len(input_string))
 