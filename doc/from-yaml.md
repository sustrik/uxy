# uxy from-yaml

Converts from YAML to UXY format.

<pre>
<b>$ cat test.yml</b>
- Name: Mercury
  Diameter: 4880 km
- Name: Venus
  Diameter: 12103 km
- Name: Earth
  Diameter: 12742 km
  Color: Blue
<b>$ uxy from-yaml < test.yml</b>
Color Diameter   Name
""    "4880 km"  Mercury 
""    "12103 km" Venus
Blue  "12742 km" Earth
</pre>
