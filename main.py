from flask import Flask, render_template, request
from flask_table import Table, Col
from markupsafe import Markup, escape

app = Flask(__name__)

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

    times = ['8:00', '9:40', '11:20', '13:00', '14:40', '16:20', '18:00', '19:40']
    
    if request.method == "GET":
        # Set initial values for checkboxes
        items = []

        for i in range(8):  
            items.append(dict(time=times[i], 
                      monday=(i, False),
                      tuesday=(i, False),
                      wednesday=(i, True),
                      thursday=(i, False),
                      friday=(i, False)))
        table = TimeTable(items)
        return render_template("timetable.html", table=table)
    
    elif request.method == "POST":
        # Get values of checkboxes
        data = request.form.to_dict(False)
        print(request.url_rule)
        print(data) # You can do something with this data here
        return "You submitted the form."

@app.route('/')
def index():

    return render_template("index.html")


if __name__ == '__main__':
   app.run(debug=True)