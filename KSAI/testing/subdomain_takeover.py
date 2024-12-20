from testing.require import * 

def Run(insubdomainsfile, outputFile):
     command = rf"cat {insubdomainsfile} | nuclei -t nuclei-templates/http/takeovers/ | tee {outputFile}"
     RunCommand(command, "Subdomain takeover test Successful", "Subdomain Takeover test failed")
     pass