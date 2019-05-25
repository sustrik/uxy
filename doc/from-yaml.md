# uxy from-yaml

Converts from YAML to UXY format.

```
$ cat test.yml 
- Name: Mercury
  Diameter: 4880 km
- Name: Venus
  Diameter: 12103 km
- Name: Earth
  Diameter: 12742 km
  Color: Blue
$ uxy from-yaml < test.yml 
Color Diameter   Name
""    "4880 km"  Mercury 
""    "12103 km" Venus
Blue  "12742 km" Earth
```

