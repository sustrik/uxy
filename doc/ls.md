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

### Example

<pre>
<b>$ uxy ls</b>
TYPE PERMISSIONS LINKS OWNER      GROUP      SIZE         TIME                                  NAME
d    rwxr-xr-x   2     martin     martin     4096         2019-05-25T16:09:58.755551983+02:00   doc 
-    rw-r--r--   1     martin     martin     1025         2019-05-24T05:37:33.571299899+02:00   LICENSE 
-    rw-r--r--   1     martin     martin     3204         2019-05-25T15:44:46.371308721+02:00   README.md 
d    rwxr-xr-x   2     martin     martin     4096         2019-05-25T11:10:55.561843561+02:00   test 
-    rwxr-xr-x   1     martin     martin     25535        2019-05-25T16:29:28.518397541+02:00   uxy 
</pre>

