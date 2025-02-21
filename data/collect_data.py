
import os, time
from pathlib import Path
import numpy as np
import sys
from tqdm import tqdm
# data_dir = __file__.parent.parent / "data"
data_dir = Path(__file__).parent 
sys.path.append(str(data_dir.parent))
print(data_dir.parent)

from raspberry_pi.sensors.arduinonNano33BleSense import arduino_sensor
    
def collect_data(posture_type):
    
    time.sleep(1)
    # Collect data for 10 seconds
    collected_data = []
    pbar = tqdm(total=10, desc="Collecting Data", ncols=100)
    while len(collected_data) < 10:
        # Collect data from the sensors
        data = arduino_sensor.read_data()
        if data is not None:
            collected_data.append(data)
            pbar.update(1)
    pbar.close()
    return np.array(collected_data)

if __name__ == "__main__":
    posture_type = sys.argv[1]
    
    assert posture_type in ["good", "bad", "debug"], "Invalid posture type"
    
    collected_data = collect_data(posture_type)
    
    # Save the collected data to a file
    dataset_dir = data_dir / 'dataset' / f'{posture_type}_posture' 
    dataset_dir.mkdir(parents=True, exist_ok=True)
    num_files = len(os.listdir(dataset_dir))
    np.save(dataset_dir / f'data_{num_files}.npy', collected_data)
    
    
 