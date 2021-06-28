from flask import Flask, render_template, jsonify, request, redirect, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
from owlready2 import *

app = Flask(__name__)
CORS(app)
global onto_name
onto_name = ""
app.config["CARTELLA_FILE"] = os.path.abspath('../Sistema di raccomandazione/prototipi')
app.config["CARTELLA_ONTOLOGIE"] = "./Ontology"


class Property:
    name = ""
    num = 0
    percent = 0.0

    def __init__(self, name, num, percent):
        self.name = name
        self.num = num
        self.percent = percent


def allowed_file(filename, tfile):
    if not "." in filename:
        return True
    if tfile == "deno":
        ext = filename.rsplit(".", 1)[1]
        if ext.upper() in ["PNG", "DOC", "JPEG", "DOCX", "GIF", "JPG", "JAVA", "C", "XLSX"]:
            return False
        else:
            return True
    elif tfile == "onto":
        ext = filename.rsplit(".", 1)[1]
        if ext.upper() in ["OWL"]:
            return True
        else:
            return False


@app.route("/postfile", methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        if request.files:
            es_file = request.files['file']
            if not allowed_file(es_file.filename, "deno"):
                print("Formato del file non valido")
                return jsonify({'response': "formato non valido"})

            filename = secure_filename(es_file.filename)
            ex_path = os.path.abspath('../Sistema di raccomandazione')
            es_file.save(os.path.join(app.config["CARTELLA_FILE"], filename))
            os.system("cd " + ex_path + "& python Pozz.py prototipi/" + filename)

            print("file salvato " + filename)
    return jsonify({'response': filename})


@app.route("/getfile", methods=['GET'])
def getPrototipeFile():
    dir = './Results'
    for file in os.scandir(dir):
        os.remove(file.path)

    if request.method == 'GET':
        file_wanted = request.args.get("filename")
        getProperties(file_wanted)
        resp = send_file('./Results/' + file_wanted + "result")
        resp.headers["Cache-Control"] = "no-store"
        return resp


@app.route("/postOntology", methods=['POST', 'GET'])
def uploadOntology():
    dir = './Ontology'
    for file in os.scandir(dir):
        os.remove(file.path)

    if request.method == 'POST':
        if request.files:
            onto_file = request.files['file']

            if not allowed_file(onto_file.filename, "onto"):
                print("Formato del file non valido")
                return jsonify({'response': "Formato non valido"})

            else:
                global onto_name
                onto_name = secure_filename(onto_file.filename)
                onto_file.save(os.path.join(app.config["CARTELLA_ONTOLOGIE"], onto_name))
                onto = get_ontology("file://./Ontology/" + onto_name).load()

                lista = list(onto.classes())

                n = 0
                while n < len(lista):
                    lista[n] = str(lista[n])
                    n = n + 1
    return jsonify(lista)


@app.route("/getClasses", methods=['GET'])
def get_classes():
    if request.method == 'GET':
        class_wanted = request.args.get("classname")
        global onto_name
        onto = get_ontology("file://./Ontology/" + onto_name).load()

        output = list(onto[class_wanted].ancestors())

        n = 0

        while n < len(output):
            output[n] = str(output[n])
            n = n + 1

        output.remove('owl.Thing')

        for x in output:
            if x.rsplit(".", 1)[1] == class_wanted:
                output.remove(x)

    return jsonify(output)


@app.route("/postFileCreated", methods=['POST'])
def postFileCreated():
    if request.method == 'POST':
        if request.json:
            json_data = request.json  # file_wanted = request.args.get("filename") !!!!! forse
            head = json_data["head"]
            modifier = json_data["modifier"]
            headT = json_data["headT"]
            modifierT = json_data["modifierT"]
            nome = write_file(head, modifier, headT, modifierT)
        else:
            return jsonify({'response': "Impossibile creare il file"})
    return jsonify({'response': "File creato correttamente", 'name': str(nome)})


@app.route("/dowloadFile", methods=['GET'])
def dowload_file():
    if request.method == 'GET':
        file_wanted = request.args.get("filename")
        resp = send_file('../Sistema di raccomandazione/prototipi/' + str(file_wanted))
        resp.headers["Cache-Control"] = "no-store"
        return resp


def write_file(head, modifier, head_prop, modifier_prop):
    filename = head[0] + "_" + modifier[0]
    f = open("../Sistema di raccomandazione/prototipi/" + head[0] + "_" + modifier[0], "w")
    f.write("#Title composizione\n")
    f.write("Title : " + head[0] + "-" + modifier[0] + "\n\n")
    f.write("#Concetto Principale\n")
    f.write("Head Concept Name : " + head[0] + "\n\n")
    f.write("#Concetto Modificatore\n")
    f.write("Modifier Concept Name : " + modifier[0] + "\n\n")

    head.pop(0)
    for p in head:
        f.write("head, " + p + "\n")
    f.write("\n\n")

    modifier.pop(0)
    for p in modifier:
        f.write("modifier, " + p + "\n")
    f.write("\n\n")

    for i in modifier_prop:
        split = i.split(":")
        numero = float(split[1])
        num = str(format(numero, '.2f'))

        f.write("T(modifier), " + split[0] + ", " + num + "\n")
    f.write("\n")

    for i in head_prop:
        split = i.split(":")
        numero = float(split[1])
        num = str(format(numero, '.2f'))
        if (split[1] == '0'):
            split[1] = split[1] + '.00'
        f.write("T(head), " + split[0] + ", " + num + "\n")
    f.write("\n")
    f.close()
    return filename


def getProperties(filename):
    prop_list = []

    with open('../Sistema di raccomandazione/prototipi/' + filename) as f:
        input_lines = f.readlines()

    for p in input_lines:
        prop = p.split(', ')
        if prop[0] in ['T(modifier)', 'T(head)']:
            x = Property(prop[1], 0, prop[2])
            prop_list.append(x)

    result = None
    for g in input_lines:
        result = g.split('Result : ')

    if len(result) > 1:
        l = result[1].replace("'", '')
        res_val = l.split(", ")
        i = 0
        while i < len(res_val) - 1:
            prop_list[i].num = int(res_val[i])
            i = i + 1
            if len(prop_list) - 1 == i:
                i = i + 1
                c = res_val[i].split('\n')
                x = Property('', 0, float(c[0]))
                prop_list.append(x)

        newFile = open('./Results/' + filename + "result", "w")
        newFile.write("#The result of the elaboration of " + filename + " is :\n\n")
        for p in prop_list:
            if p.num == 1:
                newFile.write(p.name + ' : ' + str(p.percent) + "\n")
            elif p.name == '':
                newFile.write('Scenario with probability of : ' + str(p.percent) + "\n")

        newFile.close()
    else:
        newFile = open('./Results/' + filename + "result", "w")
        newFile.write("#NO recommended scenarios!")
        newFile.close()


if __name__ == "__main__":
    app.run()
