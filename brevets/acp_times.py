"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

MAX_SPEEDS = [34, 32, 30, 28, 28, 26]
MIN_SPEEDS = [15, 15, 15, 11.428, 11.428, 13.333]

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    i = 0
    time = 0
   
    if control_dist_km > brevet_dist_km:
       control_dist_km = brevet_dist_km

    while control_dist_km > 200:
        time += (200/MAX_SPEEDS[i])
        i += 1
        control_dist_km -= 200

    time += (control_dist_km/MAX_SPEEDS[i])        
    time = ((time * 60) + 0.5)
    int(time)
    finalTime = arrow.get(brevet_start_time).shift(minutes=time)
    return finalTime


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    i = 0
    time = 0
    additionalTime = 0.5

    if (brevet_dist_km == 200 and control_dist_km >= 200):
       additionalTime += 10

    if (brevet_dist_km == 400 and control_dist_km >= 400):
       additionalTime += 20
    
    if control_dist_km > brevet_dist_km:
       control_dist_km = brevet_dist_km

    #if control_dist_km == 0:
      #return arrow.get(brevet_start_time).shift(hours=1)
    if control_dist_km <= 60:
       time = 60 + (3 * control_dist_km)
       finalTime = arrow.get(brevet_start_time).shift(minutes=time)
       return finalTime
    else:
      while control_dist_km > 200:
        time += (200/MIN_SPEEDS[i])
        i += 1
        control_dist_km -= 200

    time += (control_dist_km/MIN_SPEEDS[i])        
    time = ((time * 60) + additionalTime)
    int(time)
    finalTime = arrow.get(brevet_start_time).shift(minutes=time)
    return finalTime
