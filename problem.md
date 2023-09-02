## Problem

For this problem, you will develop a Python library that encapsulates the fetching of stock quotes from an upstream service, as well as some simple operations. Our upstream source will be Alpha Vantage. Specifically you can use either [TIME_SERIES_DAILY](https://www.alphavantage.co/documentation/#daily) or [TIME_SERIES_DAILY_ADJUSTED](https://www.alphavantage.co/documentation/#dailyadj) to fetch data. You can get a free API key for AlphaVantage from [here](https://www.alphavantage.co/support/#api-key). Note that this key will be limited to 500 calls per day.

We estimate that this should take no more than a couple of hours to complete (perhaps slightly longer for anyone using Python for the first time). Feel free to make compromises based on time-boxing this to a couple of hours. This exercise is meant to get a general sense of how you approach writing reusable software libraries; it needn't be a bulletproof production-grade solution.

## Requirements

The library should provide functionality to perform the following:

1. `lookup`: given a symbol and a date, return the open, high, low, close, and volume for that symbol on that date.

2. `min`: given a symbol and a range 'n', return the lowest price that symbol traded at over the last 'n' data points (lowest low).

3. `max`: given a symbol and a range 'n', return the highest price that symbol traded at over the last 'n' data points (highest high).

It is left up to you to design the interface (function signatures, objects, classes)

## Deliverables

Final deliverable should be a zipped github repo containing software and a brief write-up:

### Software

- your solution implemented in Python
- instructions on how to build, package, and install the library
- a usage example

### Discussion

A short write-up where you discuss the following:

- What compromises did you make due to time constraints?
- How would you approach versioning of this library?
- How would we go about publishing this library?
- How would you design this if it was going to be a service rather than a library?
- Please include any other comments about your implementation.
- How much time did you spend on this exercise?
- Please include any general feedback you have about the exercise.
