# PyPromise

This module has been written out of curiosity to understand the intricacies of Locks and Condition Variables
and how these primitives play a pivotal role in creating constructs like `Future` and `Promise` which are often taken for 
granted when we start programming in "higher level" programming languages. 

### What is a Future anyway?

A Future object holds a task or a function whose execution is likely to be completed in the near future. Meaning that 
the task or the function will not block the execution of the main thread of the program. In simple words, a Future 
object works asynchronously. 

### How Future can be useful for real life scenario?

Consider a scenario where you have to fetch the weather information by making a simple API call from the web. One simple
way of doing is as follows:

```python
import requests

response = requests.get("http://example-weather.com/?state=assam&city=jorhat?date=20241229")
print(response.text)
```
Huh... that was easy. Where is the catch?
Now if we introduce some modification in the requirements viz. fetch the weather information like before and fetch the
population of a city. Well you can argue that the same approach can be used:

```python

import requests

weather_response = requests.get("http://example-weather.com/?state=assam&city=jorhat?date=20241229")
print(weather_response.text)

census_response = requests.get("http://example-census.com/?state=assam&city=jorhat")
print(census_response.text)
```
The bottleneck in the above approach is that until an unless we don't get any response from our trusty weather API, our
main thread will be stuck at it. Worst, we don't even know if our trusty weather API will ever respond! 

Here comes *Future*

```python

import requests
from pypromise.future import Future, submit_future

future_weather_response: Future = submit_future(
    requests.get, 
    "http://example-weather.com/?state=assam&city=jorhat?date=20241229"
)

future_census_response: Future = submit_future(
    requests.get, 
    "http://example-census.com/?state=assam&city=jorhat"
)
```
Now we wrapped our two API calls inside a **Future** object which will magically make them work asynchronously. Now it doesn't
matter whether weather API responds or not because both API calls are running independently. To get the actual response 
from the future object, we have to use the `get()` method which **will block** the main execution till the actual response is
retrieved from the server.

### What is a Promise?

`Promise` is another construct for introducing asynchronization in a program. A `Promise` promises the resolution of a passed function
in the near future or rejection on error.

A `Promise` let's you chain callbacks into it unlike `Future`. It also does not block the main thread on successive callbacks like the `get()` of a `Future` does.

Continuing the same example from above, we can pass the output of the previous computation as an input to `then()` method and perform
next set of asynchronous actions on it. In our simple example, we simply extracted the response and converted it to a Python
dictionary. The entire thing is happening on a different thread without blocking any execution on the main thread. Naturally, 
`then()` method can be chained for performing multiple asynchronous tasks back to back

```python

import requests
import json
from pypromise.promise import submit_promise

submit_promise(requests.get, "http://example-weather.com/?state=assam&city=jorhat?date=20241229").then(
    lambda x: json.loads(x.text)
)
```





