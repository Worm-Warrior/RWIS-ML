## Data (Surface Dataset)

https://mesonet.agron.iastate.edu/RWIS/currentSF.phtml

Going to target Aug 1st to Dec 31st of each year.

Data Headers: 
    - Air Temp[F] (tmpf)

    - Dew Point Temp [F] (dwpf)

    - Feels Like Temp [F] (feel)

    - Relative Humidity [%] (relh)

    - Wind Speed [knots] (sknt)

    - Wind Direction [Degree N] (drct)

    - Wind Gust [knots] (gust)

    - Pavement Sensor0 Temp [F] (tfs0)

    - Pavement Sensor0 Condition (tfs0_text)
    
    - Pavement Sensor1 Temp [F] (tfs1)

    - Pavement Sensor1 Condition (tfs1_text)

    - Pavement Sensor2 Temp [F] (tfs2)

    - Pavement Sensor2 Condition (tfs2_text)

    - Pavement Sensor3 Temp [F] (tfs3)

    - Pavement Sensor3 Condition (tfs3_text)

    - Subsurface Temp [F] (subf)


## What features do we *not* care about?


Station -> This should not matter, I think that it will just be noise for the model, we care about the data itself.

Feels Like Temp -> This is pretty much just a combo of temp, wind, humid. We have those already so we don't want this I think.

