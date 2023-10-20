from flask import Flask, render_template, request
import time

app = Flask(__name__)

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if x <= pivot]
        greater = [x for x in arr[1:] if x > pivot]
        return quicksort(less) + [pivot] + quicksort(greater)

@app.route('/', methods=['GET', 'POST'])
def index():
    arraySortida = None
    tempoTomado = None

    if request.method == 'POST':
        input_array = request.form['input_array']
        try:
            input_array = [int(x) for x in input_array.split()]
            start_time = time.time()
            # time.sleep(1)  #-> Descomentar para testar tempo caso necessario sleep é para "dormir" o tempo para provar q existe a execução levando em cosideração q seu tempo é em segundos
            arraySortida = quicksort(input_array.copy())
            end_time = time.time()
            tempoTomado = (end_time - start_time) * 1000 # Convert to milliseconds
        except ValueError:
            # error_message = "Por favor, insira apenas números inteiros separados por espaços." #-> Não necessita pois existe validação no front para evitar esse problema
            # return render_template('index.html', error_message=error_message) #-> Mesma coisa pra linha de cima
            return render_template('index.html')

    return render_template('index.html', arraySortida=arraySortida, tempoTomado=tempoTomado)

if __name__ == '__main__':
    app.run(debug=True)
