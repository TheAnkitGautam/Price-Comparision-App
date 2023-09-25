import flask
app = flask.Flask(__name__)
import sqlite3
conn=sqlite3.connect('laptop.db',check_same_thread=False)
c=conn.cursor()
row = None
@app.route("/")
def home():
    return flask.render_template('index.html')

@app.route('/1', methods = ('GET','POST'))
def query1():
    if flask.request.method == 'POST':
        model_id = flask.request.form['model']
        print(type(model_id))
        mod=(model_id,)
        c.execute('select * from product where model_number==?', mod)
        ans=c.fetchall()
        if len(ans)==0:
            return 'model_id not present in the data base we will work on it'
        if ans[0][1]>ans[0][3]:
            price=ans[0][3]
            link=ans[0][4]
        else :
            price=ans[0][1]
            link=ans[0][2]
        row = (price, link)
        return flask.render_template('queries/display1.html', name = row)
    return flask.render_template('queries/1.html')

@app.route('/2', methods = ('GET','POST'))
def query2():
    if flask.request.method == 'POST':
        low_price = flask.request.form['low']
        high_price = flask.request.form['high']
        # print(low_price)
        # print(high_price)
        data=(low_price,low_price,high_price,high_price)
        c.execute('select * from product where (amazon_price>=? or flipkart_price>=?) and (flipkart_price<=? or amazon_price<=?)', data)
        rows=c.fetchall()
        # print(rows)
        if len(rows)==0:
            return 'no laptops in given range'
        return flask.render_template('queries/display2.html',names=rows)
    return flask.render_template('queries/2.html')
@app.route('/3', methods = ('GET','POST'))
def query3():
    return 'under development'

if __name__== '__main__':
    app.run(debug=True)




