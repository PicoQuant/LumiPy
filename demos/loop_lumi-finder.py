# Edited by Chenyang Lan on May 4th, 2026.

import pqlumi as pql
import pqtool as pqt

# Get user input for the number of loops
try:
    loop_input = input("Enter the number of loops to perform: ")
    total_loops = int(loop_input)
except ValueError:
    print("Invalid input. Defaulting to 1 loop.")
    total_loops = 1

# Start the main automation loop
for loop_idx in range(total_loops):
    print(f"\n--- Starting Process Loop {loop_idx + 1} of {total_loops} ---")

    # --- Step 1: Read Imaging UI Settings ---
    # Fetch current scan speed and stop conditions from the Imaging section #[cite: 1, 9]
    print("Reading Imaging UI settings...")
    img_speed = pql.measurement.img_conf.scan_speed #[cite: 1, 9]; Looks at the "Imaging" tab in the software and records how fast the scan is set to run.
    img_stop_frames = pql.measurement.img_conf.stop_on_num_frames #[cite: 1, 9] 
    img_num_frames = pql.measurement.img_conf.num_frames #[cite: 1, 9] checks how many frames the system is to capture
    
    print(f"  Settings: Speed {img_speed}%, Stop on {img_num_frames} frames.") #[cite: 1]

    # --- Step 2: Capture Image (Start Button) ---
    # Trigger the hardware for a full image capture #
    pql.measurement.start_meas('image') #[cite: 3, 9]
    print("Image capture in progress...")

    # Wait for the image acquisition to complete before proceeding #
    while True:
        if not pql.measurement.meas_status(): #[cite: 3, 9]
            break
        pqt.gui_sleep(100) # Keep GUI active and responsive #[cite: 3]
    print("Image capture finished.")

    # --- Step 3: Run LumiFinder ---
    # Execute the spot detection algorithm on the captured image #
    print("Running LumiFinder...")
    pql.measurement.point_conf.lumi_finder() #[cite: 9]

    # Retrieve the list of detected spot coordinates in meters #[cite: 5, 9]
    spot_list = pql.measurement.point_conf.point_list #[cite: 5, 9]
    num_spots = len(spot_list)

    if num_spots == 0:
        print("Find 0 spot") #[cite: 5]
    else:
        print(f"Find {num_spots} spots") #[cite: 5]

    # --- Step 4: Read Point UI Settings ---
    # Fetch acquisition conditions from the Point section #[cite: 1, 9]
    pnt_stop_time = pql.measurement.point_conf.stop_on_meas_time #[cite: 1, 9]
    pnt_meas_time = pql.measurement.point_conf.meas_time #[cite: 1, 9]
    print(f"Point Settings: Stop on time ({pnt_stop_time}) for {pnt_meas_time} s.") #[cite: 1]

    # --- Step 5: Perform Point Measurements for each Spot ---
    # Iterate through each detected coordinate and start point measurement #[cite: 6, 8]
    if num_spots > 0:
        for i, coord in enumerate(spot_list):
            # Assign the current target coordinate to the hardware #[cite: 8, 9]
            pql.measurement.point_conf.selected_point = coord #[cite: 8, 9]
            
            # Start the point measurement (e.g., FCS) #[cite: 6, 9]
            pql.measurement.start_meas('point') #[cite: 6, 9]
            print(f"  Loop {loop_idx + 1}: Measuring spot {i+1}/{num_spots} at {coord}...")
            
            # Wait for the specific point measurement to finish #[cite: 6]
            while True:
                if not pql.measurement.meas_status(): #[cite: 6, 9]
                    break
                pqt.gui_sleep(100) #[cite: 3, 6]
        
        print(f"Loop {loop_idx + 1} point sequence complete.")
    else:
        print(f"Loop {loop_idx + 1} skipped point measurements (no spots).")

print("\n--- All requested loops have been completed ---")
