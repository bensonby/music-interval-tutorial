# Tutorial for identifying written music interval (ABRSM Grade 5 music theory)

## Setup

```bash
pip install -r requirements
```

Set the policy for ImageMagick by commenting the lines in the section of `/etc/ImageMagick-7/policy.xml`

```
<!-- disable ghostscript format types -->
```

Reference: https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion

Also, comment out:

```
<policy domain="path" rights="none" pattern="@*" />
```

Reference: https://github.com/Zulko/moviepy/issues/693#issuecomment-355587113
