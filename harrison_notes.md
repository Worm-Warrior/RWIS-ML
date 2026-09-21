## Some sensors have more readings than others

Some of the sensors have a much lower rate of having any data reported at all.

We could go for a solution that involves going in order and picking the one that has the reading and using that one.

So sens0 -> sens1 -> ... and so on, and we pick the first one that has a valid reading.

## Drop rows that have certain values missing

1. Missing all labels of condition

2. Missing the pavement sensor temp for the sensor with a condition

3. Missing Air Temp


## What features do we *not* care about, and plan to not use in training?

station -> This should not matter, I think that it will just be noise for the model, we care about the data itself.

feel -> This is pretty much just a combo of temp, wind, humid. We have those already so we don't want this I think.

subf -> Almost no data points after 2015, and zeroed out after 2017

pcpn -> 2015 almost no data points, 2016-2020 zero data points, 2021-2025 good amount of data. We still want to try and use this if we can though.

vsby -> Visibility does not really do anything for us, and some years have low entries.

obtime(year) -> We should not really care about the year part of the obtime, unless we are doing some climate change angle.


## Data format?

Plan:

- Keep the raw files split by year as the source of truth, so each year's data can be inspected and reprocessed independently.
- Clean each yearly file separately, then combine the cleaned yearly outputs only when building the training dataset.