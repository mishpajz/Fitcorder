from flask import Flask, render_template, request
from flask_table import Table, Col
from markupsafe import Markup, escape
import scheduling
import threading

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


@app.route('/T9-155/', methods=['GET', 'POST'])
@app.route('/T9-105/', methods=['GET', 'POST'])
@app.route('/T9-107/', methods=['GET', 'POST'])
def timetable():
    route_name = request.url_rule.rule[1:-1]
    
    if request.method == "GET":
        # Set initial values for checkboxes

        data = scheduling.load_data(route_name)
        if not data: # check if data is empty
            data = {} # create an empty dictionary

        items = []

        for i in range(8):  
            items.append(dict(time=scheduling.times[i], 
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
        scheduling.store_data(data, route_name)
        scheduling.add_jobs(route_name)
        return "Done"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/clear-all/<target>', methods=['POST'])
def clear_all():
    print(target)

if __name__ == '__main__':
    
    for key in scheduling.schedules:
        scheduling.schedules[key].start()
        scheduling.add_jobs(key)

    app.run(debug=True)