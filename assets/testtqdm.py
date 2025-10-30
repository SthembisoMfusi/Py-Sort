from tqdm import tqdm
import time
rg=50
prog=tqdm(total=rg,desc="Loading",position=0)
for i in range(rg):
    print("\n",i)
    prog.update((((i+2)/rg)*2))
    time.sleep(0.1)
prog.close()
    