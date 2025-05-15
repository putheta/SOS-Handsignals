import numpy as np
# ข้อมูลจากการเก็บตัวอย่างจากไฟล์ exel
height = np.array([109, 143, 198, 233, 326, 340, 369])
error = np.array([4, 49, 20, 29, 35, 87, 94])

# ทำ polynomial regression องศา 2
#ใช่ครับ ผมใช้แชท ผมกากคณิตคับ
coeffs = np.polyfit(height, error, 2)

print(coeffs)  # ได้ [a, b, c]
