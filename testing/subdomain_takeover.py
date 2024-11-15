from testing.require import * 

def Run(insubdomainsfile, outputFile):
     command = rf"cat {insubdomainsfile} | nuclei -t"
     pass