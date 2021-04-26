Decypher is trained on example english text and a list of common words to predict if a series of letters is english.
It will randomly test different keys which connect letters to other letters, and then choose the key that leads to a message which is most similar to english.

To decode a message without a key,
1. Place the encoded message in coded_message.txt
2. Run decypher
3. Find the message in decoded_message.txt

To create an encoded message,
1. Place the message in message.txt
2. Place a key in key.txt (the key should be a list of 26 different letters separated by single commas)
3. Run cypher
4. Find the encoded message in coded_message.txt

To decode a message with a key,
1. Place the encoded message in coded_message.txt
2. Place the key in key.txt (the key should be a list of 26 different letters separated by single commas)
3. Run key_decypher
4. Find the decoded message in decoded_message.txt

To use your own training data and dictionary,
1. Replace training.txt with any long english text (this will hardly affect performance)
2. Replace english_words.txt with a list of words to be recognized, separated by newlines (this will *significantly* affect performance)

Decypher is a statistical model, and will be much more accurate on longer messages, with accurate training data, and with a comprehensive dictionary.
