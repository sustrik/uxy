# uxy du

Wraps `du` tool and outputs the results in UXY format.

The output has following fields:

- **USAGE**
- **FILE**

When uxy is launched with `-l` option (`uxy -l du`) following fields are added:

- **TIME**

### Example

<pre>
<b>$ uxy du</b>
USAGE    FILE
12       ./.git/objects/56 
12       ./.git/objects/62 
12       ./.git/objects/9d 
8        ./.git/objects/04 
8        ./.git/objects/43 
932      ./.git/objects 
1096     ./.git 
48       ./test 
1192     . 
</pre>

