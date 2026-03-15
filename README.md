Predictive Maintenance using Vibration Analysis (ISO 10816-3)

โปรเจคนี้เป็นตัวอย่างการวิเคราะห์การสั่นสะเทือนของเครื่องจักรหมุน (Cooling Pump) เพื่อประเมินสภาพเครื่องจักรและพยากรณ์แนวโน้มการเสียหายในอนาคต โดยอ้างอิงมาตรฐาน ISO 10816-3 และใช้เทคนิค Machine Learning สำหรับการพยากรณ์ค่า vibration ในอนาคต

การวิเคราะห์ในโปรเจคนี้แบ่งออกเป็น 4 ขั้นตอนหลัก ได้แก่

Signal Processing

ISO 10816-3 Assessment

Predictive Simulation

Machine Learning Forecast

Dataset

ข้อมูลที่ใช้เป็นข้อมูลการสั่นสะเทือนของเครื่อง Cooling Pump ซึ่งประกอบด้วย

Time stamp

Amplitude (Acceleration)

ไฟล์ข้อมูลที่ใช้ในโปรเจคคือ

A_Cooling Pump OAH 02_M1H_1480_Oct24.txt

Project Files

01_signal_processing.py
ไฟล์นี้ใช้สำหรับประมวลผลสัญญาณการสั่นสะเทือน โดยทำการอ่านข้อมูล waveform จากไฟล์ .txt จากนั้นลบค่า DC offset ของ acceleration แปลงหน่วยจาก g เป็น m/s² ทำการ integrate เพื่อคำนวณ velocity และคำนวณค่า Velocity RMS (mm/s)

ผลลัพธ์ที่ได้จากขั้นตอนนี้คือ

Velocity RMS = 2.699 mm/s
Velocity Peak = 6.211 mm/s

ไฟล์นี้จะสร้างไฟล์ผลลัพธ์ชื่อ

step1_velocity_timeseries.csv

ซึ่งเป็นข้อมูล velocity ที่ใช้ในขั้นตอนถัดไป

02_iso_assessment.py
ไฟล์นี้ใช้สำหรับประเมินสภาพเครื่องจักรตามมาตรฐาน ISO 10816-3 โดยใช้ค่า Velocity RMS จาก Step 1

สมมติฐานของเครื่องจักร

Machine type : Cooling Pump
Rated power : 75 kW
Foundation : Rigid
ISO group : 15–300 kW

ผลการประเมินพบว่าเครื่องจักรอยู่ใน

Zone A (Good condition)

03_predictive_model.py
ไฟล์นี้ใช้สำหรับจำลองแนวโน้มการเสื่อมสภาพของเครื่องจักร (Predictive Simulation)

มีการจำลอง 3 สถานการณ์ ได้แก่

Normal wear (การสึกหรอตามปกติ)
Misalignment / Unbalance
Bearing damage

โปรแกรมจะสร้างกราฟแนวโน้มค่า RMS และเปรียบเทียบกับเกณฑ์ ISO 10816-3

ไฟล์ผลลัพธ์ที่ได้จากขั้นตอนนี้คือ

step3_simulated_trend.csv
step3_prediction_summary.csv

04_ml_prediction.py
ไฟล์นี้ใช้ Machine Learning (Polynomial Regression) เพื่อเรียนรู้แนวโน้มของค่า RMS และพยากรณ์ค่า vibration ในอนาคต

ขั้นตอนที่ทำในไฟล์นี้

โหลดข้อมูลจาก Step 3
Train โมเดล Polynomial Regression (degree = 2)
ทำการ forecast ค่า RMS ในอนาคต
ตรวจสอบค่าที่เกิน threshold ของ ISO

ผลลัพธ์ที่ได้คือกราฟ

Current RMS trend
Machine Learning forecast
ISO threshold levels

Output Files

ไฟล์ผลลัพธ์ที่ได้จากโปรเจคนี้

step1_velocity_timeseries.csv
ข้อมูล velocity ที่ได้จากการแปลง acceleration

step3_simulated_trend.csv
ข้อมูล trend ที่จำลองสำหรับ predictive analysis

step3_prediction_summary.csv
สรุปผลการคาดการณ์การเสื่อมสภาพของเครื่องจักร

Conclusion

โปรเจคนี้แสดงตัวอย่างการใช้ Vibration Analysis ร่วมกับมาตรฐาน ISO 10816-3 และ Machine Learning เพื่อทำ Predictive Maintenance สำหรับเครื่องจักรหมุน

แนวทางนี้ช่วยให้สามารถ

ตรวจจับความผิดปกติของเครื่องจักร
วิเคราะห์แนวโน้มการเสื่อมสภาพ
พยากรณ์การเสียหายในอนาคต
วางแผนการบำรุงรักษาล่วงหน้า

ซึ่งช่วยลดความเสี่ยงของการหยุดเครื่องจักรโดยไม่คาดคิดและเพิ่มความน่าเชื่อถือของระบบเครื่องจักร
