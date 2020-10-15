###########
#
# Batch process diamonds
# Usage: 
#   Set up paths to executable, DLL and working directory. Point the 
#   foldersToProcess array to one or several  directories that contains diamonds 
#   which need to be processed. Make sure each folder contains both images, 
#   calibration and delta_theta files.
# 
#   WARNING: Modifies the ini-file in the working directory and strips
#            all comments!
#
###########

from os import path, listdir, mkdir, path
from shutil import copyfile, move
import subprocess
import ConfigParser
import re

###########
# Configuration
###########

_workingDir = r"F:\Eagle processing\402GRPbuild"
_executable = r"F:\Eagle processing\402GRPbuild\PolishedAnalyserHarness.exe"
_DLL = r"PolishedAnalyserx64.dll"  # relative to workingDir
_iniPath = _workingDir + r"\PolishedAnalyserDLL.ini"
_savefolder = _workingDir + "\\Results-AWP\\Eagle-11\\"

rangefolder = r"T:\Eagle 11"
datefolderlist = listdir(rangefolder)
directoriesToProcess = [rangefolder + "\\" + directory for directory in datefolderlist]


# directoriesToProcess = [r'W:\Clarity DB 28-08-13 to 11-10-13\2013-09-04 11-05-43', r'W:\Clarity DB 28-08-13 to 11-10-13\2013-09-09 07-00-25']
# directoriesToProcess = ["g:\\End of nozzle problems"]



###########
# Utils
###########
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Builds a job list for given directory of jobs
def buildJobList(dirList):
    jobs = []
    for d in dirList:
        jobs += [d + "\\" + job for job in listdir(d) if path.isdir(d + "\\" + job)]

    return jobs


# Updates the required paths in the ini file to point to the given job
def updateIniFile(iniPath, job):
    # Modify ini file

    parser = ConfigParser.RawConfigParser()

    # Override method to leave case alone when reading option names
    parser.optionxform = str
    parser.readfp(CommentlessFile(iniPath))

    parser.set("Images", "Stored images", job + r"\diffuse0\diffuse0-%03d.png")
    parser.set("Calibration", "Calibration File", job + r"\currentcalib-YawSet0.ini")
    parser.set("Calibration", "Delta theta file", job + r"\currentcalib-deltaTheta.csv")

    parser.write(file(iniPath, "w"))


# Run the process...
def runProcess(exe, dll, workingDir):
    testHarnessProcess = subprocess.Popen([exe, dll], cwd=workingDir)
    testHarnessProcess.wait()
    return testHarnessProcess.returncode


# Overloaded file class that strips comments from INI file.
# Required since the ConfigParser doesn't like comments
class CommentlessFile(file):
    def readline(self):
        line = super(CommentlessFile, self).readline()
        if not re.search(r'^[-/#]', line.strip()):
            return line
        else:
            return '#'


###########
# Main
###########

if __name__ == "__main__":

    jobs = buildJobList(directoriesToProcess)
    print str(len(jobs)) + " Jobs in total"
    jobcount = 0
    for job in jobs:
        jobcount += 1
        ###########################
        # Check not a calibration folder and we haven't done this stone already and that there is a calib file
        ###########################
        if job[-11:] != 'calibration' and path.exists(_savefolder + job[-11:]) == False and \
                path.exists(job + r'\calibration-YawSet0.ini') and is_number(job[-11:]):

            print job + ", Job no." + str(jobcount) + " Out of " + str(len(jobs))
            copyfile(job + r'\calibration-YawSet0.ini', _workingDir + r"\Calib\currentcalib-YawSet0.ini")
            copyfile(job + r'\calibration-deltaTheta.csv', _workingDir + r"\Calib\currentcalib-deltaTheta.csv")

            updateIniFile(_iniPath, job)

            # Run the process, if it doesn't return 0 then log it
            returnCode = runProcess(_executable, _DLL, _workingDir)

            if returnCode != 0:
                with open(_workingDir + r"\LogFiles\UnexpectedReturns.txt", "a") as logFile:
                    logFile.write("%s: %d\n" % (job, returnCode))
            if returnCode == 0:
                ExportPath = _workingDir + "\\Export\\"
                out_files = listdir(ExportPath)

                mkdir(_savefolder + job[-11:])
                for outfile in out_files:
                    move(_workingDir + "\\Export\\" + outfile, _savefolder + job[-11:])
