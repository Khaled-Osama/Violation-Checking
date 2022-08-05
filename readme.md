# Violation Detection.

Machine Learning system to detect, track the cars then calculate the speed based on changes on pixels whithing a specific time.

## Required Installations

the are some of installations needed to run the system successfully, we need to install the following:

```
$ conda install pytorch==1.9.0 torchvision==0.10.0 torchaudio==0.9.0 cudatoolkit=11.3 -c pytorch -c conda-forge
$ pip install opencv-python==4.5.3.56
$ pip install pandas==1.3.1
$ pip install numpy==1.19.5
$ pip install tqdm==4.49.0
$ pip install matplotlib==3.5.1
$ pip install requests==2.26.0
$ pip install pyyaml==6.0
$ pip install seaborn==0.11.2
$ pip install strenum==0.4.7
$ pip install tensorboard==2.7.0
```

## Sample code
There is a python file main.py which acts as an entry point to the system.
<img src="Screenshot from 2022-02-06 05-58-03.png" alt="My cool logo"/>

## Expected Output

Violation_report.csv: which contains all violations in every frame, so every car can
appear several times in different frames but this file can take further steps to get
exactly what we want.
video_Demo.avi: if the makeDemo flag is passed as True so, the video will be
generated while the query video is processed.
logs.log : the run logging file which tells us more details about this run.

## Demo Description
The demo will show all the results of the system. All vehicles should be bounded by boxes
and every car type (Car, Van, Truck) should have different colours.
● Blue for Car
● Red for Van
● Green for Truck
Every vehicle should have an identifier which is a number displayed above the object box
which shouldn’t be changed for a specific vehicle.
If any vehicle speed exceeds the limit speed which in our case (Car => 120 pixel/sec, Van
=> 80 pixel/sec, Truck => 60 pixel/sec) so a red segment will fill the bounding box of that
vehicle.
There are 2 counters in the top left of each frame that displays the frame number and
