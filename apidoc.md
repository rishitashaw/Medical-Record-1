# REST API documentation for Medical Record upload
## Required: POST request

## Parameters: <br>
•	tag: Tag ID scanned from temporary token <br>
•	testname: Test name <br>
•	testdate: Date of the test in YYYY-MM-DD format <br>
•	file: Report in XML or PDF format <br>
Endpoint: https://medrecord.eastus.cloudapp.azure.com/api/reportupload  <br>
<br><br>
## Example with cURL:
```
 curl -i -X POST -H "Content-Type: multipart/form-data" \
-F "tag=tag_36ffa5b6-42a8-45dc-8ea6-f893bb5f4b1a" \
-F "testname=ECG" \
-F "testdate=2022-01-16" \
-F "file=@E:/ECG_report.pdf" \
https://medrecord.eastus.cloudapp.azure.com/api/reportupload
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
