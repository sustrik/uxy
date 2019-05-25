# uxy ls

Wraps `ls` tool and outputs the results in UXY format.

The output has following fields:

- **TYPE**: Item type (`-` for normal files, `d` for directories and so on).
- **PERMISSIONS**: File permissions as reported by `ls`.
- **LINKS**: Number of links to the file.
- **OWNER**: Owner of the file.
- **GROUP**: Owner group of the file.
- **SIZE**: Size of the file in bytes.
- **TIME**: Last modification time, in ISO 8601 format.
- **NAME**: Name of the file.

When uxy is launched with `-l` option (`uxy -l ls`) following fields are added:

- **INODE**: Index number of the file.
- **BLOCKS**: Size of the file, in blocks.
- **CONTEXT**: Security context.

If `-R` option is used to do recursive listing of files, `NAME` field contains
the enitre path rather than just filename.

<pre>
<b>$ uxy ls</b>
TYPE PERMISSIONS LINKS OWNER      GROUP      SIZE         TIME                                  NAME 
-    rw-r--r--   1     martin     martin     7451         "2019-05-19 23:35:13.552174105 +0200" README.md 
-    rwxr-xr-x   1     martin     martin     11518        "2019-05-20 04:08:36.847163604 +0200" uxy 
</pre>

