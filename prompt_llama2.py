from langchain.llms import Ollama
ollama = Ollama(base_url='http://localhost:11434', model="llama2")
#print(ollama("given the main concept 'food' and sub concepts 'animal', 'fly', 'yellow' and 'black' which of the following candidates is most likely the output concept: apple, honey or house. please choose one conept from the list of output concepts. "))
#print(ollama("Given the main concept 'food' and sub concepts 'animal', 'fly', 'yellow' and 'black' which of the following candidates is most likely the output concept: apple, honey or house. Please choose one conept from the list of output concepts and print in a json format. "))
#print(ollama("Given the main concept 'food' and sub concept 'animal' which of the following candidates is most likely the output concept: apple, honey or house. Please choose one conept from the list of output concepts and print in a json format."))

print(ollama('''Select the one element of this list that best fit a "Location,Country,Flag" which is "Water,Liquid,Aquatic" and "Huge,Wider,Longer":

Apple
Virus
Tiger
Taylor Swift
Galaxy
Star Wars
Bear
Asia
Pompeii
Batman
Mars
Plato
Ocean
Italy
Knife
Tsunami
Cleopatra
Eiffel Tower
Amsterdam
Bob Marley'''))