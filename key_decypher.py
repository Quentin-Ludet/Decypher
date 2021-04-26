#%%
#start by reading the file with the coded message
file = open('coded_message.txt', 'r')
code = file.read()
print('code given:')
print(code)


#%%
#now read the key
file = open('key.txt', 'r')
key = file.read().split(',')
print('Key:')
print(key)


# %%
#function to find the letter based on the key
def getLetter(letter):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    if letter in alphabet:
        return alphabet[key.index(letter)]
    else:
        return letter


# %%
#now decode the message
message = ''
for letter in code:
    message += getLetter(letter)

print('New decoded message: ')
print(message)

# %%
# Save the solution

file = open('decoded_message.txt', 'w')
file.write(message)
file.close
print('Message saved in decoded_message.txt')


# %%