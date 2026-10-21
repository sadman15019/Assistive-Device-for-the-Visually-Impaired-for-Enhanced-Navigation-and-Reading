from textblob import TextBlob
from spellchecker import SpellChecker
import re

string="underserved areas where traditional methods might be less available. Healthwise, this study contributes to the carly detection of ancmia and other diseases for timely interventions. It also minimizes paticnt discomfort and enxicly by eliminating invasive procedures, cnhancing adherence to monitoring. This non invasive method ensures by lowering, the infection risks, complications. Legally this method requires handling or patient data collected through non-invasive methods and involvement of complisnes with data protection laws to onsure patient privacy and security. This method offers nom invasive options that empower individuals to take control of their health in a manner that is culturally appropriate and aligned with their values. 1.8 Applications of the Work Non-invasive hemoglobin measurement has the potential to offer a practical, painless, and uccessible way to determine hemoglobin levels, it has a umber of real-world applications in numerous sectors. The following are some significant applications:  © Clinical Healthcare Settings: Non-invasive hcmoglobin measurement is a quick and painless way to check pationts' hemoglobin levels in hospitals, clinics, and healthcare facilitics. This can aid medical practitioners in the diagnosis of discases like anemia and real time monitoring the efficacy of treatments. e Tosting at the Point of Carc: It can be integrated into point-of-care testmg devices for rapid atsessment of hemoglobin levels in remote or underserved areas. » Home Healthcare Monitoring: Patients with chronic conditions can vec it for home monitoring, reducing the need for frequent visits to medical facilitics. » Blood Donation and Transfusion Management: Blood banks and donation centers  can vse it to sereen potential donors and ensure thet their hemoglobin levcls meet the requirements for safe blood donation. - ® Remote Monitoring and Telemedicine: It can be integrated into wearnble devices and remote monitoring systems for remote tracking of patients’ hemoglobin levels, e Poblic Health Screening: It can be used in large-scale health scrcening proprams to identify individuals at risk of anemia and other blood-related disorders,"

# docx=re.findall("[a-zA-Z0-9]+",string)
# # print(docx)
# tb = TextBlob(string)
# corrected = tb.correct()

# print(str(corrected))
# spell=SpellChecker(distance=1)
# mis=spell.unknown(docx)
# for word in mis:
#     tb = TextBlob(word)
#     corrected = tb.correct()
#     print(word,"---->",corrected)

spell=SpellChecker(distance=1)
a="sdfsdf" 
mis=spell.unknown(a.split())
print(len(mis))  