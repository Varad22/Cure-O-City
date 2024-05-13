from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import re
import pickle
from flask_mysqldb import MySQL
import MySQLdb.cursors
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os 
from datetime import date
from werkzeug.utils import secure_filename
import pandas as pd

genfeats=['abdominal cramp',
 'abdominal distention',
 'abnormal behavior',
 'abnormal bleeding',
 'abnormal sensation',
 'abnormally frequent',
 'abscess',
 'aching',
 'acne',
 'acquiring drinking alcohol taking lot time',
 'affected part turning white',
 'anemia',
 'arm',
 'attack pain',
 'bacterial infection',
 'bad breath',
 'bad smelling thin vaginal discharge',
 'bad smelling vaginal discharge',
 'barky cough',
 'belching',
 'better sitting worse lying',
 'birth baby younger week gestational age',
 'bleeding gum',
 'bleeding skin',
 'blindness',
 'blindness one eye',
 'blister sunlight',
 'bloating',
 'blood stool',
 'blood urine',
 'bloody diarrhea',
 'blue',
 'bluish skin coloration',
 'blurred vision',
 'blurry vision',
 'body tremor',
 'bone pain',
 'bowed leg',
 'breathing problem',
 'bruising',
 'burning',
 'burning stabbing pain',
 'burning urination',
 'certain thought repeatedly',
 'change bowel movement',
 'change breast shape',
 'change color',
 'change hair',
 'change reflex',
 'change skin color red black',
 'change sleeping eating pattern',
 'change taste',
 'change voice',
 'characteristic facial feature',
 'characteristic rash',
 'chest discomfort',
 'chest pain',
 'chest tightness',
 'chill',
 'chronic cough',
 'chronic pain bladder',
 'clenched fist overlapping finger',
 'clumsy',
 'cm lump skin',
 'cold sweat',
 'coma',
 'confused thinking',
 'confusion',
 'constipation',
 'coolness',
 'coordination',
 'cough bloody mucus',
 'cough sputum production',
 'coughing',
 'coughing blood',
 'coughing including coughing blood',
 'coughing mucus',
 'crawl',
 'cry episode',
 'dark urine',
 'darker',
 'daytime sleepiness',
 'death child le one year age',
 'decreased ability feel pain',
 'decreased ability see',
 'decreased ability think',
 'decreased ability think remember',
 'decreased ability turn',
 'decreased appetite',
 'decreased motivation',
 'decreased range motion',
 'decreased taste',
 'decreased vision',
 'dehydration',
 'delayed physical growth',
 'delirium',
 'delusion',
 'dementia',
 'depending subtype abdominal pain',
 'depends organ involved',
 'depressed mood',
 'dermatitis herpetiformis',
 'developmental disability',
 'diarrhea',
 'diarrhea may bloody',
 'diarrhea mixed blood',
 'diarrhoea',
 'difficulty breathing',
 'difficulty cutting',
 'difficulty eating',
 'difficulty getting pregnant',
 'difficulty remembering recent event',
 'difficulty swallowing',
 'difficulty walking',
 'dimpling skin',
 'discharge penis',
 'disorientation',
 'distant object appear blurry',
 'distorted blurred vision distance',
 'dizziness',
 'double vision',
 'drinking large amount alcohol long period',
 'dry cough',
 'dry damp skin',
 'dry eye',
 'dry mouth',
 'ear pain',
 'easy prolonged bleeding',
 'emotional problem',
 'enlarged lymph node neck',
 'enlarged spleen',
 'enlarged thyroid',
 'enlargement thyroid',
 'enlargement tonsil',
 'episode severe',
 'erythema marginatum',
 'excess hair',
 'excessive amount uterine bleeding',
 'excessive daytime sleepiness',
 'excessive salivation',
 'expanding area redness site tick bite',
 'extreme sadness',
 'extremity weakness',
 'eye pain',
 'eye strain',
 'eyestrain',
 'fast heart rate',
 'fast heartbeat',
 'fatigue',
 'fear water',
 'feel need check thing repeatedly',
 'feeling cold',
 'feeling faint upon standing',
 'feeling generally unwell',
 'feeling like passing',
 'feeling need urinate right away',
 'feeling tired',
 'feeling tired time',
 'fever',
 'firm',
 'flat discolored spot bump may blister',
 'flu like illness',
 'flu like symptom',
 'fluid filled blister scab',
 'fluid nipple',
 'frequent infection',
 'frequent urination',
 'gas',
 'gradual loss coordination',
 'growth delay',
 'gum disease',
 'hair loss',
 'half ring finger',
 'hallucination usually hearing voice',
 'hard swelling skin',
 'hard time reading small print',
 'headache',
 'hearing loss',
 'hearing sound external sound present',
 'heartburn',
 'heat intolerance',
 'heavy period',
 'high blood pressure',
 'high body temperature',
 'hoarse voice',
 'hold reading material farther away',
 'inability child',
 'inability move feel one side body',
 'increased breath rate',
 'increased fat',
 'increased heart rate',
 'increased hunger',
 'increased risk broken bone',
 'increased risk infection',
 'increased thirst',
 'increasing weakening',
 'index',
 'infertility',
 'inflamed eye',
 'insomnia',
 'intellectual disability',
 'involuntary muscle movement',
 'involuntary sleep episode',
 'irregular edge',
 'irregular menstruation',
 'irritability',
 'irritation',
 'itchiness',
 'itching',
 'itching genital area',
 'itching result trouble sleeping',
 'itchy',
 'itchy blister',
 'itchy bump',
 'itchy ear',
 'jaundice',
 'jaw',
 'jerky body movement',
 'joint bone pain',
 'joint swelling',
 'large amount watery diarrhea',
 'large forehead',
 'large lymph node',
 'large lymph node around neck',
 'leg swelling',
 'light sensitivity',
 'little pain',
 'localized breast pain redness',
 'long term fatigue',
 'loose frequent bowel movement',
 'loose teeth',
 'loss appetite',
 'loss consciousness may sweating',
 'loss hair part head body',
 'loss lot blood childbirth',
 'loss smell',
 'loss vision one side',
 'low blood pressure',
 'low energy',
 'low red blood cell',
 'lower abdominal pain',
 'lump breast',
 'lump bump neck',
 'maculopapular rash',
 'malabsorption',
 'may symptom',
 'memory problem',
 'mental ability',
 'mental change',
 'mid dilated pupil',
 'middle finger',
 'mild moderate intellectual disability',
 'minimal',
 'missed period',
 'mole increasing size',
 'mood change',
 'mood swing',
 'mouth sore',
 'mouth ulcer',
 'multiple painful joint',
 'muscle ache difficulty breathing',
 'muscle cramp',
 'muscle joint pain',
 'muscle spasm',
 'muscle weakness',
 'muscle weakness beginning foot hand',
 'muscle weakness resulting inability move',
 'muscular pain',
 'myalgia',
 'nausea',
 'nausea vomiting',
 'nausea vomiting weight loss dehydration occur',
 'nearly undetectable spell',
 'neck',
 'neck stiffness',
 'needing urinate often',
 'newly inverted nipple',
 'non itchy skin ulcer',
 'non painful cyst middle eyelid',
 'nonaligned eye',
 'none non specific',
 'numbness',
 'object different size eye',
 'one eye myopia eye hyperopia',
 'opening upper lip may extend nose palate',
 'overlying redness',
 'pain area',
 'pain around ear',
 'pain doesnt go shingle',
 'pain sex',
 'pain specific bone',
 'painful',
 'painful blister lower leg',
 'painful heavy period',
 'painful joint base big toe',
 'painful rash occurring stripe',
 'painful skin',
 'painful swelling parotid gland',
 'painful swollen joint',
 'painful tender outer part elbow',
 'painless',
 'painless lump',
 'pale color',
 'pale skin',
 'pallor',
 'paralysis',
 'patch thick',
 'patch white skin',
 'perform certain routine repeatedly',
 'period vigorous shaking',
 'persistent rough white red patch mouth lasting longer week',
 'photophobia',
 'physical disability',
 'pimple like rash',
 'pinkish',
 'playing video game extremely long period time',
 'poor ability tolerate cold',
 'poor coordination',
 'poor tolerance heat',
 'post nasal drip',
 'problem language',
 'problem understanding speaking',
 'problem vision',
 'profuse sweating',
 'progressive muscle weakness',
 'prolonged',
 'prolonged cough',
 'prominent',
 'protein urine',
 'psychosis',
 'pulsing pain',
 'purple colored skin affected area',
 'purple colored skin lesion',
 'raised',
 'raised red blue lesion',
 'random outburst laughter',
 'rapid breathing',
 'recurring episode wheezing',
 'red',
 'red eye',
 'red purple darker skin',
 'red rash',
 'red scaly patch skin breast',
 'red skin',
 'red spot white eye',
 'red without blister',
 'reddish eye',
 'redness',
 'redness eye',
 'repetitive behavior',
 'restricted interest',
 'right lower abdominal pain',
 'rigidity',
 'ringing ear heartbeat',
 'rough skin growth',
 'runny nose',
 'scaly patch skin',
 'scratchiness',
 'seizure',
 'sensitivity smell',
 'sensitivity sound',
 'severe intellectual disability',
 'severe pain',
 'severe pain lower back abdomen',
 'shakiness',
 'shaking',
 'sharp chest pain',
 'shivering',
 'shock like pain one side face last second minute',
 'short height',
 'short stature',
 'shortness breath',
 'sit',
 'skin blister',
 'skin breakdown',
 'skin lesion generally pink color project outward',
 'skin peeling',
 'sleep problem',
 'sleeping problem',
 'small blister break open form painful ulcer',
 'small blister surrounding swelling',
 'small face',
 'small head',
 'small jaw',
 'sneezing',
 'social withdrawal',
 'sometimes symptom',
 'sore arm leg',
 'sore throat',
 'sore wrist',
 'stiff muscle',
 'stiff neck',
 'stiffness',
 'stomach pain',
 'stroke',
 'sudden',
 'sudden loss muscle strength',
 'sweat',
 'swell pain near tumor',
 'swelling',
 'swelling abdomen',
 'swelling hand foot',
 'swollen',
 'swollen hand foot',
 'swollen lymph node',
 'taste acid',
 'temporary fleeting vision one eye',
 'tender breast',
 'testicular pain',
 'tingling',
 'tingling hand foot',
 'tiredness',
 'tooth loss',
 'triangular tissue growth cornea',
 'trouble breathing nose',
 'trouble coordination',
 'trouble opening mouth',
 'trouble seeing',
 'trouble sensation',
 'trouble sleeping',
 'trouble social interaction',
 'trouble speaking',
 'trouble swallowing',
 'trouble talking',
 'trouble walking',
 'ulcer',
 'ulcer around genitals',
 'ulceration',
 'unable move',
 'unexplained weight loss',
 'unintended weight loss',
 'unpleasant smell present breath',
 'upper abdominal pain',
 'usage resulting problem',
 'vaginal bleeding',
 'vaginal bleeding without pain',
 'vaginal discharge',
 'variable',
 'vary depending part brain involved',
 'varying degree muscle weakness',
 'velvety skin',
 'vision loss',
 'vomiting',
 'warm',
 'watery eye',
 'weak grip',
 'weak muscle',
 'weakness limb',
 'weakness numbness affected leg',
 'webbed neck',
 'weight gain',
 'wet',
 'wheezing',
 'white patch vaginal discharge',
 'widespread pain',
 'withdrawal occurring stopping',
 'worrying',
 'yellow skin',
 'yellowish coloration skin white eye',
 'yellowish skin',
 'yellowish skin crust']

data1=pd.read_csv('C:/Users/Isha Patel/OneDrive/Desktop/PROJECTS/Evathon/dis_sym_dataset_norm.csv')

import pickle
model = pickle.load(open('model.pkl','rb'))

import re
from googlesearch import search
import warnings
warnings.filterwarnings("ignore")
import requests
from bs4 import BeautifulSoup

# Take input a disease and return the content of wikipedia's infobox for that specific disease

def diseaseDetail(term):
    diseases=[term]
    ret=term+"\n"
    for dis in diseases:
        # search "disease wilipedia" on google 
        query = dis+' wikipedia'
        for sr in search(query,tld="co.in",stop=10,pause=0.5): 
            # open wikipedia link
            match=re.search(r'wikipedia',sr)
            filled = 0
            if match:
                wiki = requests.get(sr,verify=False)
                soup = BeautifulSoup(wiki.content, 'html5lib')
                # Fetch HTML code for 'infobox'
                info_table = soup.find("table", {"class":"infobox"})
                if info_table is not None:
                    # Preprocess contents of infobox
                    for row in info_table.find_all("tr"):
                        data=row.find("th",{"scope":"row"})
                        if data is not None:
                            symptom=str(row.find("td"))
                            symptom = symptom.replace('.','')
                            symptom = symptom.replace(';',',')
                            symptom = symptom.replace('<b>','<b> \n')
                            symptom=re.sub(r'<a.*?>','',symptom) # Remove hyperlink
                            symptom=re.sub(r'</a>','',symptom) # Remove hyperlink
                            symptom=re.sub(r'<[^<]+?>',' ',symptom) # All the tags
                            symptom=re.sub(r'\[.*\]','',symptom) # Remove citation text                     
                            symptom=symptom.replace("&gt",">")
                            ret+=data.get_text()+" - "+symptom+"\n"
#                            print(data.get_text(),"-",symptom)
                            filled = 1
                if filled:
                    break
    return ret


UPLOAD_FOLDER = 'C:/Users/Isha Patel/OneDrive/Desktop/PROJECTS/Evathon/evathon/static/img/uploads' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER     

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Cureocity'

mysql = MySQL(app)
app.secret_key = 'key12'

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/UserRegister", methods=['GET', 'POST'])
def UserRegister():
    msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'FullName' in request.form and 'Password' in request.form and 'Weight' in request.form and 'Gender' in request.form and 'Height' in request.form and 'Address' in request.form and 'Contact' in request.form :
        # Create variables for easy access
        Username = request.form['Username']
        FullName = request.form['FullName']
        Password = request.form['Password']
        Weight = request.form['Weight']
        Gender = request.form['Gender']
        Height = request.form['Height']
        Address = request.form['Address']
        Contact = request.form['Contact']
        Allergies = request.form['Allergies']
        MedConditions = request.form['MedConditions']
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_details WHERE Username = %s AND Password=%s', [Username, Password])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
            
    
        elif not re.match(r'[A-Za-z0-9]+', Username):
            msg = 'Username must contain only characters and numbers!'
            
        elif not Username or not Password:
            msg = 'Please fill out the form!'
            
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO user_details VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', [Username,FullName, Password,Weight, Gender, Height,Address,Contact,Allergies,MedConditions])
            mysql.connection.commit()
            msg = 'Successfully registered! Please Log-In'
            
            return redirect(url_for('login'))
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template("UserRegister.html", msg=msg)

@app.route("/DoctorRegister", methods=['GET', 'POST'])
def DoctorRegister():
    msg=''
    if request.method == 'POST' and 'Username' in request.form and 'FullName' in request.form and 'Password' in request.form and 'Specialization' in request.form and 'Gender' in request.form and 'WExp' in request.form and 'Contact' in request.form :
        # Create variables for easy access
        Username = request.form['Username']
        Password = request.form['Password']
        FullName = request.form['FullName']
        Specialization = request.form['Specialization']
        Gender = request.form['Gender']
        WExp = request.form['WExp']        
        Hospital = request.form['Hospital']
        HospAdd = request.form['HospAdd']
        HospContact = request.form['HospContact']
        Contact = request.form['Contact']
        Day = request.form['Day']
        Whrs = request.form['Whrs']
        
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doc_details WHERE Username = %s AND Password=%s', [Username, Password])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'      
        elif not re.match(r'[A-Za-z0-9]+', Username):
            msg = 'Username must contain only characters and numbers!'            
        elif not Username or not Password:
            msg = 'Please fill out the form!'            
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM hospitals WHERE hosp_name=%s', [Hospital])
            hospt = cursor.fetchone()
            
            if hospt:
                cursor.execute('SELECT hosp_id FROM hospitals WHERE hosp_name=%s', [Hospital])
                hospt_id = cursor.fetchone()
                print(hospt_id)
                cursor.execute('INSERT INTO doctors (hosp_id,Doctor) VALUES(%s,%s)', (hospt_id['hosp_id'], FullName))
                mysql.connection.commit()
            else:
                cursor.execute('INSERT INTO hospitals (hosp_name) VALUES(%s)', [Hospital])
                mysql.connection.commit()
                cursor.execute('SELECT hosp_id FROM hospitals WHERE hosp_name=%s', [Hospital])
                hospt_id = cursor.fetchone()
                cursor.execute('INSERT INTO doctors (hosp_id,Doctor) VALUES(%s,%s)', (hospt_id['hosp_id'], FullName))
                mysql.connection.commit()

            cursor.execute('INSERT INTO doc_details VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (Username, FullName,Password,Specialization,Gender,WExp,Contact,Hospital,HospAdd,HospContact,Day,Whrs))
            mysql.connection.commit()
            msg = 'Successfully registered! Please Log-In'

            
            
            return redirect(url_for('login'))
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template("DoctorRegister.html", msg=msg)

@app.route("/login", methods=['GET', 'POST'])
def login():
    msg=''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        print('111111111')
        Username = request.form['Username']
        Password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_details WHERE Username=%s AND Password=%s',[Username, Password])
        user = cursor.fetchone()
        cursor.execute('SELECT * FROM doc_details WHERE Username=%s AND Password=%s', [Username, Password])
        # Fetch one record and return result
        doc = cursor.fetchone()
        print(doc, user)
            # print("gg")
        # Create variables for easy access
        
       
        # If account exists in accounts table in out database
        if user==None and doc==None:
            msg = 'Incorrect Username or Password'
            # return redirect(url_for('login',msg=msg))   
        elif user!=None and doc==None:
            session['loggedin'] = True
            session['Username'] = user['Username']
            return redirect(url_for('UserHome'))
        elif doc!=None and user==None:
            session['loggedin'] = True
            session['Username'] = doc['Username']
            session['FullName'] = doc['FullName']
            return redirect(url_for('DocHome'))

    
    return render_template('login.html', msg=msg)   


@app.route("/UserHome", methods=['GET', 'POST'])
def UserHome():
    return render_template("UserHome.html")

@app.route("/UserProfile", methods=['GET', 'POST'])
def UserProfile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user_details WHERE Username=%s ',[session['Username']])
    user = cursor.fetchone()
    return render_template("UserProfile.html",user=user)

@app.route("/UpdateUserProfile", methods=['GET', 'POST'])
def UpdateUserProfile():
    if request.method == 'POST':
        Weight = request.form['Weight']
        Height = request.form['Height']
        Address = request.form['Address']
        Contact = request.form['Contact']
        Allergies = request.form['Allergies']
        MedConditions = request.form['MedConditions']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)        
        if Weight:
            cursor.execute('UPDATE user_details SET Weight = %s WHERE Username=%s', (Weight,session['Username']))
            mysql.connection.commit()
        if Height:
            cursor.execute('UPDATE user_details SET Height = %s WHERE Username=%s', (Height,session['Username']))
            mysql.connection.commit()
        if Address:
            cursor.execute('UPDATE user_details SET Address = %s WHERE Username=%s', (Address,session['Username']))
            mysql.connection.commit()
        if Contact:
            cursor.execute('UPDATE user_details SET Contact = %s WHERE Username=%s', (Contact,session['Username']))
            mysql.connection.commit()
        if Allergies:
            cursor.execute('UPDATE user_details SET Allergies = %s WHERE Username=%s', (Allergies,session['Username']))
            mysql.connection.commit()
        if MedConditions:
            cursor.execute('UPDATE user_details SET MedConditions = %s WHERE Username=%s', (MedConditions,session['Username']))
            mysql.connection.commit()

    return render_template("UpdateUserProfile.html")

@app.route("/Diagnosis/<topk_sorted>", methods=['GET', 'POST'])
def Diagnosis(topk_sorted):
    print(type(topk_sorted))
    
    topk_sorted = topk_sorted.replace('{','')
    topk_sorted = topk_sorted.replace('}','')
    topk_sorted = topk_sorted.replace(':',',')
    topk_sorted = topk_sorted.split(',')
    print(topk_sorted)
    display=[]
    prob=[]
    for i,j in enumerate(topk_sorted):
        if i%2==0:
            display.append(data1['label_dis'][int(j)]) 
        else:
            prob.append(float(j)*100)
    if topk_sorted=='UserHome':
        return redirect(url_for('UserHome'))
    return render_template("Diagnosis.html", details=zip(prob, display))

@app.route("/Symptoms", methods=['GET', 'POST'])
def Symptoms():
    symptoms =[]
    if request.method=='POST':
        if 'sym' in request.form:
            symptoms.append(request.form['sym'])
        if 'sym2' in request.form:
            symptoms.append(request.form['sym2'])
        if 'sym3' in request.form:
            symptoms.append(request.form['sym3'])
        if 'sym4' in request.form:
            symptoms.append(request.form['sym4'])
        if 'sym5' in request.form:
            symptoms.append(request.form['sym5'])
        if 'sym6' in request.form:
            symptoms.append(request.form['sym6'])

        data = pd.read_csv('C:/Users/Isha Patel/OneDrive/Desktop/PROJECTS/Evathon/dis_sym_dataset_comb.csv')
        data1 = pd.read_csv('C:/Users/Isha Patel/OneDrive/Desktop/PROJECTS/Evathon/dis_sym_dataset_norm.csv')
        y_new = data['label_dis']
        X_new = data.iloc[:,1:]
        
        for i in X_new.columns:
            if i not in genfeats:    
                X_new.drop(i, axis='columns', inplace=True)
                data1.drop(i, axis='columns', inplace=True)

        v=symptoms
        dis_list = set()
        final_symp = [] 
        counter_list = []
        for idx in v:
            if idx in data1.columns:
                symp=idx    
                final_symp.append(symp)
                dis_list.update(set(data1[data1[symp]==1]['label_dis']))
        
        
        for dis in dis_list:
            row = data1.loc[data1['label_dis'] == dis].values.tolist()        
            row[0].pop(0)        
            for idx,val in enumerate(row[0]):
               
                if val!=0 and genfeats[idx] not in final_symp:
                    counter_list.append(genfeats[idx])

        from collections import Counter
        import operator
        dict_symp = dict(Counter(counter_list))
        
        dict_symp_tup = sorted(dict_symp.items(), key=operator.itemgetter(1),reverse=True)
         

        return redirect(url_for('Symptoms2',dict_symp_tup=dict_symp_tup,final_symp=final_symp))


    return render_template("Symptoms.html",var=genfeats)

@app.route("/Symptoms2/<dict_symp_tup>/<final_symp>", methods=['GET', 'POST'])
def Symptoms2(dict_symp_tup, final_symp):   
    found_symptoms=[]
    count=0
    dict_symp_tup = dict_symp_tup.replace('(','')
    dict_symp_tup = dict_symp_tup.replace(')','')
    dict_symp_tup = dict_symp_tup.replace('[','')
    dict_symp_tup = dict_symp_tup.replace(']','')
    dict_symp_tup = dict_symp_tup.replace("'",'')       
    dict_symp_tup = dict_symp_tup.split(',')

    final_symp = final_symp.replace('[','')
    final_symp = final_symp.replace("'",'')
    final_symp = final_symp.replace(']','')
    final_symp = final_symp.split(',')

    for i in dict_symp_tup:
            if len(i)<=3:
                dict_symp_tup.remove(i)
    print(dict_symp_tup)
    if request.method=='POST':
        for i in dict_symp_tup:
            if i in request.form:
               final_symp.append(i) 
        found_symptoms = [] 
        
        

        data = pd.read_csv('C:/Users/Isha Patel/OneDrive/Desktop/PROJECTS/Evathon/dis_sym_dataset_comb.csv')
        data1 = pd.read_csv('C:/Users/Isha Patel/OneDrive/Desktop/PROJECTS/Evathon/dis_sym_dataset_norm.csv')
        y_new = data['label_dis']
        X_new = data.iloc[:,1:]
        
        for i in X_new.columns:
            if i not in genfeats:    
                X_new.drop(i, axis='columns', inplace=True)
                data1.drop(i, axis='columns', inplace=True)


        
        
    
        for tup in dict_symp_tup:
            count+=1
            found_symptoms.append(tup)
            if count%5==0 or count==len(dict_symp_tup):
                # print("\nCommon co-occuring symptoms:")
                for idx,ele in enumerate(found_symptoms):
                    pass
        

            sample_x = [0 for x in range(0,len(genfeats))]
            
            for val in final_symp:
                if val in genfeats:
                    
                    sample_x[genfeats.index(val)]=1        

            prediction = model.predict_proba([sample_x])
            k = 10
            diseases = list(set(data1['label_dis']))
            diseases.sort()
            topk = prediction[0].argsort()[-k:][::-1]

            from statistics import mean
            topk_dict = {}
            for idx,t in  enumerate(topk):
                match_sym=set()
                row = data1.loc[data1['label_dis'] == diseases[t]].values.tolist()
                row[0].pop(0)

                for idx,val in enumerate(row[0]):
                    if val!=0:
                        match_sym.add(genfeats[idx])
                prob = (len(match_sym.intersection(set(final_symp)))+1)/(len(set(final_symp))+1)
                prob *= 0.876627051499717
                topk_dict[t] = prob
            print(topk_dict)
            j = 0
            topk_index_mapping = {}
            topk_sorted = dict(sorted(topk_dict.items(), key=lambda kv: kv[1], reverse=True))
            print('llllllllllllllllllll')
            print(topk_sorted)
            return redirect(url_for('Diagnosis',topk_sorted=topk_sorted))
    # if len(topk_sorted)

    

    # select = input("\nMore details about the disease? Enter index of disease or '-1' to discontinue and close the system:\n")
    # if select!='-1':
    #     dis=diseases[topk_index_mapping[int(select)]]
        
    #     print(diseaseDetail(dis))
    # return redirect(url_for('Diagnosis', details=diseaseDetail(dis)))

    return render_template("Symptoms2.html", dict_symp_tup=dict_symp_tup)

# @app.route("/BookAppointment", methods=['GET', 'POST'])
# def BookAppointment():
   
    # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute('SELECT FullName,Hospital,Specialization FROM doc_details')
    # lst = cursor.fetchall()
    # print(lst)
    
    # doctors=[]
    # spcz=[]
    # hosp=[]
    # for i in doctors:
    #     spcz.append(i['Specialization'])
    #     hosp.append(i['Hospital'])
    #     doctors.append(i['FullName'])
    # data={}
    # data2={}        

    # if request.method == 'POST' and 'Specialization' in request.form and 'Mode' in request.form and 'Doctor' in request.form and 'Date' in request.form and 'Time' in request.form and 'Hospital' in request.form:        
    #     Specialization = request.form['Specialization']
    #     Mode = request.form['Mode']
    #     Doctor = request.form['Doctor']
    #     Date = request.form['Date']
    #     Time = request.form['Time']
    #     Patient = session['Username']
    #     Hospital = session['Hospital']

    #     if Mode=='Online':
    #         PATH = "C:\Program Files (x86)\chromedriver.exe"
    #         driver = webdriver.Chrome(PATH)
    #         driver.get("https://talky.io/")
    #         button = driver.find_element_by_class_name("create-room-form-button")
    #         button.click()
    #         link=driver.current_url
    #         driver.quit()
    #         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #         cursor.execute('INSERT INTO appointments VALUES(%s,%s,%s,%s,%s,%s,%s)',[Patient, Specialization, Mode, Doctor, Date, Time,link])
    #         mysql.connection.commit()

    #     else:
    #         link=''
    #         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #         cursor.execute('INSERT INTO appointments VALUES(%s,%s,%s,%s,%s,%s,%s)',[Patient, Specialization, Mode, Doctor, Date, Time,link])
    #         mysql.connection.commit()       
                   
        
    # return render_template("BookAppointment.html", doctors=doctors)

@app.route('/BookAppointment', methods=['POST', 'GET'])
def BookAppointment():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM hospitals ORDER BY hosp_id")
    carbrands = cur.fetchall()
    print(carbrands)
    if request.method == 'POST' and 'Mode' in request.form and 'Doctor' in request.form and 'Date' in request.form and 'Time' in request.form and 'Hospital' in request.form:        
        
        Mode = request.form['Mode']
        Doctor = request.form['Doctor']
        Date = request.form['Date']
        Time = request.form['Time']
        Patient = session['Username']
        Hospital = request.form['Hospital']
        print(Doctor)
        hosp_name=''
        dc_name=''
        if Mode=='Online':
            
            PATH = "C:\Program Files (x86)\chromedriver.exe"
            driver = webdriver.Chrome(PATH)
            driver.get("https://talky.io/")
            button = driver.find_element_by_class_name("create-room-form-button")
            button.click()
            link=driver.current_url
            driver.quit()
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute('SELECT Doctor FROM doctors WHERE dc_id=%s', [Doctor])
            var = cursor.fetchone()
            cursor.execute('SELECT hosp_name FROM hospitals WHERE hosp_id=%s', [Hospital])
            hvar = cursor.fetchone()

            cursor.execute('INSERT INTO appointments VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',[Patient, Mode, Doctor, Hospital, hvar['hosp_name'], var['Doctor'], Date, Time,link])
            mysql.connection.commit()
            
            
            
        else:
            link=''
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT Doctor FROM doctors WHERE dc_id=%s', [Doctor])
            var = cursor.fetchone()
            cursor.execute('SELECT hosp_name FROM hospitals WHERE hosp_id=%s', [Hospital])
            hvar = cursor.fetchone()
            # print(var, hvar)
            cursor.execute('INSERT INTO appointments VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',[Patient, Mode, Doctor, Hospital, hvar['hosp_name'], var['Doctor'], Date, Time,link])
            mysql.connection.commit()     
                   
    return render_template('BookAppointment.html', carbrands=carbrands)
 
@app.route("/carbrand",methods=["POST","GET"])
def carbrand():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        
        result = cur.execute("SELECT * FROM doctors WHERE hosp_id = %s ORDER BY Doctor ASC", [category_id] )
        carmodel = cur.fetchall()  
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'id': row['hosp_id'],
                'name': row['Doctor'],
                'dc_id':row['dc_id']}
            OutputArray.append(outputObj)
    
    return jsonify(OutputArray)

@app.route("/BookedAppointments", methods=['GET', 'POST'])
def BookedAppointments():
    # print(session['Username'])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM appointments WHERE Patient=%s', [session['Username']])
    user = cursor.fetchall()
    print(user)  
    
    return render_template("BookedAppointments.html", user=user)

@app.route("/Prescriptions", methods=['GET', 'POST'])
def Prescriptions():  
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM appointments WHERE Patient=%s AND Mode="Online"', [session['Username']])
    user = cursor.fetchall() 
    path1 = UPLOAD_FOLDER + '/' + session['Username']
    var = os.listdir(path1)
    print(var)
    name=session['Username']
    return render_template('Prescriptions.html', users=zip(user,var), name=name)

@app.route("/NearbyHospitals", methods=['GET', 'POST'])
def NearbyHospitals():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM doc_details ')
    details = cursor.fetchall()
    return render_template("NearbyHospitals.html",details=details)

@app.route("/Diagnosis/UserHome", methods=['GET', 'POST'])
def DHome():
    return render_template("UserHome.html")

# DOCTOR------------------------------------------

@app.route("/DocHome", methods=['GET', 'POST'])
def DocHome():
    return render_template("DocHome.html")

@app.route("/DocProfile", methods=['GET', 'POST'])
def DocProfile():
    return render_template("DocProfile.html")

@app.route("/DocsSchedule", methods=['GET', 'POST'])
def DocsSchedule():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM appointments WHERE dc_name=%s',[session['Username']])
    sch = cursor.fetchall()
    # cursor.execute('SELECT Doctor FROM doctors WHERE dc_id IN %s',[sch['Doctor']])
    # dc = cursor.fetchall()
    
        
    return render_template("DocsSchedule.html",sch=sch)

@app.route("/GivePrescription", methods=['GET', 'POST'])
def GivePrescription():
    msg=''
    print(session['Username'])
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM appointments WHERE dc_name=%s AND Mode="Online"',[session['Username']])
    details = cursor.fetchall()
    print(details)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            msg= 'No file part'
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            msg= 'No selected file'
        if file and allowed_file(file.filename):
            if request.form['Submit']:
                name=request.form.get('Submit')
            filename = secure_filename(file.filename)
            path1 = UPLOAD_FOLDER + '/' + name
            if os.path.isdir(path1):
                app.config['UPLOAD_FOLDER'] = path1
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                os.mkdir(path1)
                app.config['UPLOAD_FOLDER'] = path1
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            dir_list = os.listdir(path1)
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            d1=d1.split('/')
            d1='-'.join(d1)
            os.rename(path1+'/'+dir_list[-1], path1+'/'+d1+"."+filename.split('.')[-1])
            msg='Done'
    
    return render_template("GivePrescription.html", details=details, msg=msg)



@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('Username', None)
    return redirect(url_for('index'))

if __name__ =="__main__":
    app.run(debug=True)