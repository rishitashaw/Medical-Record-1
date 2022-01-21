# REST API documentation for Medical Record

## Report Upload
## Required: POST request

## Parameters: <br>
•	tag: Tag ID scanned from temporary token <br>
•	testname: Test name <br>
•	testdate: Date of the test in YYYY-MM-DD format <br>
•	file: Report in XML or PDF format <br>
Endpoint: https://medical-record.centralindia.cloudapp.azure.com/api/reportupload  <br>
<br><br>
## Example with cURL:
```
 curl -i -X POST -H "Content-Type: multipart/form-data" \
-F "tag=tag_36ffa5b6-42a8-45dc-8ea6-f893bb5f4b1a" \
-F "testname=ECG" \
-F "testdate=2022-01-16" \
-F "file=@E:/ECG_report.pdf" \
https://medical-record.centralindia.cloudapp.azure.com/api/reportupload
```
## Response:
```
HTTP/1.1 200 OK
Date: Sun, 16 Jan 2022 01:15:13 GMT
Server: Apache/2.4.29 (Ubuntu)
Content-Length: 13
Vary: Accept-Encoding
Content-Type: text/html; charset=utf-8

File uploaded
```
## Responses:
•	Token expired: Invalid or expired token <br>
•	Invalid test date: Test date out of format or in future <br>
•	Unsupported file: File out of format <br>
•	File uploaded: File uploaded successfully <br>
 <hr>
 
## Token Details
## Required: GET request

## Parameters: <br>
•	tag: Tag ID scanned from temporary token <br>

Endpoint: https://medical-record.centralindia.cloudapp.azure.com/api/tokendetails  <br>
<br><br>

## Example with cURL:
```
curl https://medical-record.centralindia.cloudapp.azure.com/api/tokendetails?tag=tag_a450ba5c-772c-4da4-996e-6f76149bfa4a
```
## Response:
```
{"expiry": "2022-01-23", "issued_to": "Hospital 1", "name": "Aditya Mitra"}
```
## Responses:
•	Token expired: Invalid or expired token <br>
•	Returns expiry date of the token (in YYYY-MM-DD format), to one it is issued to and patient name in JSON format.
