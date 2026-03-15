คำอธิบายไฟล์ในโปรเจค
01_signal_processing.py

ไฟล์นี้ใช้สำหรับ ประมวลผลสัญญาณการสั่นสะเทือน

ขั้นตอนที่ทำในไฟล์นี้

อ่านข้อมูล waveform จากไฟล์ .txt

ลบค่า DC offset ของ acceleration

แปลงหน่วยจาก g → m/s²

ทำการ integrate เพื่อคำนวณ velocity

คำนวณค่า Velocity RMS (mm/s)

ตัวอย่างผลลัพธ์

Velocity RMS  = 2.699 mm/s
Velocity Peak = 6.211 mm/s

ไฟล์นี้จะสร้างไฟล์ผลลัพธ์

step1_velocity_timeseries.csv

ซึ่งเป็นข้อมูล velocity ที่ใช้ในขั้นตอนถัดไป

02_iso_assessment.py

ไฟล์นี้ใช้สำหรับ ประเมินสภาพเครื่องจักรตามมาตรฐาน ISO 10816-3

สมมติฐานของเครื่องจักร

รายการ	ค่า
ประเภทเครื่องจักร	Cooling Pump
กำลังเครื่อง	75 kW
ฐานเครื่อง	Rigid
ISO Group	15–300 kW

ผลการวิเคราะห์

Velocity RMS = 2.699 mm/s
Machine Condition = Zone A (Good Condition)

หมายความว่าเครื่องจักรยังสามารถทำงานได้ตามปกติ

03_predictive_model.py

ไฟล์นี้ใช้สำหรับ จำลองแนวโน้มการเสื่อมสภาพของเครื่องจักร

มีการจำลอง 3 สถานการณ์ ได้แก่

Normal wear (การสึกหรอตามปกติ)

Misalignment / Unbalance

Bearing damage

โปรแกรมจะสร้างกราฟแนวโน้มค่า RMS และเปรียบเทียบกับเกณฑ์ ISO 10816-3

ไฟล์ผลลัพธ์ที่ได้

step3_simulated_trend.csv
step3_prediction_summary.csv
04_ml_prediction.py

ไฟล์นี้ใช้ Machine Learning (Polynomial Regression) เพื่อเรียนรู้แนวโน้มของค่า RMS และพยากรณ์ค่า vibration ในอนาคต

ขั้นตอนหลัก

โหลดข้อมูลจาก Step 3

Train โมเดล Polynomial Regression

พยากรณ์ค่า RMS ในอนาคต

เปรียบเทียบค่าที่ได้กับเกณฑ์ ISO

ผลลัพธ์จะเป็นกราฟที่แสดง

แนวโน้มค่า RMS ปัจจุบัน

ผลการพยากรณ์จาก Machine Learning

เส้นเกณฑ์ ISO 10816-3

ไฟล์ผลลัพธ์ (Output)
ไฟล์	คำอธิบาย
step1_velocity_timeseries.csv	ข้อมูล velocity ที่ได้จากการแปลง acceleration
step3_simulated_trend.csv	ข้อมูลแนวโน้มที่จำลอง
step3_prediction_summary.csv	สรุปผลการคาดการณ์การเสื่อมสภาพ
