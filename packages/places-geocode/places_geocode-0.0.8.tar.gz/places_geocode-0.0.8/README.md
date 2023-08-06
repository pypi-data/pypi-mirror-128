### **Places API Geocoding**! 

There are a many geocoding APIs out there to choose from. However, `Places API` tops them
all with the most accurate, affordable, and effective solution!  

Our package focuses on a pythonic and accessible way to geocode POIs (Places of Interest) in Python. 

---

#### **SUPPORT**

We have multiple support channels that you can contact us on: 
- [Slack](https://join.slack.com/t/placestheplac-wum4061/shared_invite/zt-xcxsg31e-Unu5i5VPTOBuQ0bTcQU~0A
  )
- [Twitter]()

---

#### **NOTE**

`Places` is a commercial product created for the purpose of geocoding with simplicity and speed. Authorization
API tokens are necessary for using the API endpoints. Registering such API tokens is possible through 
our [website](https://sites.google.com/places.place/comingsoon) subscription page. 

&#8594; Check out our official [documentation](https://docs.google.com/document/d/1pQ2NiONDzIjCViocdG2P9RwbJrJM1P02YSVYkUFTPiE/edit?usp=sharing)!

---

#### **QUICK START**

##### The places module: 

The `places(token: str)` module allows you to register your access tokens into the `Places API` which
provides the base functionality for geocoding, density, convex, and radius calls.

&#8594; Note: The Places API package undergoes constant development so consider that endpoint changes may occur. 

To `import` the `Places API` package:

```python

from places_geocode import places_api as pa
```

---

#### **TABLE OF CONTENTS**
 
Endpoint | Function
---------|----------
load_properties_api | load_radius()
convex_search | convex()
density_search | density()
reverse_geocode | reverse()
batch_reverse | batch_reverse()
geocode | forward()
batch_geocode | batch_forward()
---

#### API EXAMPLES

All example code to the `Places API` package can be found below:

<details>
<summary>load_radius()</summary>

- coordinate: _required_, indicates `center` of search
- radius: _required_, indicates `radius` of search
- reverse_param: _option_, (_bool_ indicating the `order` of the input coordinates)

##### Example(1)
```python
pg = pa.places(token)

result = pg.load_properties(
    coordinates=[43.0961466, -77.6337776],
    radius=100,
    reverse_param=False
)
```

</details>

<details>
<summary>convex()</summary>

- coordinate_array: _required_, `edges` of polygon
- reverse_param: _optional_, (_bool_ indicating the `order` of the input coordinates)

##### Example(2)
```python
pg = pa.places(token)

result = pg.convex(
    coordinates=[[43.0961466, -77.6337776],
     [43.1018722, -77.6334654],
     [43.1010339, -77.6342459]],
    reverse_param=False
)
```

</details>

<details>
<summary>density()</summary>

#### **Radius Load Density**: 

- unit_input: _required_, str
  * options: [km, mi, m, ft, yd]
- unit_output: _required_, str 
  * options: [km, mi, m, ft, yd]
- coordinates: _optional_, _list_    
- reverse_param: _optional_, (_bool_ indicating the `order` of the input coordinates)

##### Example(3)
```python
pg = pa.places(token)
result = pg.density(
    unit_in='ft',
    unit_out='ft',
    coordinate=[43.1010339, -77.6342459],
    radius=100
)
```

---

#### **Custom Density**:

- unit_input: _required_, str
  * options: [km, mi, m, ft, yd]
- unit_output: _required_, str 
  * options: [km, mi, m, ft, yd]
- custom_option: _optional_, str
  * city
  * postcode
  * region/state
- custom_utility: _optional_, int/str, 
  * custom_utility specifies the input of `custom_option`

##### Example(4)
```python
pg = pa.places(token)
result = pg.density(
    unit_in='ft',
    unit_out='ft',
    custom_option='postcode',
    custom_utility=10980
)
```

</details>

<details>
<summary>reverse()</summary>

- coordinate: _required_, geographic location of `POI`
- radius: _optional_, radius of `error`
  * Default error radius is **10 ft**
- reverse_param: _optional_, (_bool_ indicating the reversal of the input coordinates)

##### Example(5)
```python
pg = pa.places(token)
result = pg.reverse(
    coordinate=[43.1017283, -77.6338936],
    radius=10, 
    reverse_param=False
)
```

</details>

<details>
<summary>batch_reverse()</summary>

- coordinates: _required_, geographic location(s) of `POI`
- radius: _optional_, radius of `error`
  * Default error radius is **10 ft**
- reverse_param: _optional_, (_bool_ indicating the reversal of the input coordinate)

##### Example(6)
```python
pg = pa.places(token)
result = pg.batch_reverse(
    coordinates=[[43.1017283, -77.6338985],
    [43.0936914, -77.6349024],
    [43.0937299, -77.6350315],
    [43.0930091, -77.6354702],
    [43.09245, -77.6353749]],
    radius=10,
    reverse_param=False
)
```

</details>

<details>
<summary>forward()</summary>

#### **Full Address Geocoding**

- full address: _optional_, user-defined<sub>1</sub> address of the POI
1. Places API's Flex-Formatting AI allows users to define their own U.S address format 

##### Example(7)
```python
pg = pa.places(token)
result = pg.forward(
    full_address="94 Crittenden Way, Brighton, NY, 14623",
)
```

#### **Parsed Address Geocoding**

- street: _optional_, `street` on which the POI is located
- number: _optional_, `number` of the POI's street
- postcode: _optional_, `zip code` or `microregion` of the POI
- region: _optional_, `state` in the USA<sub>1</sub> or `region` internationally
- city: _optional_, `city` where the POI is located
- unit: _optional_, `unit` if the POI is non-singular (ex. apartment)

1. If the POI is within USA borders, the region must be the state's 2-letter abbreviation
##### Example (8.1) **without** unit
```python
pg = pa.places(token)
result = pg.forward(
    street="Crittenden Way",
    number=94,
    postcode=14623,
    region="NY",
    city="Brighton",
)
```

##### Example (8.2) **with** unit
```python
pg = pa.places(token)
result = pg.forward(
    street="Crittenden Way",
    number=88,
    postcode=14623,
    region="NY",
    city="Brighton",
    unit='Unit 2'
)
```

</details>

<details>
<summary>batch_forward()</summary>

- addresses: _optional_, list of `formatted addresses`
- address_file: _optional_, `JSON` or `XML` file of formatted addresses<sub>1</sub>

1. Note: Check our [documentation]() for formatting details

##### Example(9.1) **array** of addresses
```python
pg = pa.places(token)
result = pg.batch_forward(
    addresses=["88 Crittenden Way, Brighton, NY, 14623, Unit 2",
     "140 Centre Drive, Brighton, NY, 14623",
     "94 Crittenden Way, Brighton, NY, 14623",
     "104 Crittenden Way, Brighton, NY, 14623, Unit 6"
     ]
)
```

##### Example(9.2) **file** of addresses

```python
pg = pa.places(token)
result = pg.batch_forward(
  address_file=address_file.json
)
```

```python
pg = pa.places(token)
result = pg.batch_forward(
  address_file=address_file.xml
)
```

&#8594; Download the [XML](https://github.com/MartinMashalov/PeekAPI/blob/package/analytics/address_file_XML.xml) or [JSON](https://github.com/MartinMashalov/PeekAPI/blob/okteto/analytics/test_spreadsheet_address.json) file as "address_file" to test the examples

</details>


---

#### INSTALLATION

Install the `Places API` on `pip`: 

```
$ pip install places_geocoding
```

**OR**

Install the `Places API` on `conda`: 

```
$ conda install -c Martin Mashalov places_geocoding
```

---

#### REQUIREMENTS

- [Python3](https://www.python.org/downloads/) >= 3.6
- [pymongo](https://pypi.org/project/pymongo/) >= 3.7.0
- [numpy](https://numpy.org/install/)
- [pandas](https://pandas.pydata.org/)

---

#### BUSINESS CONTACT

Our business email contact is: `hello@places.place`. Please feel free to reach out 
regarding any product feedback or support. 
