import random
import pymorphy3
import re
from collections import defaultdict

# Инициализация лемматизатора
morph = pymorphy3.MorphAnalyzer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # Удаление всех чисел
    text = re.sub(r'[^\w\s]', '', text)  # Удаление знаков препинания
    return text

def lemmatize_text(text):
    words = text.split()
    lemmas = [morph.parse(word)[0].normal_form for word in words if word.strip()]
    return lemmas

def build_markov_chain(lemmas, n):
    markov_chain = defaultdict(list)
    for i in range(len(lemmas) - n):
        key = tuple(lemmas[i:i+n])
        next_word = lemmas[i+n]
        markov_chain[key].append(next_word)
    return markov_chain

def predict_next_word(lemmas, current_sequence):
    n = len(current_sequence)
    while n > 0:
            # Построение цепи Маркова
        chain = build_markov_chain(lemmas, n)
        #ключ - цепочка для которой требуется предсказание
        #значение по этому ключу - есть результат предсказания
        key = tuple(current_sequence[-n:])
        #идем по всем построенным цепочкам слов, и работаем только с той которая нам нужна
        if key in chain:
            #так как цепочек может быть несколько, мы просто выбираем случайную.
            return (random.choice(chain[key]), n)
        n -= 1
    return ("", "Подсказок нет")

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Считывание текста из файла
file_path = 'text.txt'
text = read_text_from_file(file_path)

# Предобработка текста
clean_text = preprocess_text(text)

# Лемматизация текста
lemmas = lemmatize_text(clean_text)


# Основной цикл ввода
print("Введите последовательность из нескольких слов:")
while True:
    user_input = input().strip()
    if not user_input:
        print("Пожалуйста, введите хотя бы одно слово.")
        continue
    
    # Предобработка и лемматизация введенной строки
    clean_input = preprocess_text(user_input)
    input_lemmas = lemmatize_text(clean_input)
    
    # Предсказание следующего слова
    next_word = predict_next_word(lemmas, input_lemmas)
    if (next_word[0] == ""):
        print(f"{next_word[1]}")
    else:
        print((f"Следующее слово: {next_word[0]}\nИз {len(input_lemmas)} слов использовано {next_word[1]} слов(а)\n"))