import os
import string
from urllib.request import urlopen

from flask import Flask, render_template, request, url_for
from flask_cors import CORS, cross_origin




app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# solr = pysolr.Solr('http://localhost:8983/solr/fooddishes_shard1_replica_n1', always_commit=True)



@app.route("/", methods = ["GET","POST"])
@cross_origin()
def home():
  if request.method == 'POST':
    query_do = request.form['do_t']
    query_donot = request.form['donot_t']

    tokens_do = []
    tokenize(tokens_do, query_do)

    tokens_donot = []
    tokenize(tokens_donot, query_donot)
    query = "Ingredients:("
    for token in tokens_do:
      query += token + "+"

    for token in tokens_donot:
      query += "-" + token + "+"

    query += ")"
    print('http://localhost:8983/solr/food/select?q='+query+'&wt=python')
    connection = urlopen('http://localhost:8983/solr/food/select?q='+query+'&wt=python')
    response = eval(connection.read())
    #response = solr.search(query, **{'rows': 20, })




    total = response['response']['numFound']

    final_list = []
    for document in response['response']['docs']:
      temp = []
      temp.append(document['Title'])
      temp.append(document['Ingredients'])
      temp.append(document['Instructions'])
      image_path = "/data/" + document['Image_Name'] + '.jpg'
      temp.append(image_path)
      final_list.append(temp)


    return render_template("Retrieved_Documents.html", list=final_list, do = query_do , donot = query_donot, total = total)

  return render_template("search.html")


"""
    Function performs tokenization operation on given string or elementtree object by extracting words/nouns.
    :argument list - final list in which word needs to be added after operations
    :argument tag - string or elementtree object 
"""
def tokenize(list, tag):
    if tag != None:
        if type(tag) == str:
            for punctuation in string.punctuation:
                tag = tag.replace(punctuation, " ")
            items = tag.split()
            for item in items:
                formatWord(list, item)
        else:
            for sub in tag:
                text = sub.text
                if text != None:
                    for punctuation in string.punctuation:
                        text = text.replace(punctuation, " ")
                    items = text.split()
                    for item in items:
                        formatWord(list, item)

"""
    Function which performs format operations on word such as lowercase conversion, removes numbers and stopwords.
    :argument list - final list in which word needs to be added after operations
    :argument word - word that needs to be formatted
"""
def formatWord(list, word):

    word = word.lower().strip()
    for i in range(10):
        word = word.replace(str(i),'')

    if len(word) > 0:
        list.append(word)

if __name__ == "__main__":
    app.run(debug=True)

