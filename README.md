# CloudBasedRansomwareDetection
The Cloud Based Ransomware Detection is an application that helps the user to protect against ransomware, fast and efficient. This program provides a cloud interface that operates automatically, which uses online services to get a full analysis of the executable.

If the report is positive (i.e. the executable is a ransomware), the user application will delete the executable from the client’s computer without its interference, and a popup will appear to notify the user he has downloaded a malicious file.

This program uses a client/server based model. The client is basically the user’s computer. The client program will communicate with:

•	Machine learning server that will examine the executable bytes of the executable and based on a trained model it will report if it a ransomware or not. 

•	Dynamic analysis server that will run the executable in an isolated environment, and based on hundreds of scans and sophisticated analysis, it will return the executable chances to be a ransomware and the overall behavior of the executable. 
Also, the dynamic analysis server sends a real screenshot of the executable in action, which will be presented if eventually it will be a ransomware.
