#%%
#start by reading the file with the coded message
file = open('coded_message.txt', 'r')
code = file.read()
print('code given:')
print(code)


#%%
# assume that the key is just the alphabet
key = alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']



#%%
#now find which letters are most common in english for a baseline key
file = open('training.txt', 'r', encoding='utf8')
text_letters =  ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', 'other']
text = file.read()
letter_count = [0] * len(text_letters)
for letter in text:
    if letter.lower() in text_letters:
        letter_count[text_letters.index(letter.lower())] += 1
    else:
        letter_count[-1] += 1

print(letter_count)
print('Summary:')

most_common = []
count_sorted = sorted(letter_count, reverse=True)
for count in count_sorted:
    most_common.append(text_letters[letter_count.index(count)])
most_common.pop(0)

print('Letters in order: ' + str(most_common))
print("Most common letter: '" + most_common[0] + "' with " + str(letter_count[text_letters.index(most_common[0])]) + ' appearances')
print("Least common letter: '" + most_common[-1] + "' with " + str(letter_count[text_letters.index(most_common[-1])]) + ' appearances')



# %%
# most common in coded message:
code_letters =  ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', 'other']
code_letter_count = [0] * len(code_letters)
for letter in code:
    if letter in code_letters:
        code_letter_count[code_letters.index(letter)] += 1
    else:
        code_letter_count[-1] += 1

code_most_common = []
code_count_sorted = sorted(code_letter_count, reverse=True)
last_count = None
last_index = 0
for count in code_count_sorted:
    if last_count != count:
        code_most_common.append(code_letters[code_letter_count.index(count)])
        last_index = code_letter_count.index(count)
    else:
        code_most_common.append(code_letters[code_letter_count.index(count, last_index + 1)])
        last_index = code_letter_count.index(count, last_index + 1)
    last_count = count
code_most_common.pop(code_most_common.index('other'))
print('Most common in code:')
print(code_most_common)



# %%
# create the first key

solution = {}
for key in code_most_common:
    for original in most_common:
        solution[key] = original
        most_common.remove(original)
        break

# %%
# test to see the result using the predicted key

def decode(solution):
    message = ''
    for letter in code:
        if letter.lower() in alphabet[:-1]:
            message += solution[letter]
        else:
            message += letter
    return message

print('New decoded message: ')
print(decode(solution))


# %%
# establish a list of english words

file = open('english_words.txt', 'r')
english_words = file.read().split('\n')
print('Keeping track of ' + str(len(english_words)) + ' words')


# %%
# create a matrix to find the probability of a string of letters

import numpy as np
from numba import jit

probability = np.zeros((27, 27))

last_letter = ' '
letter_count = 0
for letter in text:
    if not letter in alphabet:
        continue
    letter = letter.lower()
    probability[alphabet.index(last_letter)][alphabet.index(letter)] += 1
    last_letter = letter
    letter_count += 1

for value in probability:
    value /= letter_count

@jit
def probability_estimate_dictionary(text):
    last_letter = ' '
    comparison_count = 0
    prob_sum = 0
    for letter in text:
        if not letter in alphabet:
            last_letter = ' '
            continue
        letter = letter.lower()
        prob_sum += probability[alphabet.index(last_letter)][alphabet.index(letter)]
        last_letter = letter
        comparison_count += 1
    word_count = 0.
    real_words = 0.
    for word in text.split(' '):
        word_count += 1
        if word in english_words:
            real_words += 1
    return (prob_sum * 50 / comparison_count) + (real_words / word_count)

@jit
def probability_estimate(text):
    last_letter = ' '
    comparison_count = 0
    prob_sum = 0
    for letter in text:
        if not letter in alphabet:
            last_letter = ' '
            continue
        letter = letter.lower()
        prob_sum += probability[alphabet.index(last_letter)][alphabet.index(letter)]
        last_letter = letter
        comparison_count += 1
    return (prob_sum * 100 / comparison_count)




# %%
# now start testing random changes to see if it becomes better
import random
import copy

def switch_keys(key1, key2):
    temp = solution[key1]
    solution[key1] = solution[key2]
    solution[key2] = temp

best_solution = copy.deepcopy(solution)
best_accuracy = probability_estimate(decode(best_solution))
all_time_best_acc = 0
all_time_best_sol = copy.deepcopy(solution)
past_best_accuracy = 0
try_new = 0
print('starting probability')
print(best_accuracy)
for i in range(100000 - 1):
    switch_keys(alphabet[random.randint(0,25)], alphabet[random.randint(0,25)])
    if try_new > 0 or probability_estimate(decode(solution)) > best_accuracy:
        best_solution = copy.deepcopy(solution)
        best_accuracy = probability_estimate(decode(best_solution))
        try_new -= 1
    else:
        solution = copy.deepcopy(best_solution)
    if i % 1000 == 0:
        print(str(i) + '   ' + str(best_accuracy))
        if best_accuracy > all_time_best_acc:
            all_time_best_acc = best_accuracy
            all_time_best_sol = copy.deepcopy(best_solution)
        if abs(past_best_accuracy - best_accuracy) < 0.0001:
            print('trying random changes')
            try_new = 3
        past_best_accuracy = best_accuracy

best_solution = all_time_best_sol
best_accuracy = probability_estimate_dictionary(decode(best_solution))
#%%
# now using the dictionary
for i in range(20000 - 1):
    switch_keys(alphabet[random.randint(0,25)], alphabet[random.randint(0,25)])
    if try_new > 0 or probability_estimate_dictionary(decode(solution)) > best_accuracy:
        best_solution = copy.deepcopy(solution)
        best_accuracy = probability_estimate_dictionary(decode(best_solution))
        try_new -= 1
    else:
        solution = copy.deepcopy(best_solution)
    if i % 1000 == 0:
        print(str(i) + '   ' + str(best_accuracy))
        if best_accuracy > all_time_best_acc:
            all_time_best_acc = best_accuracy
            all_time_best_sol = copy.deepcopy(best_solution)
        if abs(past_best_accuracy - best_accuracy) < 0.0001:
            print('trying random changes')
            try_new = 3
        past_best_accuracy = best_accuracy


# %%
# finally decode the best solution

print('Final probability:')
print(all_time_best_acc)



print('Final answer: ')
print(decode(all_time_best_sol))


# %%
# Save the solution

file = open('decoded_message.txt', 'w')
file.write(decode(all_time_best_sol))
file.close
print('Message saved in decoded_message.txt')


# %%
