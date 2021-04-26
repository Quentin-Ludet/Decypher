# cypher a message
#%%
#start by reading the file with the message
file = open('message.txt', 'r')
message = file.read()
print('Message given:')
print(message)


#%%
#now read the key
file = open('key.txt', 'r')
key = file.read().split(',')
print('Key:')
print(key)


# %%
#function to find the value of a message letter
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
def getIndex(letter):
    return alphabet.index(letter.lower())


# %%
#now encode the message
code = ''
for letter in message:
    if letter.lower() in alphabet:
        code += key[getIndex(letter.lower())]
    else:
        code += letter

print('New encoded message: ')
print(code)


# %%
#now save the encoded message to a file
file = open('coded_message.txt', 'w')
file.write(code)
file.close
print('Message saved in coded_message.txt')
# %%
