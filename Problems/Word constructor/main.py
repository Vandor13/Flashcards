word1 = input()
word2 = input()
brand = []
for letter1, letter2 in zip(word1, word2):
    brand.append(letter1)
    brand.append(letter2)
print("".join(brand))
