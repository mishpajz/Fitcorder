from flask import Flask, render_template, request
from flask_table import Table, Col
from markupsafe import Markup, escape
import pickle
import os

app = Flask(__name__)
app.url_map.strict_slashes = False

class CheckboxCol(Col):
    def td_format(self, content):

        markup = Markup('<input type="checkbox" name="{name}" value="{value}"'.format(
            name=escape(self.name),
            value=escape(content[0])
        ))

        if content[1]:
            markup += " checked"

        markup += " >"

        return markup
    
class TimeTable(Table):
    time = Col('Time')
    monday = CheckboxCol('mon', td_html_attrs={'class': 'checkbox'})
    tuesday = CheckboxCol('tue', td_html_attrs={'class': 'checkbox'})
    wednesday = CheckboxCol('wed', td_html_attrs={'class': 'checkbox'})
    thursday = CheckboxCol('thu', td_html_attrs={'class': 'checkbox'})
    friday = CheckboxCol('fri', td_html_attrs={'class': 'checkbox'})

def store_data(data, filename):
    # create a relative path to the config directory
    filepath = os.path.join("config", filename)
    try:
        # check if the config directory exists
        if not os.path.exists("config"):
            # create a new directory
            os.mkdir("config")
        # open the file for writing
        file = open(filepath, "wb")
        # write the dictionary to the file
        pickle.dump(data, file)
    except Exception as e:
        # handle any other exception
        print(f"An error occurred: {e}")
    finally:
        # close the file if it is opened
        if "file" in locals():
            file.close()

def load_data(filename):
    # create a relative path to the config directory
    filepath = os.path.join("config", filename)
    try:
        # open the file for reading
        file = open(filepath, "rb")
        # load the dictionary from the file
        data = pickle.load(file)
    except Exception as e:
        # handle any other exception
        print(f"An error occurred: {e}")
    finally:
        # close the file if it is opened
        if "file" in locals():
            file.close()
            return data


@app.route('/T9-155/', methods=['GET', 'POST'])
@app.route('/T9-105/', methods=['GET', 'POST'])
@app.route('/T9-107/', methods=['GET', 'POST'])
def timetable():
    route_name = request.url_rule.rule[1:-1]

    times = ['8:00', '9:40', '11:20', '13:00', '14:40', '16:20', '18:00', '19:40']
    
    if request.method == "GET":
        # Set initial values for checkboxes

        data = load_data(route_name)
        if not data: # check if data is empty
            data = {} # create an empty dictionary

        items = []

        for i in range(8):  
            items.append(dict(time=times[i], 
                      monday=(i, str(i) in data.get('mon', [])),
                      tuesday=(i, str(i) in data.get('tue', [])),
                      wednesday=(i, str(i) in data.get('wed', [])),
                      thursday=(i, str(i) in data.get('thu', [])),
                      friday=(i, str(i) in data.get('fri', []))
                      ))
        table = TimeTable(items)
        return render_template("timetable.html", table=table)
    
    elif request.method == "POST":
        # Get values of checkboxes
        data = request.form.to_dict(False)
        store_data(data, route_name);
        return "Saved!"

@app.route('/')
def index():

    return render_template("index.html")


if __name__ == '__main__':
   app.run(debug=True)