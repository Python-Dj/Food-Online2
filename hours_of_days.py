from datetime import time

HOURS_OF_DAY_24 = []

for h in range(0, 24):
    for m in (0, 30):
        HOURS_OF_DAY_24.append((time(h, m).strftime("%I:%M %p"), time(h, m).strftime("%I:%M %p")))

print(HOURS_OF_DAY_24)