import pandas as pd

# ====== INPUT (แก้ตรงนี้) ======
VEL_RMS = 2.699  # mm/s (จาก Step 1)
# เลือกกลุ่ม/ฐาน (ถ้าโจทย์ไม่ให้ ให้สมมติและเขียนในรายงาน)
GROUP = "15-300kW"         # ตัวอย่างสมมติ
FOUNDATION = "Rigid"        # "Rigid" หรือ "Flexible"

# ====== ISO 10816-3 Thresholds (ตัวอย่างชุดที่ใช้กันบ่อยในงานเรียน) ======
# หมายเหตุ: เกณฑ์จริงขึ้นกับ Group/ฐาน ให้คุณอ้างอิงรูป chart ของอาจารย์ประกอบในรายงาน
# ชุดนี้: 15–300 kW (มักใช้เป็น Group 2/4 ในหลายสไลด์เรียน)
THRESHOLDS = {
    "15-300kW": {
        "Rigid":   {"A_B": 2.8, "B_C": 4.5, "C_D": 7.1},
        "Flexible":{"A_B": 4.5, "B_C": 7.1, "C_D": 11.0},
    }
}

def classify_zone(v_rms, th):
    if v_rms < th["A_B"]:
        return "Zone A", "ดีมาก / เครื่องใหม่หรือสภาพดี"
    elif v_rms < th["B_C"]:
        return "Zone B", "ใช้งานได้ปกติ (Unrestricted operation)"
    elif v_rms < th["C_D"]:
        return "Zone C", "ควรวางแผนซ่อม/ตรวจเพิ่ม (Restricted operation)"
    else:
        return "Zone D", "เสี่ยงเสียหาย/ควรหยุดหรือแก้ไขด่วน (Damage occurs)"

th = THRESHOLDS[GROUP][FOUNDATION]
zone, meaning = classify_zone(VEL_RMS, th)

print("=== STEP 2: ISO 10816-3 ASSESSMENT ===")
print(f"Velocity RMS (mm/s): {VEL_RMS:.3f}")
print(f"Assumption: GROUP={GROUP}, FOUNDATION={FOUNDATION}")
print(f"Thresholds: A/B={th['A_B']}, B/C={th['B_C']}, C/D={th['C_D']} (mm/s)")
print(f"Result: {zone} -> {meaning}")