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

from os import path, listdir
import subprocess
import ConfigParser
import re

###########
# Configuration
###########

_workingDir = r"C:\Diamonds\PolishedAnalyserHarness"
_executable = r"C:\Diamonds\PolishedAnalyserHarness\Release_x64\PolishedAnalyserHarness.exe"
_DLL = r"PolishedAnalyserx64.dll"  # relative to workingDir
_iniPath = _workingDir + r"\PolishedAnalyserDLL.ini"

directoriesToProcess = [
    r"\\us-topeka\Projects-LA\Diamonds\Phase 9 - Area 1 Aretfacts 2014-09\Polished2014\End of nozzle problems",
    r"\\us-topeka\Projects-LA\Diamonds\Phase 9 - Area 1 Aretfacts 2014-09\Sept 2014 data\End of nozzle problems",
    r"\\us-topeka\Projects-LA\Diamonds\Phase 9 - Area 1 Aretfacts 2014-09\Polished2014\Dirt",
    r"\\us-topeka\Projects-LA\Diamonds\Phase 9 - Area 1 Aretfacts 2014-09\Sept 2014 data\Dirt",
    r"\\us-topeka\Projects-LA\Diamonds\Phase9 - Area 1 Artefacts 2014-10\Good stones"
]


###########
# Utils
###########

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
    parser.set("Calibration", "Calibration File", job + r"\calibration-YawSet0.ini")
    parser.set("Calibration", "Delta theta file", job + r"\calibration-deltaTheta.csv")

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

    for job in jobs:

        updateIniFile(_iniPath, job)

        # Run the process, if it doesn't return 0 then log it
        returnCode = runProcess(_executable, _DLL, _workingDir)

        if returnCode != 0:
            with open(_workingDir + r"\LogFiles\UnexpectedReturns.txt", "a") as logFile:
                logFile.write("%s: %d\n" % (job, returnCode))
