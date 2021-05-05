import sys
import os
import pickle
import datetime
import numpy as np
#import traceback

from PyQt5 import QtWidgets, QtCore
from Designs import mainWindow
from Windows import AppWindows
from Models import GuiModels
import Models.Experiment as Experiment
from Controllers import ExperimentControl
from PyPulse import PulseInterface
from HelperFunctions import Email as email


class MainApp(QtWidgets.QMainWindow, mainWindow.Ui_MainWindow):
    saved = QtCore.pyqtSignal()
    loaded = QtCore.pyqtSignal()
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.saved_status = True
        self.config_path = ".autonomouseconfig"
        
        # create config folder if not exists
        if not os.path.isdir(self.config_path):
            os.makedirs(self.config_path)
        
        self.hardware_prefs = self.load_config_data()
        self.hardware_window = AppWindows.HardwareWindow(self)
        self.animal_window = None
        self.analysis_window = None
        self.mail_window = None
        self.control_window = None
        self.setup_experiment_bindings(Experiment.Experiment())
        
        # function bindings
        self.actionAnimal_List.triggered.connect(self.open_animal_window)
        self.actionHardware_Preferences.triggered.connect(self.open_hardware_window)
        self.actionAnalyse_Experiment.triggered.connect(self.open_analysis_window)
        self.actionMailing_List.triggered.connect(self.open_mail_window)
        self.actionVideo_Control.triggered.connect(self.open_control_window)
        self.actionSave_Experiment.triggered.connect(self.save_experiment)
        self.actionLoad_Experiment.triggered.connect(self.load_experiment)
        self.saved.connect(self.experiment_saved)
        
    def setup_experiment_bindings(self, experiment):
        self.experiment = experiment
        
        if self.experiment.default_row.maxlen != Experiment.Experiment().default_row.maxlen:
            self.experiment.default_row = Experiment.Experiment().default_row.copy()
            temp = self.experiment.trials.copy()
            self.experiment.trials = self.experiment.default_row.copy()
            for row in temp:
                self.experiment.trials.append(row)
                
        self.experiment_control = ExperimentControl.ExperimentController(self)
        
        self.model = GuiModels.TableModel(['Animal ID', 'Time Stamp', 'Schedule Idx', 'Trial Idx', 'Odour', 'Delay', 'Rewarded',
                                           'Wait Response', 'Response', 'Correct', 'Timeout','Number of Licks'],
                                            self.experiment.trials, parent=self)

        self.trialView.setModel(self.model)

        try:
            self.startButton.disconnect()
            self.stopButton.disconnect()
        except:
            pass
        self.startButton.clicked.connect(self.experiment_control.start)
        self.stopButton.clicked.connect(self.experiment_control.stop)
        
        self.hardware_window.new_pref.connect(self.experiment_control.update_pref)
        
        self.experiment_control.trial_job.trial_end.connect(self.update_trial_view)
        self.experiment_control.trial_job.trial_end.connect(self.update_data_view)
        self.experiment_control.trial_job.trial_end.connect(self.status_changed)

        self.trialView.selectionModel().selectionChanged.connect(self.on_trial_selected)

    def load_config_data(self):
        hardware_config_path = self.config_path+"/hardware.config"
        if os.path.exists(hardware_config_path):
            with open(hardware_config_path, 'rb') as fn:
                return pickle.load(fn)
        else:
            return None

    def open_animal_window(self):
        self.animal_window = AppWindows.AnimalWindow(self)
        self.animal_window.changed.connect(self.status_changed)
        self.animal_window.show()

    def open_hardware_window(self):
        self.hardware_window.show()
        #hardware_window = AppWindows.HardwareWindow(self)
        #hardware_window.show()
    
    def open_control_window(self):
        self.control_window = AppWindows.ControlWindow(self.experiment, parent=self)
        self.control_window.show()
    
    def open_mail_window(self):
        self.mail_window = AppWindows.MailWindow(self)
        self.mail_window.show()

    def open_analysis_window(self):
        self.analysis_window = AppWindows.AnalysisWindow(self.experiment, parent=self)
        self.analysis_window.show()

    def update_trial_view(self):
        self.model.layoutChanged.emit()

    def update_data_view(self): #DONE thoraxView is obsolete. ACHTUNG: von GUI wegkommentieren!
        self.dataLView.plotItem.clear()
        self.dataRView.plotItem.clear()
        self.dataLView.plotItem.plot(np.arange(len(self.experiment.last_data_l)) / self.hardware_prefs['samp_rate'],
                                    np.array(self.experiment.last_data_l))
        self.dataRView.plotItem.plot(np.arange(len(self.experiment.last_data_r)) / self.hardware_prefs['samp_rate'], 
                                      np.array(self.experiment.last_data_r))
        self.dataLView.setYRange(0, 6)
        self.dataRView.setYRange(0, 6)

    def update_graphics_view(self, trial):
        animal = self.experiment.trials[trial][0]
        sched_idx = self.experiment.trials[trial][2]
        trial_idx = self.experiment.trials[trial][3]

        try:
            trial_data = self.experiment.animal_list[animal].schedule_list[sched_idx].trial_params[trial_idx]
    
            pulses, t = PulseInterface.make_pulse(self.hardware_prefs['samp_rate'], 0.0, 0.0, trial_data)
                
            onset = np.zeros(int(self.hardware_prefs['fv_delay']*self.hardware_prefs['samp_rate']))
            offset = np.zeros(int((self.hardware_prefs['lick_delay']+self.hardware_prefs['thorax_delay'])*self.hardware_prefs['samp_rate']))
            t = np.arange(len(onset)+len(offset)+len(t)) / self.hardware_prefs['samp_rate']
                
            self.graphicsView.plotItem.clear()
            for p, pulse in enumerate(pulses):
                self.graphicsView.plotItem.plot(t, np.hstack((onset,np.array(pulse),offset)) - (p * 1.1))
        except:
            pass

    def on_trial_selected(self):
        try:
            selected_trial = self.trialView.selectionModel().selectedRows()[0].row()
        except:
            selected_trial = 0
        self.update_graphics_view(selected_trial)

    def update_experiment_info(self):
        self.experimentNameLabel.setText(self.experiment.name)
        self.experimentDateLabel.setText(self.experiment.date)
        self.savePathLabel.setText(self.experiment.save_path)

    def save_experiment(self):
        try:
            #bit messy, what if the experiment class changes, should rather be saving the data in the class
            fname, suff = QtWidgets.QFileDialog.getSaveFileName(self, "Save Experiment", '', "AutonoMouse Experiment (*.autmaus)")
            tmpName = os.path.basename(fname)
            tmpSavePath = os.path.dirname(fname)
            self.experiment.name = tmpName
            self.experiment.save_path = tmpSavePath
            
            # We don't change the original date of creation
            if self.experiment.date is None:
                self.experiment.date = str(datetime.datetime.now())
                logs_path = os.path.dirname(fname)+ '/Logs/logs_' + self.experiment.name.split(".")[0]
                self.experiment.logs_path = logs_path
                if os.path.isdir(self.experiment.logs_path):
                    i = 1
                    while os.path.isdir(self.experiment.logs_path):
                        self.experiment.logs_path = logs_path +'('+str(i)+')'
                        i += 1
                os.makedirs(self.experiment.logs_path)  
            
            self.update_experiment_info()
            
            with open(fname, 'wb') as fn:
                pickle.dump(self.experiment, fn)
            
            self.saved.emit()
        except:
            print('were not saved...')
            
            
    
    def experiment_saved(self):
        self.saved_status = True
        self.setWindowTitle('AutonoMouse2')
    
    def status_changed(self):
        self.saved_status = False
        self.setWindowTitle('AutonoMouse2*')
    
    def load_experiment(self):
        try:
            fname, suff = QtWidgets.QFileDialog.getOpenFileName(self, "Open Experiment", '',"AutonoMouse2 Experiment (*.autmaus)")
            
            if fname != '':
                with open(fname, 'rb') as fn:
                    experiment = pickle.load(fn)

                self.setup_experiment_bindings(experiment)
                self.update_experiment_info()
                self.update_trial_view()
        except:
            QtWidgets.QMessageBox.about(self,"Error","Cannot load data")
    
    def thread_control(self):
        self.experiment_control.stop()
    
    def windows_control(self):
        if self.animal_window is not None:
            self.animal_window.close()
        if self.analysis_window is not None:
            self.analysis_window.close()
        if self.hardware_window is not None:
            self.hardware_window.close()
        if self.mail_window is not None:
            self.mail_window.close()
        if self.control_window is not None:
            self.control_window.close()
    
    def closeEvent(self,event):
        if self.saved_status == False:
            answer = QtWidgets.QMessageBox.question(self, "Warning", "Data has not been saved.\nSave changes?",QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No|QtWidgets.QMessageBox.Cancel,QtWidgets.QMessageBox.Cancel)
            if answer == QtWidgets.QMessageBox.No:
                self.windows_control()
                self.saved_status = True
                self.thread_control()
                event.accept()
            elif answer == QtWidgets.QMessageBox.Yes:
                self.save_experiment()
                self.windows_control()
                if self.saved_status:
                    self.thread_control()
                    event.accept()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            self.windows_control()
            self.thread_control()
            event.accept()
            
# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    email.crash_error(exctype,value,traceback)
    # Print the error and traceback
#    test = "".join(traceback.format_exception(exctype,value,traceback))
#    print(test)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainApp()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()