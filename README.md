# [FIDO2 Smart Card for Medical record maintenance and Temporary Token Authentication for in-house hospital patients](https://medical-record.centralindia.cloudapp.azure.com)

FIDO2, a recently evolved technology by FIDO Alliance is on its way to prove itself to be
instrumental in Passwordless authentication frameworks. However, it can used for much more than
just authentication. This project proposes a centralized system for medical record maintenance of
everyone. We aim to have a partnership with various hospitals. It guarantees easy record maintenance
and hence the patients will not have to go about the hospitals with an entire medical file.

## Contributors

1. [Aditya Mitra](http://github.com/AdityaMitra5102)
2. [Rishita Shaw](http://github.com/theseregrets)
3. [Anisha Ghosh](http://github.com/anisha100)

## Objective

Users willing to use this service can buy a FIDO2 supported physical security key with USB and NFC
capabilities. Then register on our website to generate a unique username and register the FIDO2 key
along with it. The user portal contains the option to view and upload the medical reports. It is to be
noted that there is no way to delete already added reports. This is to prevent misguidance. There is
also an option to register a temporary token for authentication. This temporary token would be just an
NFC card which can be kept in the hospital files. The user must set an expiry date for the NFC card
after which it will be automatically disabled. A hospital while admitting a patient can request the
patient to register the smart card which can be kept in the hospital files so that the doctors can access
the patient records and add new reports after medical tests.
**The user has the option to disable the registered temporary tokens on discharge from the hospital to
prevent data misuse, and if not disabled manually, it will be automatically disabled when the
stipulated time has passed.**

## Features

The website will have two versions:

1. User version: This has the option to view records, add records, register and remove temporary
   tokens and register new FIDO2 keys.
2. Hospital version: This has only the options to view and add records. The hospital will not be
   authorized to manage tokens and keys. It is to be noted that the hospital can login only with
   temporary tokens.
3. For medical equipments: We provide an API endpoint with which medical devices and softwares 
   will be able to directly upload the report against an user. It is to be noted that the medical 
   equipments should preferably be interfaced with a NFC reader as the API endpoint authenticates 
   the device with it only. API Documentation [here](./apidoc.md)

## Tech Stacks
```bash
Technologies to be used:
• FIDO2 Specifications
• Web NFC
• Microsoft Azure.
```
## FAQ

FAQ:

1. What if the user loses the FIDO2 key? – he can login via Email OTP to assign new FIDO2
   key.
2. When the user is sick how can he login? – Since FIDO2 is a Passwordless technology, the
   family members of the user can use the security key.
3. What are the system requirements for the user? – Any android phone with Google Chrome
   89+ and NFC reader.
4. What are the system requirements for the hospital? – Android device with Google Chrome
   89+ and NFC reader. However, it is inconvenient for the hospital to use phone so any
   computer with NFC reader is supposed to work. Some laptops have NFC readers inbuilt, as
   well as USB NFC readers are available.
5. How will the reports be stored? – The reports will be stored as uploaded by the hospital in any
   file. We are intentionally not enforcing any file format as some medical records need to be
   stored as PDF, while some like the medical scans are stored as DICOM or other formats.
