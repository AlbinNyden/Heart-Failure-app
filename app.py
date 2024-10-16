import sys
import pickle as pkl
import pandas as pd
from PyQt5.QtWidgets import QLabel, QMainWindow, QWidget, QApplication, QVBoxLayout, QComboBox, QLineEdit, QPushButton
from PyQt5.QtGui import QPalette, QColor

##Load model
with open("./ML/model/heart_failure_model.pkl", "rb") as f:
    model = pkl.load(f)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Heart Failure Prediction")

        #Calculate Button
        calculate = QPushButton("Calculate Heart Failure Probability")
        calculate.setCheckable(False)
        calculate.clicked.connect(self.get_model_result)

        #Layout
        layout = QVBoxLayout()

        #Age widget
        self.age = QLineEdit()
        self.age.setMaxLength(2)
        self.age.setPlaceholderText("Enter your age")

        #Gender widget
        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female"])

        #Chest Pain
        self.chest_pain = QComboBox()
        self.chest_pain.addItems(["TA", "ATA", "NAP", "ASY"])

        #Resting BP
        self.resting_bp = QLineEdit()
        self.resting_bp.setMaxLength(4)
        self.resting_bp.setPlaceholderText("Enter your Resting Blood Pressure")

        #Cholesterol
        self.cholesterol = QLineEdit()
        self.cholesterol.setMaxLength(4)
        self.cholesterol.setPlaceholderText("Enter your Cholesterol")

        #Fasting BP
        self.fasting_bp = QLineEdit()
        self.fasting_bp.setMaxLength(4)
        self.fasting_bp.setPlaceholderText("Enter your Fasting Blood Sugar")

        #Resting ECG
        self.resting_ecg = QComboBox()
        self.resting_ecg.addItems(["Normal", "ST", "LVH"])

        #Max Heart Rate
        self.max_heartrate = QLineEdit()
        self.max_heartrate.setMaxLength(4)
        self.max_heartrate.setPlaceholderText("Enter Max Heart Rate")

        #Excersie Angina
        self.exercise_angina = QComboBox()
        self.exercise_angina.addItems(["No", "Yes"])

        #Oldspeak
        self.oldspeak = QLineEdit()
        self.oldspeak.setMaxLength(2)
        self.oldspeak.setPlaceholderText("Enter Oldspeak")

        #ST Slope
        self.st_slope = QComboBox()
        self.st_slope.addItems(["Flat", "Up", "Down"])

        #Model Result
        self.result = QLabel("")
        
        

        #Add widgets
        layout.addWidget(self.age)
        layout.addWidget(self.gender)
        layout.addWidget(self.chest_pain)
        layout.addWidget(self.resting_bp)
        layout.addWidget(self.cholesterol)
        layout.addWidget(self.fasting_bp)
        layout.addWidget(self.resting_ecg)
        layout.addWidget(self.max_heartrate)
        layout.addWidget(self.exercise_angina)
        layout.addWidget(self.oldspeak)
        layout.addWidget(self.st_slope)
        layout.addWidget(calculate)
        layout.addWidget(self.result)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

    #### Functions ####
    def get_model_result(self):
        input = pd.DataFrame([self.get_data()])
        model_result = model.predict_proba(input)[0][1]
        model_result = round(100*model_result,1)
        self.result.setText(f"Probability of Heart Failure: {model_result}%")

    def get_data(self):
        #Get the data from the widgets
        AGE = int(self.age.text())
        GENDER = int(self.gender.currentIndex())
        CHEST_PAIN = int(self.chest_pain.currentIndex())
        RESTING_BP = int(self.resting_bp.text())
        CHOLESTEROL = int(self.cholesterol.text())
        FASTING_BP = int(self.fasting_bp.text())
        if(FASTING_BP > 120):
            FASTING_BP = 1
        else:
            FASTING_BP = 0
        
        RESTING_ECG = int(self.resting_ecg.currentIndex())
        MAX_HEARTRATE = int(self.max_heartrate.text())
        EXERCISE_ANGINA = int(self.exercise_angina.currentIndex())
        OLDSPEAK = int(self.oldspeak.text())
        ST_SLOPE = int(self.st_slope.currentIndex())

        return(
            {"Age": AGE,
             "Sex": GENDER,
             "ChestPainType": CHEST_PAIN,
             "RestingBP": RESTING_BP,
             "Cholesterol": CHOLESTEROL,
             "FastingBS": FASTING_BP,
             "RestingECG": RESTING_ECG,
             "MaxHR": MAX_HEARTRATE,
             "ExerciseAngina": EXERCISE_ANGINA,
             "Oldpeak": OLDSPEAK,
             "ST_Slope": ST_SLOPE}
        )


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()